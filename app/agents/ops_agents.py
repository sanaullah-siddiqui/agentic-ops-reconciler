from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel
from app.config import settings
from app.tools.ledger_tools import inspect_settlement_discrepancies
from app.tools.log_tools import search_service_logs


def build_model():
    if settings.openai_base_url:
        client = AsyncOpenAI(
            base_url=settings.openai_base_url,
            api_key=settings.openai_api_key or "local-dev-key",
        )
        return OpenAIChatCompletionsModel(model=settings.model_name, openai_client=client)
    return settings.model_name


def create_triage_orchestrator() -> Agent:
    model = build_model()

    log_analyst_agent = Agent(
        name="Log_Diagnostics_Specialist",
        handoff_description="Investigates microservice and gateway error logs for specific transaction IDs.",
        instructions=(
            "You are a Senior Site Reliability Engineer. Use `search_service_logs` to inspect "
            "warnings and errors for each flagged transaction reference. Identify the failing "
            "microservice, error code, and probable infrastructure root cause."
        ),
        tools=[search_service_logs],
        model=model,
    )

    reconciliation_coordinator = Agent(
        name="Ops_Reconciliation_Coordinator",
        instructions=(
            "You are a Lead DevOps & FinOps Reconciliation Coordinator. "
            "1. Call `inspect_settlement_discrepancies` to find mismatched or missing settlements. "
            "2. Hand off to `Log_Diagnostics_Specialist` to correlate each discrepancy with service logs. "
            "3. Produce a clean Markdown Incident & Reconciliation Triage Report containing: "
            "Executive Summary, Discrepancy Table (Tx Ref, Merchant, Issue, Root Cause Service), "
            "and Recommended Remediation Steps."
        ),
        tools=[inspect_settlement_discrepancies],
        handoffs=[log_analyst_agent],
        model=model,
    )

    return reconciliation_coordinator