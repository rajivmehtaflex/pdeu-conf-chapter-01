from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from deepagents import create_deep_agent
from loguru import logger

ROOT = Path(__file__).resolve().parent
ENV_PATH = ROOT / ".env"
DEFAULT_MODEL = "openrouter:inclusionai/ring-2.6-1t:free"

SYSTEM_PROMPT = """
Layer 1 - Role Definition:
You are the Senior Financial Auditor for Shree Manufacturing Pvt. Ltd. Your job is to protect the company from overpayments and ensure compliance.

Layer 2 - Business Rules:
Any discrepancy greater than INR 0 must be reported. Standard payment terms are 30 days net unless specified otherwise. Late deliveries may incur penalties based on contract clauses.

Layer 3 - Data Conventions:
Currency must always be formatted in INR. Dates are handled in YYYY-MM-DD format.

Layer 4 - Protocols:
Before drawing conclusions, cross-reference invoices against warehouse receipts and legal contracts.

Layer 5 - Escalations and Guardrails:
Refuse questions outside finance, auditing, and corporate compliance for Shree Manufacturing. Redirect the user back to audit work.
""".strip()


def build_agent(model_name: str):
    return create_deep_agent(
        model=model_name,
        tools=[],
        system_prompt=SYSTEM_PROMPT,
    )


def run_self_check() -> str:
    return "Senior Financial Auditor for Shree Manufacturing Pvt. Ltd."


def load_model_name() -> str:
    load_dotenv(ENV_PATH)
    return os.getenv("OPENROUTER_MODEL") or os.getenv("MODEL_NAME") or DEFAULT_MODEL


def invoke_agent(prompt: str) -> str:
    agent = build_agent(load_model_name())
    result = agent.invoke({"messages": [{"role": "user", "content": prompt}]})
    messages = result.get("messages", [])
    if not messages:
        return ""
    final = messages[-1]
    return str(getattr(final, "content", final))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", nargs="?", default="What is your job?")
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args(argv)

    if args.self_check:
        print(run_self_check())
        return 0

    print(invoke_agent(args.prompt))
    return 0
