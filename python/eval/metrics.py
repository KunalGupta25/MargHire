"""Evaluation metrics for Role Lens comparison.

All functions are pure so they can be unit-tested without any model calls.
"""

from __future__ import annotations

import statistics
from collections.abc import Sequence

from .schema import AdapterResult, HarnessResult, Pair, PairMetrics


def precision(selected: set[str], positive: set[str]) -> float:
    """Of items selected, what fraction are truly positive?

    Returns 1.0 when selected is empty (no false positives made).
    """
    if not selected:
        return 1.0
    return len(selected & positive) / len(selected)


def recall(selected: set[str], positive: set[str]) -> float:
    """Of truly positive items, what fraction were selected?

    Returns 1.0 when positive is empty (nothing to recall).
    """
    if not positive:
        return 1.0
    return len(selected & positive) / len(positive)


def f1(prec: float, rec: float) -> float:
    """Harmonic mean of precision and recall. Returns 0.0 when both are 0."""
    if prec + rec == 0:
        return 0.0
    return 2 * prec * rec / (prec + rec)


def order_sensitivity(result_a: AdapterResult, result_b: AdapterResult) -> int:
    """Number of item ids that differ between two shuffle runs of the same pair.

    Both results must be for the same pair and adapter.
    """
    if result_a.pair_id != result_b.pair_id:
        raise ValueError("Cannot compare order sensitivity across different pairs")
    set_a = set(result_a.selected_ids)
    set_b = set(result_b.selected_ids)
    return len(set_a.symmetric_difference(set_b))


def pair_metrics(pair: Pair, result: AdapterResult) -> PairMetrics:
    """Compute precision, recall and f1 for one (pair, result) combination."""
    selected = set(result.selected_ids)
    positive = pair.positive_ids()
    prec = precision(selected, positive)
    rec = recall(selected, positive)
    return PairMetrics(
        pair_id=pair.id,
        adapter_name=result.adapter_name,
        precision=prec,
        recall=rec,
        f1=f1(prec, rec),
    )


def aggregate(
    pairs: Sequence[Pair],
    results: Sequence[AdapterResult],
    adapter_name: str,
) -> HarnessResult:
    """Aggregate per-pair metrics into a HarnessResult for one adapter.

    Args:
        pairs: All pairs that were evaluated.
        results: Adapter outputs for the primary and optional shuffled runs.
        adapter_name: Name of the adapter being aggregated.

    Returns:
        HarnessResult with macro-averaged metrics.
    """
    pair_map = {p.id: p for p in pairs}
    primary = [
        r
        for r in results
        if r.adapter_name == adapter_name
        and r.shuffle_index == 0
        and r.pair_id in pair_map
    ]

    per_pair: list[PairMetrics] = []
    order_differences: list[float] = []
    for result in primary:
        pair = pair_map.get(result.pair_id)
        if pair is None:
            continue
        metrics = pair_metrics(pair, result)
        variants = [
            other
            for other in results
            if other.adapter_name == adapter_name
            and other.pair_id == result.pair_id
            and other.shuffle_index != result.shuffle_index
        ]
        if variants:
            metrics.order_changed = statistics.mean(
                order_sensitivity(result, other) for other in variants
            )
            order_differences.append(metrics.order_changed)
        per_pair.append(metrics)

    if not per_pair:
        return HarnessResult(
            adapter_name=adapter_name,
            pair_count=0,
            macro_precision=0.0,
            macro_recall=0.0,
            macro_f1=0.0,
            median_latency_s=None,
            total_cost_usd=None,
            per_pair=[],
            mean_order_sensitivity=None,
        )

    latencies = [r.latency_s for r in primary if r.latency_s is not None]
    costs = [r.cost_usd for r in primary]

    return HarnessResult(
        adapter_name=adapter_name,
        pair_count=len(per_pair),
        macro_precision=statistics.mean(m.precision for m in per_pair),
        macro_recall=statistics.mean(m.recall for m in per_pair),
        macro_f1=statistics.mean(m.f1 for m in per_pair),
        median_latency_s=statistics.median(latencies) if latencies else None,
        total_cost_usd=(
            sum(cost for cost in costs if cost is not None)
            if costs and all(cost is not None for cost in costs)
            else None
        ),
        per_pair=per_pair,
        mean_order_sensitivity=(
            statistics.mean(order_differences) if order_differences else None
        ),
    )
