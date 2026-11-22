import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_base_url: str | None = os.getenv("OPENAI_BASE_URL") or None
    model_name: str = os.getenv("MODEL_NAME", "gpt-4o-mini")
    data_dir: str = os.getenv("DATA_DIR", "data")
    output_report: str = os.getenv("OUTPUT_REPORT", "output/triage_report.md")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()