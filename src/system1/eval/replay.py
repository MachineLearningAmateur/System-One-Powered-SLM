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


def dev_percentile(score: float, dev_scores: np.ndarray, dev_weights: np.ndarray) -> float:
    """The weighted mid-rank percentile of a score in a router's frozen development distribution:
    (W(dev < s) + W(dev = s) / 2) / W. It puts the scores of different routers on one scale; the
    ranking view uses it where a missing Jev score falls back to the cheap LR."""
    total = dev_weights.sum()
    return float((dev_weights[dev_scores < score].sum() + dev_weights[dev_scores == score].sum() / 2) / total)


def top_k(scores: np.ndarray, checkpoint_ids: list[str], rate: float,
          secondary: np.ndarray | None = None, priority: np.ndarray | None = None) -> np.ndarray:
    """Boolean mask: exactly floor(rate M + 0.5) rows by descending score. Ties go first to the
    higher priority (the router's own score before a cheap-fallback score: a frozen, arbitrary
    rule), then to the higher secondary key (the raw score, compared only within one source,
    because `scores` are dev percentiles that tie between adjacent dev values), then to tie_u."""
    m = len(scores)
    k = int(math.floor(rate * m + 0.5))
    sec = np.zeros(m) if secondary is None else np.asarray(secondary, float)
    pri = np.zeros(m) if priority is None else np.asarray(priority, float)
    order = sorted(range(m), key=lambda i: (-scores[i], -pri[i], -sec[i], tie_u(checkpoint_ids[i])))
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
    # Checkpoint ids do not name the run: scores and Jev records are keyed by them, so two runs
    # with the same task and attempt would silently share them. Refuse instead.
    ids = [c["checkpoint_id"] for c in checkpoints]
    if len(ids) != len(set(ids)):
        raise ValueError("the same checkpoint id appears in more than one run; replay them separately")
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
    """Per replicate r and attempt i: the final hidden pass, and the probability that the frontier
    is called (optional or forced) or called optionally. Policies that do not look at the frontier
    answer escalate the same way in every replicate; the oracle does not."""
    name: str
    final_by_replicate: np.ndarray  # replicate x attempt
    escalated_by_replicate: np.ndarray  # replicate x attempt
    optional_by_replicate: np.ndarray  # replicate x attempt
    extra: dict = field(default_factory=dict)

    @property
    def final(self) -> np.ndarray:  # expected final pass per attempt (mean over replicates)
        return self.final_by_replicate.mean(axis=0)

    @property
    def escalated(self) -> np.ndarray:
        return self.escalated_by_replicate.mean(axis=0)

    @property
    def optional(self) -> np.ndarray:
        return self.optional_by_replicate.mean(axis=0)


def frontier_matrix(attempts: list[Attempt], values: dict[str, np.ndarray]) -> np.ndarray:
    """replicate x attempt matrix of a per-task, per-replicate quantity (outcome or cost)."""
    return np.stack([values[a.task_id] for a in attempts], axis=1)


def outcome(attempts: list[Attempt], zbar: dict[str, np.ndarray], esc_vp: np.ndarray, name: str,
            forced_to_frontier: bool = True) -> PolicyResult:
    """Final outcomes when the decision checkpoints in esc_vp (bool per attempt) escalate.
    zbar[task] holds the task's frontier outcomes, one per replicate."""
    z = frontier_matrix(attempts, zbar)
    forced = np.array([a.forced for a in attempts])
    y = np.array([a.y for a in attempts])
    opt = ~forced & np.asarray(esc_vp, bool)
    esc = opt | (forced & forced_to_frontier)
    final = np.where(esc[None, :], z, y[None, :])
    n_rep = z.shape[0]
    return PolicyResult(name, final, np.tile(esc.astype(float), (n_rep, 1)), np.tile(opt.astype(float), (n_rep, 1)))


def random_expected(attempts: list[Attempt], zbar: dict[str, np.ndarray], q_vp: float) -> PolicyResult:
    """Random escalation of a share q_vp of the decision checkpoints, in expectation (closed form)."""
    z = frontier_matrix(attempts, zbar)
    forced = np.array([a.forced for a in attempts], float)
    y = np.array([a.y for a in attempts])
    final = forced * z + (1 - forced) * ((1 - q_vp) * y + q_vp * z)
    opt = np.tile((1 - forced) * q_vp, (z.shape[0], 1))
    res = PolicyResult(f"random@{q_vp:.3f}", final, opt + forced, opt)
    res.extra["q_vp"] = q_vp
    return res


def always_frontier(attempts: list[Attempt], zbar: dict[str, np.ndarray]) -> PolicyResult:
    """The frontier answers every attempt directly; no small-model run (its cost is not charged)."""
    z = frontier_matrix(attempts, zbar)
    return PolicyResult("always-frontier", z, np.ones_like(z), np.zeros_like(z))


