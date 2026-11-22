from app.tools.ledger_tools import compare_ledgers
from app.tools.log_tools import filter_error_lines


def test_compare_ledgers_detects_missing_and_mismatched():
    expected = [
        {"tx_ref": "TX-1", "merchant_id": "M-1", "amount": 100.0, "status": "APPROVED"},
        {"tx_ref": "TX-2", "merchant_id": "M-1", "amount": 200.0, "status": "APPROVED"},
        {"tx_ref": "TX-3", "merchant_id": "M-2", "amount": 300.0, "status": "APPROVED"},
    ]
    actual = [
        {"tx_ref": "TX-1", "merchant_id": "M-1", "amount": 100.0, "status": "SETTLED"},
        {"tx_ref": "TX-2", "merchant_id": "M-1", "amount": 150.0, "status": "SETTLED"},
    ]

    issues = compare_ledgers(expected, actual)
    assert len(issues) == 2
    assert issues[0]["tx_ref"] == "TX-2"
    assert issues[0]["type"] == "AMOUNT_OR_STATUS_MISMATCH"
    assert issues[1]["tx_ref"] == "TX-3"
    assert issues[1]["type"] == "MISSING_IN_SETTLEMENT"


def test_filter_error_lines():
    sample_log = (
        "2026-11-22T08:00:00Z INFO [worker] Healthy\n"
        "2026-11-22T08:01:00Z ERROR [hsm] Timeout on TX-99\n"
    )
    matches = filter_error_lines(sample_log, keyword="TX-99")
    assert len(matches) == 1
    assert "HSM" in matches[0].upper()