"""Routers against a test-based cascade, from saved data only (paper revision, reviewer B4), version 1.

    uv run python scripts/analysis/b4_test_gate.py

Exploratory and descriptive; chosen after the test results; no new generation, no fitting.

1. Test gate. The replay's forced-failure-only policy escalates exactly the attempts that still fail their visible
   tests after the last repair round and keeps every visible-pass answer: a cascade gated by tests alone. For the
   1.7B and 9B replays (three saved frontier samples per task) this reports its pass rate and frontier calls per
   attempt beside each router at the 10/25/50% budgets (exact view), and the pass-rate difference router minus gate
   with the extra calls. The replay's own bootstrap does not cover this difference, so no interval is given.
2. Self-written tests. Many worker answers contain module-level assert statements. The sandbox runs them when it
   loads the code, so a visible-pass answer passed all of them. Asserts whose text (spaces removed) is not part of a
   visible test are the worker's own new tests. For visible-pass checkpoints (Amendment A2 exclusions applied) this
   reports the hidden-failure share by group: own new module-level tests, only copies of visible tests, none.
   Asserts inside functions or a main guard are not counted.
Writes results/b4_test_gate_v1.json.
"""

from __future__ import annotations

import json
import re
import sys

from system1.config import RESULTS, ROOT
from system1.eval.labels import load_labelled

VERSION = "b4-test-gate-v1"
WORKERS = {"Qwen3-1.7B": ("main-test-v1", ROOT / "docs/results/replay_main-test-v1_final_routers-v2.json"),
           "Qwen3.5-9B": ("q9b-test-v1", RESULTS / "replay_q9b-test-v1_final_routers-q9b-v1.json")}
ROUTERS = ["cheap", "cheap+code+thinking", "strong4 mean", "direct jev"]
ASSERT = re.compile(r"^assert\b")


def squash(s: str) -> str:
    return re.sub(r"\s+", "", s)


def main() -> int:
    out: dict = {"version": VERSION, "prespecified": False, "workers": {}}
    for w, (run, replay) in WORKERS.items():
        pol = {p["policy"]: p for p in json.loads(replay.read_text(encoding="utf-8"))["policies"]}
        gate = pol["forced-failure-only"]
        res = {"run": run, "replay": str(replay.relative_to(ROOT)),
               "always_small": pol["always-small"]["pass"], "always_frontier": pol["always-frontier"]["pass"],
               "test_gate": {"pass": gate["pass"], "calls_per_attempt": gate["frontier_calls_per_attempt"]},
               "routers": {}}
        for r in ROUTERS:
            for q in ("0.10", "0.25", "0.50"):
                p = pol.get(f"{r} | top-k | q={q}")
                if p is None:
                    continue
                res["routers"][f"{r} q={q}"] = {
                    "pass": p["pass"], "calls_per_attempt": p["frontier_calls_per_attempt"],
                    "pass_minus_gate_pp": 100 * (p["pass"] - gate["pass"]),
                    "extra_calls_per_attempt": p["frontier_calls_per_attempt"] - gate["frontier_calls_per_attempt"]}
        groups = {"own new tests": [0, 0], "only visible copies": [0, 0], "none": [0, 0]}
        for c in load_labelled(RESULTS / "runs" / run):
            if not c["visible_pass"]:
                continue
            vis = squash(" ".join(c.get("visible_tests") or []))
            asserts = [ln.strip() for ln in (c.get("code") or "").splitlines() if ASSERT.match(ln)]
            new = [a for a in asserts if squash(a) not in vis]
            g = "own new tests" if new else ("only visible copies" if asserts else "none")
            groups[g][0] += 1
            groups[g][1] += int(not c["hidden"]["passed"])
        res["self_tests"] = {g: {"visible_pass": n, "hidden_fail": f, "hidden_fail_share": f / n if n else None}
                             for g, (n, f) in groups.items()}
        out["workers"][w] = res
        print(f"== {w}: always-small {100*res['always_small']:.2f}%, test gate {100*gate['pass']:.2f}% "
              f"({100*gate['frontier_calls_per_attempt']:.1f}% calls), always-frontier {100*res['always_frontier']:.2f}%")
        for k, v in res["routers"].items():
            print(f"   {k:28s} pass {100*v['pass']:.2f}%  {v['pass_minus_gate_pp']:+.2f} pp vs gate  "
                  f"calls {100*v['calls_per_attempt']:.1f}% (+{100*v['extra_calls_per_attempt']:.1f})")
        for g, v in res["self_tests"].items():
            print(f"   self tests: {g:20s} n {v['visible_pass']:5d}  hidden fail {v['hidden_fail']:4d} ({v['hidden_fail_share']:.1%})")
    (RESULTS / "b4_test_gate_v1.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print("written results/b4_test_gate_v1.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
