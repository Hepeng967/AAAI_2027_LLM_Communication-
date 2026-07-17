"""LLM endpoint configuration without repository-embedded credentials."""

import os


class LLMModelConfig:
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url

    def __repr__(self):
        masked = self.api_key[:6] + "*" * max(0, len(self.api_key) - 6)
        return f"LLMModelConfig(api_key='{masked}', base_url='{self.base_url}')"


LLM_MODELS = {
    "deepseek-v4-flash": LLMModelConfig(
        api_key=os.getenv("DEEPSEEK_API_KEY", ""),
        base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
    ),
    "deepseek-v4-pro": LLMModelConfig(
        api_key=os.getenv("DEEPSEEK_API_KEY", ""),
        base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
    ),
    "gpt-4.1-mini": LLMModelConfig(
        api_key=os.getenv("OPENAI_API_KEY", ""),
        base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    ),
}
