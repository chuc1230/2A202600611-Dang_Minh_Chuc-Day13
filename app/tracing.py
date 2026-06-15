from __future__ import annotations

import os
from typing import Any

try:
    from langfuse import observe, get_client
    
    class LangfuseContextWrapper:
        def update_current_trace(self, **kwargs: Any) -> None:
            get_client().update_current_trace(**kwargs)

        def update_current_observation(self, **kwargs: Any) -> None:
            usage_details = kwargs.pop("usage_details", None)
            if usage_details:
                metadata = kwargs.setdefault("metadata", {})
                metadata["usage_details"] = usage_details
            get_client().update_current_span(**kwargs)

        def score_current_span(self, **kwargs: Any) -> None:
            get_client().score_current_span(**kwargs)

    langfuse_context = LangfuseContextWrapper()
except ImportError:  # pragma: no cover
    def observe(*args: Any, **kwargs: Any):
        def decorator(func):
            return func
        return decorator

    class _DummyContext:
        def update_current_trace(self, **kwargs: Any) -> None:
            return None

        def update_current_observation(self, **kwargs: Any) -> None:
            return None

    langfuse_context = _DummyContext()


def tracing_enabled() -> bool:
    return bool(os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY"))
