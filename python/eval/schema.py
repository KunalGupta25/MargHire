"""Data model for evaluation pairs, labels and results.

Each pair is one (pool, job) combination with labeled item inclusion decisions.
All types are dataclasses so they serialise cleanly to/from JSON without a third-party library.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

PoolItemKind = Literal["skill", "project", "work", "education", "certification", "publication"]


@dataclass(frozen=True)
class PoolItem:
    """One item from the professional pool."""

    id: str
    kind: PoolItemKind
    text: str
    tags: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class Job:
    title: str
    description: str


@dataclass
class Pair:
    """One evaluation unit: a pool, a job, and hand labels.

    labels maps item id -> True (should appear on the resume) / False (should not).
    Every item id in `pool` must appear in `labels`.
    """

    id: str
    created_by: str
    created_at: str  # ISO-8601 date string
    job: Job
    pool: list[PoolItem]
    labels: dict[str, bool]

    def positive_ids(self) -> set[str]:
        """Item ids that a human labelled as should-appear."""
        return {item_id for item_id, include in self.labels.items() if include}

    def validate(self) -> list[str]:
        """Return a list of validation errors (empty means valid)."""
        errors: list[str] = []
        pool_ids = {item.id for item in self.pool}
        label_ids = set(self.labels.keys())

        if not self.id:
            errors.append("pair id is empty")
        if not self.job.title:
            errors.append("job title is empty")
        if not self.job.description:
            errors.append("job description is empty")
        if not self.pool:
            errors.append("pool is empty")
        if not self.labels:
            errors.append("labels is empty")

        unlabelled = pool_ids - label_ids
        if unlabelled:
            errors.append(f"pool items without labels: {sorted(unlabelled)}")

        phantom = label_ids - pool_ids
        if phantom:
            errors.append(f"labels reference ids not in pool: {sorted(phantom)}")

        return errors


@dataclass
class AdapterResult:
    """What one adapter returned for one pair."""

    pair_id: str
    adapter_name: str
    selected_ids: list[str]
    # Wall-clock seconds for the call; None if not measured (e.g. a stub)
    latency_s: float | None = None
    # Estimated cost in USD; None if unknown
    cost_usd: float | None = None
    # Shuffle index: which shuffle of the option order was used (for order sensitivity)
    shuffle_index: int = 0


@dataclass
class PairMetrics:
    """Precision, recall and order sensitivity for one pair x adapter combination."""

    pair_id: str
    adapter_name: str
    precision: float
    recall: float
    f1: float
    # Mean item changes from the primary run to each additional shuffle.
    order_changed: float | None = None


@dataclass
class HarnessResult:
    """Aggregated result for one adapter over all pairs."""

    adapter_name: str
    pair_count: int
    macro_precision: float
    macro_recall: float
    macro_f1: float
    median_latency_s: float | None
    total_cost_usd: float | None
    per_pair: list[PairMetrics] = field(default_factory=list)
    mean_order_sensitivity: float | None = None
