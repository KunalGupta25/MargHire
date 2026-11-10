"""Clef / Clef-flash adapter stub.

Clef and Clef-flash are decision models on Cloudflare Workers AI.
Phase 0: stub only. Wire to Cloudflare Workers AI in Phase 2/3.
"""

from __future__ import annotations

from ..schema import AdapterResult, Pair
from .base import Adapter


class ClefAdapter(Adapter):
    """Stub Clef adapter. Wire to Cloudflare Workers AI in Phase 3."""

    def __init__(self, flash: bool = False) -> None:
        self._flash = flash

    @property
    def name(self) -> str:
        return "clef-flash-stub" if self._flash else "clef-stub"

    def select(self, pair: Pair, shuffle_index: int = 0) -> AdapterResult:
        # ponytail: stub returns empty; replace with Workers AI call in Phase 3
        return AdapterResult(
            pair_id=pair.id,
            adapter_name=self.name,
            selected_ids=[],
            latency_s=None,
            cost_usd=None,
            shuffle_index=shuffle_index,
        )
