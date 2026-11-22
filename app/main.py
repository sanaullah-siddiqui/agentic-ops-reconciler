import asyncio
import logging
from pathlib import Path
from agents import Runner
from app.agents.ops_agents import create_triage_orchestrator
from app.config import settings

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger("ops-reconciler")


async def run_triage() -> str:
    if not settings.openai_api_key and not settings.openai_base_url:
        raise RuntimeError("Set OPENAI_API_KEY or OPENAI_BASE_URL in your environment before running.")

    orchestrator = create_triage_orchestrator()
    logger.info("Starting multi-agent reconciliation and log triage run...")

    result = await Runner.run(
        orchestrator,
        "Run batch settlement reconciliation against today's expected ledger, correlate anomalies "
        "with service logs, and generate a structured Markdown triage report.",
    )

    report_text = str(result.final_output)
    out_path = Path(settings.output_report)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report_text, encoding="utf-8")
    logger.info("Triage report written to %s", out_path)
    return report_text


if __name__ == "__main__":
    output = asyncio.run(run_triage())
    print("\n" + output)