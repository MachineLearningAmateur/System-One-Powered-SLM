"""Offline replay of escalation policies (docs/research-plan.md, "Still to freeze
before the replay", frozen October 17).

The loop accepts a visible pass at once, so an attempt has at most one optional
decision: its visible-pass checkpoint (the "decision checkpoint"). An attempt
without a visible pass ended after round 3 and is a forced escalation for every
policy except always-small (frozen visible-fail rule). Policies differ only at
decision checkpoints; every policy runs the same logged small-model attempt.

Outcomes are computed in closed form from the frontier replicates: for a task
with frontier outcomes z_1..z_R, zbar is their mean; an escalated attempt ends
with zbar (the mean over replicates), an accepted one with its own hidden label
y. Random escalation at rate q selects K of the M decision checkpoints uniformly,
so its expected outcome is (1 - q) y + q zbar at each of them.

Thresholds (weighted_threshold, escalate): s > t, or s = t and u < alpha, with u
a frozen hash of the checkpoint id (tie_u). The ranking view (top_k) escalates
exactly round(q M) checkpoints by score, ties ordered by the same hash.
"""

from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass, field

import numpy as np

RATES = (0.10, 0.25, 0.50)
TIE_TAG = "s1-tie-v1"


def tie_u(checkpoint_id: str) -> float:
    """A frozen, label-free uniform number in [0, 1) for one checkpoint."""
    return int(hashlib.sha256(f"{TIE_TAG}:{checkpoint_id}".encode()).hexdigest()[:13], 16) / 16 ** 13


def weighted_threshold(scores: np.ndarray, weights: np.ndarray, rate: float) -> tuple[float, float]:
    """(t, alpha) so that the weighted share escalated by `escalate` is `rate` on these rows:
    W(s > t) <= rate W <= W(s >= t), alpha = (rate W - W(s > t)) / W(s = t)."""
    if not 0.0 <= rate <= 1.0:
        raise ValueError("rate must be in [0, 1]")
    scores, weights = np.asarray(scores, float), np.asarray(weights, float)
    total = weights.sum()
    if rate == 0.0:
        return math.inf, 0.0
    target = rate * total
    for t in np.unique(scores)[::-1]:  # from the highest score down
        above = weights[scores > t].sum()
        at = weights[scores == t].sum()
        if above + at >= target - 1e-12:
            return float(t), float(min(1.0, max(0.0, (target - above) / at)))
    return float(scores.min()), 1.0


def escalate(score: float, t: float, alpha: float, checkpoint_id: str) -> bool:
    return score > t or (score == t and tie_u(checkpoint_id) < alpha)


def top_k(scores: np.ndarray, checkpoint_ids: list[str], rate: float) -> np.ndarray:
    """Boolean mask: exactly floor(rate M + 0.5) rows by descending score, ties by tie_u."""
    m = len(scores)
    k = int(math.floor(rate * m + 0.5))
    order = sorted(range(m), key=lambda i: (-scores[i], tie_u(checkpoint_ids[i])))
    mask = np.zeros(m, bool)
    mask[order[:k]] = True
    return mask


@dataclass
class Attempt:
    run: str
    task_id: str
    benchmark: str
    attempt: int
    rounds: int
    decision_id: str | None  # checkpoint id of the visible-pass checkpoint, or None (forced)
    y: float  # hidden pass of the final small-model candidate (0/1)
    gen_tokens: int  # thinking + answer tokens over all rounds
    gpu_s: float = 0.0  # allocated share of the run's wall time
    energy_wh: float = 0.0  # allocated share of the run's energy

    @property
    def forced(self) -> bool:
        return self.decision_id is None


def build_attempts(checkpoints: list[dict], max_rounds: int = 3) -> list[Attempt]:
    """One Attempt per (run, task, attempt) from labelled checkpoints (eval.labels.load_labelled)."""
    groups: dict[tuple, list[dict]] = {}
    for c in checkpoints:
        groups.setdefault((c["run_id"], c["task_id"], c["attempt"]), []).append(c)
    out = []
    for (run, task, att), cps in sorted(groups.items()):
        cps = sorted(cps, key=lambda c: c["round"])
        if [c["round"] for c in cps] != list(range(1, len(cps) + 1)):
            raise ValueError(f"{run} {task} a{att}: rounds are not 1..n")
        last = cps[-1]
        if any(c["visible_pass"] for c in cps[:-1]):
            raise ValueError(f"{run} {task} a{att}: a visible pass before the last round")
        if not last["visible_pass"] and last["round"] != max_rounds:
            raise ValueError(f"{run} {task} a{att}: ended in a visible fail before round {max_rounds}")
        tokens = sum(c["generation"]["thinking_tokens"] + c["generation"]["answer_tokens"] for c in cps)
        out.append(Attempt(run=run, task_id=task, benchmark=last["benchmark"], attempt=att, rounds=len(cps),
                           decision_id=last["checkpoint_id"] if last["visible_pass"] else None,
                           y=float(bool(last["hidden"]["passed"])), gen_tokens=tokens))
    return out


