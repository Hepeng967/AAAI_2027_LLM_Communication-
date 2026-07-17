"""Minimal API configuration smoke test; credentials come from the environment."""

import os

from openai import OpenAI


def build_client():
    return OpenAI(
        api_key=os.environ["DEEPSEEK_API_KEY"],
        base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
    )
