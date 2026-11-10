"""LLM adapter stub.

Phase 0: not wired to a real model. Returns an empty selection so the harness
and metrics code can be tested without any API keys.
"""

from __future__ import annotations

from ..schema import AdapterResult, Pair
from .base import Adapter


class LLMAdapter(Adapter):
    """Stub LLM adapter. Wire to a real provider in Phase 2."""

    @property
    def name(self) -> str:
        return "llm-stub"

    def select(self, pair: Pair, shuffle_index: int = 0) -> AdapterResult:
        # ponytail: stub returns empty; replace with real call in Phase 2
        return AdapterResult(
            pair_id=pair.id,
            adapter_name=self.name,
            selected_ids=[],
            latency_s=None,
            cost_usd=None,
            shuffle_index=shuffle_index,
        )
