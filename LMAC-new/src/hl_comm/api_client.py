"""DeepSeek/OpenAI-compatible API client used by the HL communication loop."""

from __future__ import annotations

import importlib.util
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class LLMResponse:
    content: str
    usage: dict[str, Any]
    dry_run: bool = False


class DeepSeekClient:
    """Small wrapper around the OpenAI-compatible DeepSeek chat API."""

    def __init__(
        self,
        *,
        model: str = "deepseek-v4-pro",
        base_url: str = "https://api.deepseek.com",
        api_key: str = "",
        api_config: str = "",
        temperature: float = 0.2,
        reasoning_effort: str = "",
        deepseek_thinking: bool = False,
        dry_run: bool = False,
    ) -> None:
        config = self._load_api_config(api_config) if api_config else {}
        self.model = model or config.get("model") or "deepseek-v4-pro"
        self.base_url = base_url or config.get("base_url") or "https://api.deepseek.com"
        self.api_key = api_key or os.environ.get("DEEPSEEK_API_KEY") or config.get("api_key", "")
        self.temperature = temperature
        self.reasoning_effort = reasoning_effort
        self.deepseek_thinking = deepseek_thinking
        self.dry_run = dry_run

    def chat(self, messages: list[dict[str, str]], *, call_type: str) -> LLMResponse:
        if self.dry_run:
            return LLMResponse(
                content=self._dry_run_content(call_type),
                usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
                dry_run=True,
            )

        if not self.api_key:
            raise RuntimeError("No DeepSeek API key found. Set DEEPSEEK_API_KEY or pass --api-key.")
        try:
            from openai import OpenAI
        except Exception as exc:  # pragma: no cover - dependency failure
            raise RuntimeError("The openai package is required for DeepSeek API calls.") from exc

        client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "temperature": self.temperature,
        }
        if self.reasoning_effort:
            kwargs["reasoning_effort"] = self.reasoning_effort
        if self.deepseek_thinking:
            kwargs["extra_body"] = {"thinking": {"type": "enabled"}}
        resp = client.chat.completions.create(**kwargs)
        usage = {}
        if getattr(resp, "usage", None) is not None:
            usage = {
                "prompt_tokens": getattr(resp.usage, "prompt_tokens", None),
                "completion_tokens": getattr(resp.usage, "completion_tokens", None),
                "total_tokens": getattr(resp.usage, "total_tokens", None),
            }
        return LLMResponse(content=resp.choices[0].message.content, usage=usage)

    @staticmethod
    def _load_api_config(path: str) -> dict[str, str]:
        config_path = Path(path)
        if not config_path.exists():
            raise FileNotFoundError(f"API config file does not exist: {config_path}")
        spec = importlib.util.spec_from_file_location("hl_comm_external_api_config", config_path)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        try:
            spec.loader.exec_module(module)
            return {
                "api_key": getattr(module, "DEEPSEEK_API_KEY", ""),
                "model": getattr(module, "DEEPSEEK_MODEL", ""),
                "base_url": getattr(module, "DEEPSEEK_BASE_URL", ""),
            }
        except ModuleNotFoundError:
            text = config_path.read_text(encoding="utf-8")
            return {
                "api_key": _string_constant(text, "DEEPSEEK_API_KEY"),
                "model": _string_constant(text, "DEEPSEEK_MODEL"),
                "base_url": _string_constant(text, "DEEPSEEK_BASE_URL"),
            }

    @staticmethod
    def _dry_run_content(call_type: str) -> str:
        if call_type in {"init_coder", "revision_coder", "repair_coder"}:
            return """```python
import torch as th

def message_design_instruction():
    return "Dry-run teacher: explicit who/when/what functions with zero communication edges."

def communication_what(o):
    return th.zeros_like(o)

def communication_who(o):
    b, n = o.shape[0], o.shape[-2]
    return th.zeros(b, n, n, device=o.device, dtype=o.dtype)

def communication_when(o):
    b, n = o.shape[0], o.shape[-2]
    return th.zeros(b, n, n, device=o.device, dtype=o.dtype)

```"""
        return (
            '{"Evaluation": "dry-run only", '
            '"Missing_Information_Hypothesis": "not evaluated", '
            '"Improvement_Suggestions": "run without --dry-run for LLM feedback"}'
        )


def _string_constant(text: str, name: str) -> str:
    match = re.search(rf"^{name}\s*=\s*['\"]([^'\"]*)['\"]", text, flags=re.MULTILINE)
    return match.group(1) if match else ""
