"""Environment-specific facts for the shared communication-teacher pipeline."""

from .registry import get_adapter, normalize_environment

__all__ = ["get_adapter", "normalize_environment"]