def oracle(attempts: list[Attempt], zbar: dict[str, np.ndarray]) -> PolicyResult:
    """Per replicate: escalate a decision checkpoint exactly when that replicate's answer passes and
    the small model's does not; forced attempts escalate as for every policy."""
    z = frontier_matrix(attempts, zbar)
    forced = np.array([a.forced for a in attempts])
    y = np.array([a.y for a in attempts])
    opt = (~forced)[None, :] & (z > y[None, :])
    esc = opt | forced[None, :]
    return PolicyResult("oracle", np.where(esc, z, y[None, :]), esc.astype(float), opt.astype(float))


def summarize(res: PolicyResult, attempts: list[Attempt], zbar: dict[str, np.ndarray]) -> dict:
    """Pass rate, rates and calls; rescues and harms per replicate, then averaged."""
    vp = np.array([not a.forced for a in attempts])
    y = np.array([a.y for a in attempts])[None, :]
    z = frontier_matrix(attempts, zbar)
    opt = res.optional_by_replicate
    return {"policy": res.name, "pass": float(res.final.mean()),
            "pass_by_replicate": [float(v) for v in res.final_by_replicate.mean(axis=1)],
            "q_vp": float(res.optional[vp].mean()) if vp.any() else 0.0, "q_total": float(res.escalated.mean()),
            "frontier_calls_per_attempt": float(res.escalated.mean()),
            "optional_calls_per_attempt": float(res.optional.mean()),
            "forced_calls_per_attempt": float((res.escalated * ~vp).mean()),
            "rescues_per_attempt": float((opt * (1 - y) * z).mean()),
            "harms_per_attempt": float((opt * y * (1 - z)).mean()),
            "n_attempts": len(attempts), "n_decisions": int(vp.sum())}


def frontier_cost(res: PolicyResult, cost_by_replicate: np.ndarray) -> np.ndarray:
    """Expected frontier dollars per attempt: escalation and cost matched replicate by replicate."""
    return (res.escalated_by_replicate * cost_by_replicate).mean(axis=0)


def _strata(attempts: list[Attempt]) -> tuple[dict[str, np.ndarray], dict[str, list[str]]]:
    idx: dict[str, list[int]] = {}
    strata: dict[str, list[str]] = {}
    for i, a in enumerate(attempts):
        if a.task_id not in idx:
            strata.setdefault(a.benchmark, []).append(a.task_id)
        idx.setdefault(a.task_id, []).append(i)
    return {t: np.array(v) for t, v in idx.items()}, strata


def _resamples(attempts: list[Attempt], n_boot: int, seed: int):
    rng = np.random.default_rng(seed)
    idx, strata = _strata(attempts)
    for _ in range(n_boot):
        yield np.concatenate([idx[t] for ts in strata.values() for t in rng.choice(ts, len(ts), replace=True)])


def task_bootstrap_gain(attempts: list[Attempt], a: np.ndarray, b: np.ndarray, n_boot: int = 2000,
                        seed: int = 0) -> tuple[float, float, float]:
    """(mean of a - b, 2.5%, 97.5%) for two fixed policies (e.g. a router against
    forced-failure-only): whole tasks resampled within benchmark, all their attempts kept."""
    d = a - b
    stats = [d[rows].mean() for rows in _resamples(attempts, n_boot, seed)]
    return float(d.mean()), float(np.percentile(stats, 2.5)), float(np.percentile(stats, 97.5))


def gain_vs_random(attempts: list[Attempt], zbar: dict[str, np.ndarray], res: PolicyResult, n_boot: int = 2000,
                   seed: int = 0) -> tuple[float, float, float]:
    """Gain over random escalation at the policy's realized rate, with that rate and the random
    expectation recomputed inside every resample. The policy's decisions are held fixed: the
    interval is conditional on its selection (for top-K, the ranking is not rerun per resample)."""
    y = np.array([a.y for a in attempts])
    zb = frontier_matrix(attempts, zbar).mean(axis=0)
    vp = np.array([not a.forced for a in attempts])
    opt, final = res.optional, res.final

    def stat(rows: np.ndarray) -> float:
        v = rows[vp[rows]]
        q = opt[v].mean() if len(v) else 0.0
        rand = np.where(vp[rows], (1 - q) * y[rows] + q * zb[rows], zb[rows])
        return float((final[rows] - rand).mean())

    point = stat(np.arange(len(attempts)))
    stats = [stat(rows) for rows in _resamples(attempts, n_boot, seed)]
    return point, float(np.percentile(stats, 2.5)), float(np.percentile(stats, 97.5))
