import numpy as np
import pytest

from system1.eval import replay as R


def cp(run, task, att, rnd, vp, passed, bench="mbpp+", tokens=10):
    return {"run_id": run, "task_id": task, "attempt": att, "round": rnd, "visible_pass": vp, "benchmark": bench,
            "checkpoint_id": f"{task}/a{att}/r{rnd}", "hidden": {"passed": passed},
            "generation": {"thinking_tokens": tokens, "answer_tokens": 0}}


def test_weighted_threshold_hits_the_rate_with_ties_and_weights():
    rng = np.random.default_rng(0)
    s = np.round(rng.random(400), 1)  # many ties
    w = rng.choice([1.0, 0.2], size=400)
    ids = [f"c{i}" for i in range(400)]
    for q in (0.0, 0.1, 0.25, 0.5, 1.0):
        t, a = R.weighted_threshold(s, w, q)
        esc = np.array([R.escalate(v, t, a, c) for v, c in zip(s, ids)])
        assert (w * esc).sum() / w.sum() == pytest.approx(q, abs=0.03)  # hash ties: close, not exact
        assert not esc[s < t].any() and esc[s > t].all()


def test_tie_hash_is_frozen_and_uniform():
    u = [R.tie_u(f"T/{i}") for i in range(5000)]
    assert R.tie_u("T/1") == R.tie_u("T/1") and 0.45 < np.mean(u) < 0.55 and min(u) >= 0 and max(u) < 1


def test_top_k_selects_exactly_k_and_breaks_ties_by_hash():
    s = np.array([0.9, 0.5, 0.5, 0.5, 0.1])
    ids = list("abcde")
    m = R.top_k(s, ids, 0.5)  # round(2.5) -> 3? floor(2.5 + 0.5) = 3
    assert m.sum() == 3 and m[0] and not m[4]
    assert m.sum() == R.top_k(s[::-1].copy(), ids[::-1], 0.5).sum()


def test_build_attempts_and_the_loop_rules():
    rows = [cp("r", "T1", 0, 1, False, False), cp("r", "T1", 0, 2, True, True),
            cp("r", "T2", 0, 1, False, False), cp("r", "T2", 0, 2, False, False), cp("r", "T2", 0, 3, False, False)]
    a = R.build_attempts(rows)
    assert [(x.task_id, x.forced, x.y, x.rounds) for x in a] == [("T1", False, 1.0, 2), ("T2", True, 0.0, 3)]
    assert a[0].decision_id == "T1/a0/r2" and a[0].gen_tokens == 20
    with pytest.raises(ValueError):  # a visible fail cannot end an attempt before round 3
        R.build_attempts([cp("r", "T3", 0, 1, False, False)])
    with pytest.raises(ValueError):  # a visible pass ends the attempt
        R.build_attempts([cp("r", "T4", 0, 1, True, True), cp("r", "T4", 0, 2, True, True)])


def test_outcomes_random_closed_form_matches_simulation():
    rng = np.random.default_rng(1)
    rows = []
    for t in range(60):
        rows.append(cp("r", f"T{t}", 0, 1, True, bool(rng.random() < 0.7)))
    rows += [cp("r", "F", 0, r, False, False) for r in (1, 2, 3)]
    att = R.build_attempts(rows)
    z = {a.task_id: rng.integers(0, 2, 3).astype(float) for a in att}
    q = 0.25
    exact = R.random_expected(att, z, q)
    vp = [i for i, a in enumerate(att) if not a.forced]
    sims = []
    for _ in range(4000):
        esc = np.zeros(len(att), bool)
        esc[rng.choice(vp, int(q * len(vp)), replace=False)] = True
        sims.append(R.outcome(att, z, esc, "x").final.mean())
    assert exact.final.mean() == pytest.approx(np.mean(sims), abs=0.003)
    small = R.outcome(att, z, np.zeros(len(att), bool), "small", forced_to_frontier=False)
    forced = R.outcome(att, z, np.zeros(len(att), bool), "forced")
    i_f = [i for i, a in enumerate(att) if a.forced][0]
    assert small.final[i_f] == 0.0 and forced.final[i_f] == z["F"].mean()
    s = R.summarize(exact, att, z)
    assert s["q_vp"] == pytest.approx(q) and s["forced_calls_per_attempt"] == pytest.approx(1 / len(att))


