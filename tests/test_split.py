import json
import random

import pytest

from system1.eval.split import load_split, make_split, split_of

IDS = {
    "humaneval+": [f"HumanEval/{i}" for i in range(164)],
    "mbpp+": [f"Mbpp/{i}" for i in range(2, 380)],
}


def test_sizes_match_the_plan():
    s = make_split(IDS)
    he, mb = s["benchmarks"]["humaneval+"], s["benchmarks"]["mbpp+"]
    assert (len(he["dev"]), len(he["test"])) == (66, 98)
    assert (len(mb["dev"]), len(mb["test"])) == (151, 227)


def test_deterministic_and_independent_of_input_order():
    shuffled = {b: random.Random(1).sample(ids, len(ids)) for b, ids in IDS.items()}
    assert make_split(IDS) == make_split(shuffled)
    assert make_split(IDS) != make_split(IDS, seed=1)


def test_disjoint_complete_and_lookup(tmp_path):
    s = make_split(IDS)
    for bench, part in s["benchmarks"].items():
        assert set(part["dev"]).isdisjoint(part["test"])
        assert set(part["dev"]) | set(part["test"]) == set(IDS[bench])
    p = tmp_path / "split.json"
    p.write_text(json.dumps(s), encoding="utf-8")
    loaded = load_split(p)
    assert split_of(loaded, s["benchmarks"]["mbpp+"]["dev"][0]) == "dev"
    assert split_of(loaded, s["benchmarks"]["humaneval+"]["test"][0]) == "test"
    with pytest.raises(KeyError):
        split_of(loaded, "HumanEval/9999")


def test_load_rejects_overlap(tmp_path):
    s = make_split(IDS)
    part = s["benchmarks"]["humaneval+"]
    part["test"][0] = part["dev"][0]
    p = tmp_path / "split.json"
    p.write_text(json.dumps(s), encoding="utf-8")
    with pytest.raises(ValueError):
        load_split(p)
