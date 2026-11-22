from pathlib import Path
from agents import function_tool
from app.config import settings


def filter_error_lines(log_text: str, keyword: str = "") -> list[str]:
    """Filters log lines for WARN/ERROR entries, optionally narrowed by transaction or service keyword."""
    results = []
    for line in log_text.splitlines():
        if ("WARN" in line or "ERROR" in line) and (not keyword or keyword in line):
            results.append(line.strip())
    return results


@function_tool
def search_service_logs(tx_ref: str = "") -> str:
    """Searches microservice operational logs for warnings and errors related to a transaction reference."""
    log_path = Path(settings.data_dir) / "service_errors.log"
    if not log_path.exists():
        return "Log file not found."
    matches = filter_error_lines(log_path.read_text(encoding="utf-8"), keyword=tx_ref)
    if not matches:
        return f"No WARN/ERROR log entries found for filter '{tx_ref}'."
    return "\n".join(matches)