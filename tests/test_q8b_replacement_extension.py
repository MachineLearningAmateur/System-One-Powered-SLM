"""Offline integration checks for the already-inspected 8B replacement extension."""

import hashlib
import importlib.util
from pathlib import Path

import numpy as np
import pytest


def extension():
    path = Path(__file__).resolve().parents[1] / "scripts" / "analysis" / "q8b_replacement_extension.py"
    spec = importlib.util.spec_from_file_location("q8b_replacement_extension", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_frozen_population_and_equal_optional_budget():
    m = extension()
    if not m.MANIFEST.exists() or not (m.RESULTS / "runs" / m.SOURCE_RUN / "hidden_labels.jsonl").exists():
        pytest.skip("operator-held 8B artifacts or freeze manifest unavailable")
    frozen = m.verify_manifest()
    assert len(frozen["task_ids"]) == 324
    assert frozen["analysis"]["n_attempts"] == 1620
    assert frozen["policies"]["forced_count"] == 40
    assert frozen["policies"]["optional_count"] == 395
    for ids in frozen["policies"]["selected_checkpoint_ids"].values():
        assert len(ids) == 395 and len(set(ids)) == 395


def test_mocked_two_sample_replay_saves_tables_without_model_or_grader_calls(tmp_path, monkeypatch):
    m = extension()
    if not m.MANIFEST.exists() or not (m.RESULTS / "runs" / m.SOURCE_RUN / "hidden_labels.jsonl").exists():
        pytest.skip("operator-held 8B artifacts or freeze manifest unavailable")
    frozen = m.verify_manifest()
    outcomes = {}
    costs = {}
    for task in frozen["task_ids"]:
        h = int(hashlib.sha256(task.encode()).hexdigest()[:8], 16)
        outcomes[task] = np.array([float(h % 3 == 0), float(h % 5 == 0)])
        costs[task] = np.array([0.002, 0.0025])
    def mock_frontier(run, manifest):
        assert run == m.FRONTIER_RUN
        assert manifest == frozen
        return outcomes, costs, {"replicates": 2, "calls_with_unknown_cost": 0, "grade_session": "synthetic"}
    monkeypatch.setattr(m, "_frontier_data", mock_frontier)
    monkeypatch.setattr(m, "OUT", tmp_path)
    monkeypatch.setattr(m, "N_BOOT", 30)
    path = m.analyze(m.FRONTIER_RUN)
    assert path.exists()
    assert (tmp_path / "policy_table.csv").exists()
    assert (tmp_path / "paired_comparisons.csv").exists()
    assert (tmp_path / "discordant_optional.csv").exists()
    assert (tmp_path / "paper_table.md").exists()
    assert (tmp_path / "pass_vs_cost.svg").exists()
    import json
    data = json.loads(path.read_text())
    assert len(data["policies"]) == 7
    assert len(data["comparisons"]) == 6
    assert data["frontier_recorded_collection_usd"] == pytest.approx(324 * (0.002 + 0.0025))
