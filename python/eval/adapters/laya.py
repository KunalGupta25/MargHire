"""Laya local inference adapter stub.

Laya is a local decision model that runs through the Python helper sidecar.
Phase 0: stub only. Wire to the actual Laya process in Phase 2/3.
"""

from __future__ import annotations

from ..schema import AdapterResult, Pair
from .base import Adapter


class LayaAdapter(Adapter):
    """Stub Laya adapter. Wire to local Laya process in Phase 3."""

    @property
    def name(self) -> str:
        return "laya-stub"

    def select(self, pair: Pair, shuffle_index: int = 0) -> AdapterResult:
        # ponytail: stub returns empty; replace with Laya HTTP call in Phase 3
        return AdapterResult(
            pair_id=pair.id,
            adapter_name=self.name,
            selected_ids=[],
            latency_s=None,
            cost_usd=None,
            shuffle_index=shuffle_index,
        )