def allocate_run_costs(attempts: list[Attempt], run_totals: dict[str, tuple[float, float]]) -> None:
    """Give each attempt its share (by generated tokens) of its run's wall time and energy."""
    for run, (secs, wh) in run_totals.items():
        mine = [a for a in attempts if a.run == run]
        n = sum(a.gen_tokens for a in mine)
        for a in mine:
            a.gpu_s, a.energy_wh = secs * a.gen_tokens / n, wh * a.gen_tokens / n


@dataclass
class PolicyResult:
    name: str
    final: np.ndarray  # expected final hidden pass per attempt (mean over frontier replicates)
    final_by_replicate: np.ndarray  # replicate x attempt
    escalated: np.ndarray  # per attempt: probability that the frontier is called (optional or forced)
    optional: np.ndarray  # per attempt: probability of an optional escalation at its decision checkpoint
    extra: dict = field(default_factory=dict)


def outcome(attempts: list[Attempt], zbar: dict[str, np.ndarray], esc_vp: np.ndarray, name: str,
            forced_to_frontier: bool = True) -> PolicyResult:
    """Final outcomes when the decision checkpoints in esc_vp (bool per attempt) escalate.
    zbar[task] holds the task's frontier outcomes, one per replicate."""
    n_rep = len(next(iter(zbar.values())))
    by_rep = np.zeros((n_rep, len(attempts)))
    escalated = np.zeros(len(attempts), bool)
    optional = np.zeros(len(attempts), bool)
    for i, a in enumerate(attempts):
        z = zbar[a.task_id]
        if a.forced:
            use_frontier = forced_to_frontier
        else:
            use_frontier = bool(esc_vp[i])
            optional[i] = use_frontier
        escalated[i] = use_frontier
        by_rep[:, i] = z if use_frontier else a.y
    return PolicyResult(name, by_rep.mean(axis=0), by_rep, escalated.astype(float), optional.astype(float))


def random_expected(attempts: list[Attempt], zbar: dict[str, np.ndarray], q_vp: float) -> PolicyResult:
    """Random escalation of a share q_vp of the decision checkpoints, in expectation (closed form)."""
    n_rep = len(next(iter(zbar.values())))
    by_rep = np.zeros((n_rep, len(attempts)))
    for i, a in enumerate(attempts):
        z = zbar[a.task_id]
        by_rep[:, i] = z if a.forced else (1 - q_vp) * a.y + q_vp * z
    forced = np.array([a.forced for a in attempts], float)
    optional = (1 - forced) * q_vp
    res = PolicyResult(f"random@{q_vp:.3f}", by_rep.mean(axis=0), by_rep, forced + optional, optional)
    res.extra["q_vp"] = q_vp
    return res


def always_frontier(attempts: list[Attempt], zbar: dict[str, np.ndarray]) -> PolicyResult:
    """The frontier answers every attempt directly; no small-model run (its cost is not charged)."""
    by_rep = np.stack([zbar[a.task_id] for a in attempts], axis=1)
    return PolicyResult("always-frontier", by_rep.mean(axis=0), by_rep, np.ones(len(attempts)),
                        np.zeros(len(attempts)))


def summarize(res: PolicyResult, attempts: list[Attempt], zbar: dict[str, np.ndarray]) -> dict:
    vp = np.array([not a.forced for a in attempts])
    y = np.array([a.y for a in attempts])
    zb = np.array([zbar[a.task_id].mean() for a in attempts])
    opt = res.optional
    return {"policy": res.name, "pass": float(res.final.mean()),
            "pass_by_replicate": [float(v) for v in res.final_by_replicate.mean(axis=1)],
            "q_vp": float(opt[vp].mean()) if vp.any() else 0.0, "q_total": float(res.escalated.mean()),
            "frontier_calls_per_attempt": float(res.escalated.mean()),
            "optional_calls_per_attempt": float(opt.mean()),
            "forced_calls_per_attempt": float((res.escalated * ~vp).mean()),
            "rescues_per_attempt": float((opt * (1 - y) * zb).mean()),
            "harms_per_attempt": float((opt * y * (1 - zb)).mean()),
            "n_attempts": len(attempts), "n_decisions": int(vp.sum())}


def task_bootstrap_gain(attempts: list[Attempt], a: np.ndarray, b: np.ndarray, n_boot: int = 2000,
                        seed: int = 0) -> tuple[float, float, float]:
    """(mean of a - b, 2.5%, 97.5%): whole tasks resampled within benchmark, all their attempts kept."""
    rng = np.random.default_rng(seed)
    d = a - b
    by_task: dict[str, list[int]] = {}
    for i, at in enumerate(attempts):
        by_task.setdefault(at.task_id, []).append(i)
    strata: dict[str, list[str]] = {}
    for at in attempts:
        if at.task_id not in strata.setdefault(at.benchmark, []):
            strata[at.benchmark].append(at.task_id)
    idx = {t: np.array(v) for t, v in by_task.items()}
    stats = []
    for _ in range(n_boot):
        rows = np.concatenate([idx[t] for ts in strata.values() for t in rng.choice(ts, len(ts), replace=True)])
        stats.append(d[rows].mean())
    return float(d.mean()), float(np.percentile(stats, 2.5)), float(np.percentile(stats, 97.5))
