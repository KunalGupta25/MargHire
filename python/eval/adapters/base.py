"""Abstract base class for Role Lens adapters.

An adapter takes a Pair and returns the item ids it thinks should appear on the resume.
"""

from __future__ import annotations

import abc
import random

from ..schema import AdapterResult, Pair


class Adapter(abc.ABC):
    """Base class for all Role Lens evaluation adapters."""

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Short identifier used in result files and reports."""

    @property
    def model_id(self) -> str:
        """Provider model identifier, or the adapter name for a stub."""
        return self.name

    @abc.abstractmethod
    def select(self, pair: Pair, shuffle_index: int = 0) -> AdapterResult:
        """Select item ids from pair.pool that should appear for pair.job.

        Args:
            pair: The evaluation pair to process.
            shuffle_index: Which shuffle of the option order to use. Callers
                that want order-sensitivity measurements call this multiple
                times with different indices.

        Returns:
            AdapterResult with selected_ids and any available latency or cost data.
        """

    def _shuffled_pool(self, pair: Pair, shuffle_index: int) -> list[str]:
        """Return pool item ids in a reproducibly shuffled order.

        The same shuffle_index always produces the same order for the same pair,
        so order-sensitivity measurements are reproducible.
        """
        ids = [item.id for item in pair.pool]
        rng = random.Random(f"{pair.id}:{shuffle_index}")
        rng.shuffle(ids)
        return ids
