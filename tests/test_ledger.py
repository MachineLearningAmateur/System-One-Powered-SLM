from system1.eval.ledger import CostLedger, LedgerRow, read_jsonl, usd_for

PRICES = {
    "models": {
        "priced": {"usd_per_m_input": 2.0, "usd_per_m_output": 10.0},
        "unpriced": {"usd_per_m_input": None, "usd_per_m_output": None},
    }
}

NL = chr(10)


def test_append_and_read(tmp_path):
    ledger = CostLedger(tmp_path / "sub" / "ledger.jsonl")
    ledger.append(LedgerRow(component="router", model="m", provider="p", input_tokens=5))
    ledger.append(LedgerRow(component="frontier", model="m2", provider="p", output_tokens=7))
    rows, bad = ledger.read()
    assert bad == []
    assert [r["component"] for r in rows] == ["router", "frontier"]
    assert rows[0]["input_tokens"] == 5 and rows[1]["output_tokens"] == 7
    assert rows[0]["output_tokens"] is None  # unknown usage stays null, never zero
    assert rows[0]["ts"]


def test_read_missing_file(tmp_path):
    assert CostLedger(tmp_path / "none.jsonl").read() == ([], [])


def test_damaged_line_kept_for_audit(tmp_path):
    ledger = CostLedger(tmp_path / "ledger.jsonl")
    ledger.append(LedgerRow(component="router", model="m", provider="p"))
    with open(ledger.path, "a", encoding="utf-8") as f:
        f.write('{"component": "rout')  # interrupted write
    rows, bad = ledger.read()
    assert len(rows) == 1
    assert bad == [(2, '{"component": "rout')]


def test_append_after_damaged_tail_is_not_lost(tmp_path):
    path = tmp_path / "ledger.jsonl"
    path.write_text('{"component": "router"}' + NL + '{"component": "rou', encoding="utf-8")
    ledger = CostLedger(path)  # reopening terminates the damaged line
    ledger.append(LedgerRow(component="frontier", model="m", provider="p"))
    rows, bad = ledger.read()
    assert [r["component"] for r in rows] == ["router", "frontier"]
    assert bad == [(2, '{"component": "rou')]


def test_invalid_utf8_line_kept_for_audit(tmp_path):
    path = tmp_path / "ledger.jsonl"
    truncated_euro = bytes([0xE2, 0x82])  # a UTF-8 character cut in the middle
    path.write_bytes(b'{"component": "router"}' + b"\n" + b'{"x": "' + truncated_euro + b'"}' + b"\n")
    rows, bad = CostLedger(path).read()
    assert len(rows) == 1 and len(bad) == 1 and bad[0][0] == 2


def test_read_jsonl_never_writes(tmp_path):
    path = tmp_path / "ledger.jsonl"
    data = ('{"component": "router"}' + NL + '{"component": "rou').encode()
    path.write_bytes(data)
    rows, bad = read_jsonl(path)
    assert len(rows) == 1 and bad == [(2, '{"component": "rou')]
    assert path.read_bytes() == data  # the damaged tail is not terminated by a read
    assert read_jsonl(tmp_path / "none.jsonl") == ([], [])


def test_usd_for():
    assert usd_for(PRICES, "priced", 1_000_000, 100_000) == 3.0
    assert usd_for(PRICES, "unpriced", 10, 10) is None
    assert usd_for(PRICES, "missing", 10, 10) is None
    assert usd_for(None, "priced", 10, 10) is None
    assert usd_for(PRICES, "priced", None, 10) is None