def test_rescues_minus_harms_is_the_gain_over_forced_only():
    rows = [cp("r", "A", 0, 1, True, False), cp("r", "B", 0, 1, True, True), cp("r", "C", 0, 1, True, True)]
    att = R.build_attempts(rows)
    z = {"A": np.array([1.0, 1.0, 0.0]), "B": np.array([0.0, 1.0, 1.0]), "C": np.array([1.0, 1.0, 1.0])}
    esc = np.array([True, True, False])
    res = R.outcome(att, z, esc, "p")
    base = R.outcome(att, z, np.zeros(3, bool), "forced")
    s = R.summarize(res, att, z)
    assert s["rescues_per_attempt"] - s["harms_per_attempt"] == pytest.approx((res.final - base.final).mean())


def test_costs_are_allocated_by_tokens():
    att = R.build_attempts([cp("r", "A", 0, 1, True, True, tokens=30), cp("r", "B", 0, 1, True, True, tokens=10)])
    R.allocate_run_costs(att, {"r": (100.0, 8.0)})
    assert [a.gpu_s for a in att] == [75.0, 25.0] and [a.energy_wh for a in att] == [6.0, 2.0]


def test_bootstrap_gain_is_centered_on_the_mean_difference():
    att = R.build_attempts([cp("r", f"T{i}", 0, 1, True, True, bench="mbpp+" if i % 2 else "humaneval+")
                            for i in range(40)])
    a = np.linspace(0, 1, 40)
    mean, lo, hi = R.task_bootstrap_gain(att, a, np.zeros(40), n_boot=500)
    assert mean == pytest.approx(0.5) and lo < mean < hi


def test_gain_vs_random_recomputes_the_rate_in_each_resample():
    # Codex's case: two failing small attempts, both always rescued; the router escalates one.
    att = R.build_attempts([cp("r", "A", 0, 1, True, False), cp("r", "B", 0, 1, True, False)])
    z = {"A": np.ones(3), "B": np.ones(3)}
    res = R.outcome(att, z, np.array([True, False]), "p")
    point, lo, hi = R.gain_vs_random(att, z, res, n_boot=500)
    assert point == pytest.approx(0.0) and lo == pytest.approx(0.0) and hi == pytest.approx(0.0)


def test_oracle_rescues_and_costs_are_counted_per_replicate():
    att = R.build_attempts([cp("r", "A", 0, 1, True, False)])
    z = {"A": np.array([1.0, 0.0, 0.0])}
    orc = R.oracle(att, z)
    s = R.summarize(orc, att, z)
    assert s["rescues_per_attempt"] == pytest.approx(1 / 3) and orc.final[0] == pytest.approx(1 / 3)
    cost = R.frontier_matrix(att, {"A": np.array([9.0, 1.0, 1.0])})
    assert R.frontier_cost(orc, cost)[0] == pytest.approx(3.0)


def test_dev_percentile_puts_scores_on_one_scale():
    dev = np.array([0.1, 0.2, 0.2, 0.9])
    w = np.array([1.0, 1.0, 1.0, 1.0])
    assert R.dev_percentile(0.2, dev, w) == pytest.approx((1 + 1) / 4)
    assert R.dev_percentile(1.0, dev, w) == 1.0 and R.dev_percentile(0.0, dev, w) == 0.0


def test_the_same_checkpoint_in_two_runs_is_refused():
    with pytest.raises(ValueError):
        R.build_attempts([cp("r1", "A", 0, 1, True, True), cp("r2", "A", 0, 1, True, True)])


