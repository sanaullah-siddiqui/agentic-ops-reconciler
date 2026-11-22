import json
from pathlib import Path
from agents import function_tool
from app.config import settings


def compare_ledgers(expected: list[dict], actual: list[dict]) -> list[dict]:
    """Deterministic comparison between expected POS transactions and actual settlement records."""
    actual_map = {row["tx_ref"]: row for row in actual}
    discrepancies: list[dict] = []

    for exp in expected:
        ref = exp["tx_ref"]
        act = actual_map.get(ref)

        if act is None:
            discrepancies.append({
                "tx_ref": ref,
                "merchant_id": exp["merchant_id"],
                "type": "MISSING_IN_SETTLEMENT",
                "expected_amount": exp["amount"],
                "actual_amount": None,
                "actual_status": "NOT_FOUND",
            })
        elif exp["amount"] != act["amount"] or act["status"] != "SETTLED":
            discrepancies.append({
                "tx_ref": ref,
                "merchant_id": exp["merchant_id"],
                "type": "AMOUNT_OR_STATUS_MISMATCH",
                "expected_amount": exp["amount"],
                "actual_amount": act["amount"],
                "actual_status": act["status"],
            })

    return discrepancies


@function_tool
def inspect_settlement_discrepancies() -> str:
    """Loads expected and actual settlement JSON files and returns all detected transaction discrepancies."""
    base = Path(settings.data_dir)
    expected = json.loads((base / "expected_settlements.json").read_text(encoding="utf-8"))
    actual = json.loads((base / "actual_settlements.json").read_text(encoding="utf-8"))
    mismatches = compare_ledgers(expected, actual)
    return json.dumps({"total_discrepancies": len(mismatches), "items": mismatches}, indent=2)