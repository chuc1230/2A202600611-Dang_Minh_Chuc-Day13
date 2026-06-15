from __future__ import annotations

import random
import time
from dataclasses import dataclass

from .incidents import STATE


@dataclass
class FakeUsage:
    input_tokens: int
    output_tokens: int


@dataclass
class FakeResponse:
    text: str
    usage: FakeUsage
    model: str


from .tracing import observe


class FakeLLM:
    def __init__(self, model: str = "claude-sonnet-4-5") -> None:
        self.model = model

    @observe(as_type="generation")
    def generate(self, prompt: str) -> FakeResponse:
        time.sleep(0.15)
        input_tokens = max(20, len(prompt) // 4)
        output_tokens = random.randint(80, 180)
        if STATE["cost_spike"]:
            output_tokens *= 4
        input_cost = round((input_tokens / 1_000_000) * 3, 6)
        output_cost = round((output_tokens / 1_000_000) * 15, 6)
        total_cost = round(input_cost + output_cost, 6)
            
        try:
            from langfuse import get_client
            get_client().update_current_generation(
                model=self.model,
                usage_details={
                    "input": input_tokens,
                    "output": output_tokens
                },
                cost_details={
                    "input": input_cost,
                    "output": output_cost,
                    "total": total_cost
                }
            )
        except Exception:
            pass

        answer = (
            "Starter answer. Teams should improve this output logic and add better quality checks. "
            "Use retrieved context and keep responses concise."
        )
        return FakeResponse(text=answer, usage=FakeUsage(input_tokens, output_tokens), model=self.model)