def test_percentile_ties_keep_the_raw_score_order():
    dev, w = np.array([0.1, 0.5]), np.ones(2)
    raw = np.array([0.3, 0.4])
    pct = np.array([R.dev_percentile(v, dev, w) for v in raw])
    assert pct[0] == pct[1]  # both fall between the two dev values
    for ids in (["a", "b"], ["b", "a"]):
        assert list(R.top_k(pct, ids, 0.5, secondary=raw)) == [False, True]


def test_frontier_call_cost_never_assumes_zero_billing():
    import importlib.util
    from pathlib import Path
    spec = importlib.util.spec_from_file_location("replay_script", Path(__file__).resolve().parents[1] / "scripts" / "replay.py")
    rs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rs)
    assert rs.call_cost([], "absent") == (0.0, False)
    timeout = {"call_id": "c", "usd_reported": None, "usd_computed": None, "status": "transport:ReadTimeout",
               "output_tokens": None}
    ok = {"call_id": "c", "usd_reported": 0.002, "usd_computed": 0.002, "status": "ok", "output_tokens": 10}
    assert rs.call_cost([timeout, ok], "c") == (0.002, False)
    assert rs.call_cost([ok], "c") == (0.002, True)


def test_external_router_score_and_missing_fallback():
    import importlib.util
    from pathlib import Path
    spec = importlib.util.spec_from_file_location("replay_script2", Path(__file__).resolve().parents[1] / "scripts" / "replay.py")
    rs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rs)
    router = {"model": {"kind": "external"}}
    row = {"cp": {"checkpoint_id": "T/a0/r1"}}
    assert rs.score_final(row, router, {"T/a0/r1": {"score": 0.25}}) == 0.25
    assert rs.score_final(row, router, {}) is None  # missing -> the cheap LR decides
    assert rs.ARMS["pinocchio"] == []  # no Jev cost


def test_top_k_cross_source_ties_put_own_scores_first():
    pct = np.array([0.5, 0.5, 0.5])
    raw = np.array([0.1, 0.9, 0.2])  # row 1 is a cheap-fallback score on another scale
    own = np.array([1.0, 0.0, 1.0])
    m = R.top_k(pct, ["a", "b", "c"], 0.34, secondary=raw, priority=own)  # k = 1
    assert list(m) == [False, False, True]  # own scores first, then raw order within the source


def test_pinocchio_records_must_match_execution_input_and_setup():
    from system1.features import pinocchio_input as PI
    tasks = {"T": type("Task", (), {"prompt": "def f():", "shown_tests": "", "task_id": "T"})()}
    cp_ = {"checkpoint_id": "T/a0/r1", "exec_id": "e1", "task_id": "T", "answer": "x", "code": "def f(): pass\n"}
    import system1.features.pinocchio_input as mod
    orig = mod.first_round_messages
    mod.first_round_messages = lambda task: [{"role": "user", "content": task.prompt}]
    try:
        good = {"checkpoint_id": "T/a0/r1", "exec_id": "e1", "input_version": PI.V2,
                "input_sha256": PI.input_sha(*PI.build_input(cp_, tasks, PI.V2)), **PI.PINNED}
        stale = {**good, "exec_id": "e0"}
        legacy = {k: v for k, v in good.items() if k not in ("adapter_revision", "dtype")}
        recs, counts = PI.select_records([stale, good], [cp_], tasks, PI.V2, require_pinned=True)
        assert recs["T/a0/r1"] is good and counts["stale"] == 1
        recs, counts = PI.select_records([legacy], [cp_], tasks, PI.V2, require_pinned=True)
        assert recs == {} and counts["stale"] == 1
        assert PI.select_records([legacy], [cp_], tasks, PI.V2, require_pinned=False)[0]
        with pytest.raises(PI.PinocchioRecordError):
            PI.select_records([good, dict(good)], [cp_], tasks, PI.V2, require_pinned=True)
    finally:
        mod.first_round_messages = orig
