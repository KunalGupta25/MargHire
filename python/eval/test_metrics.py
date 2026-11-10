"""Unit tests for eval/metrics.py.

All inputs are synthetic. No model calls are made.
Test IDs map to Test Plan:
  - test_precision_* -> T-LENS-1 (Role Lens selects correctly)
  - test_recall_*    -> T-LENS-2 (Role Lens differentiates jobs)
"""

from __future__ import annotations

import pytest

from eval.metrics import aggregate, f1, order_sensitivity, pair_metrics, precision, recall
from eval.schema import AdapterResult, Pair


class TestPrecision:
    def test_all_correct(self) -> None:
        assert precision({"a", "b"}, {"a", "b"}) == 1.0

    def test_all_wrong(self) -> None:
        assert precision({"c", "d"}, {"a", "b"}) == 0.0

    def test_partial(self) -> None:
        assert precision({"a", "b"}, {"a"}) == pytest.approx(0.5)

    def test_empty_selected(self) -> None:
        # No false positives when nothing is selected
        assert precision(set(), {"a"}) == 1.0

    def test_empty_positive(self) -> None:
        # Selecting items when nothing should be selected = 0 precision
        assert precision({"a"}, set()) == 0.0


class TestRecall:
    def test_all_recalled(self) -> None:
        assert recall({"a", "b"}, {"a", "b"}) == 1.0

    def test_none_recalled(self) -> None:
        assert recall(set(), {"a", "b"}) == 0.0

    def test_partial(self) -> None:
        assert recall({"a"}, {"a", "b"}) == pytest.approx(0.5)

    def test_empty_positive(self) -> None:
        # Nothing to recall = perfect recall
        assert recall({"a"}, set()) == 1.0


class TestF1:
    def test_perfect(self) -> None:
        assert f1(1.0, 1.0) == 1.0

    def test_zero(self) -> None:
        assert f1(0.0, 0.0) == 0.0

    def test_harmonic(self) -> None:
        assert f1(1.0, 0.5) == pytest.approx(2 / 3)


class TestOrderSensitivity:
    def _result(self, selected: list[str], shuffle: int = 0) -> AdapterResult:
        return AdapterResult(
            pair_id="pair-001",
            adapter_name="test",
            selected_ids=selected,
            shuffle_index=shuffle,
        )

    def test_identical(self) -> None:
        a = self._result(["x", "y"], 0)
        b = self._result(["x", "y"], 1)
        assert order_sensitivity(a, b) == 0

    def test_fully_different(self) -> None:
        a = self._result(["x", "y"], 0)
        b = self._result(["a", "b"], 1)
        assert order_sensitivity(a, b) == 4

    def test_partial(self) -> None:
        a = self._result(["x", "y"], 0)
        b = self._result(["x", "z"], 1)
        assert order_sensitivity(a, b) == 2

    def test_different_pairs_raises(self) -> None:
        a = AdapterResult(pair_id="pair-001", adapter_name="t", selected_ids=[])
        b = AdapterResult(pair_id="pair-002", adapter_name="t", selected_ids=[])
        with pytest.raises(ValueError, match="different pairs"):
            order_sensitivity(a, b)


class TestPairMetrics:
    def test_perfect_selection(self, all_positive_pair: Pair) -> None:
        result = AdapterResult(
            pair_id=all_positive_pair.id,
            adapter_name="test",
            selected_ids=["a", "b"],
        )
        metrics = pair_metrics(all_positive_pair, result)
        assert metrics.precision == 1.0
        assert metrics.recall == 1.0
        assert metrics.f1 == 1.0

    def test_empty_selection_all_positive(self, all_positive_pair: Pair) -> None:
        result = AdapterResult(
            pair_id=all_positive_pair.id,
            adapter_name="test",
            selected_ids=[],
        )
        metrics = pair_metrics(all_positive_pair, result)
        assert metrics.precision == 1.0  # No false positives
        assert metrics.recall == 0.0     # Missed everything

    def test_empty_selection_all_negative(self, all_negative_pair: Pair) -> None:
        result = AdapterResult(
            pair_id=all_negative_pair.id,
            adapter_name="test",
            selected_ids=[],
        )
        metrics = pair_metrics(all_negative_pair, result)
        assert metrics.precision == 1.0
        assert metrics.recall == 1.0  # Nothing to recall


class TestAggregate:
    def test_empty_results(self, simple_pair: Pair) -> None:
        summary = aggregate([simple_pair], [], "test-adapter")
        assert summary.pair_count == 0
        assert summary.macro_precision == 0.0
        assert summary.macro_recall == 0.0

    def test_single_pair(self, all_positive_pair: Pair) -> None:
        result = AdapterResult(
            pair_id=all_positive_pair.id,
            adapter_name="my-adapter",
            selected_ids=["a", "b"],
        )
        summary = aggregate([all_positive_pair], [result], "my-adapter")
        assert summary.pair_count == 1
        assert summary.macro_precision == pytest.approx(1.0)
        assert summary.macro_recall == pytest.approx(1.0)
        assert summary.macro_f1 == pytest.approx(1.0)

    def test_ignores_other_adapters(self, all_positive_pair: Pair) -> None:
        result = AdapterResult(
            pair_id=all_positive_pair.id,
            adapter_name="other-adapter",
            selected_ids=["a"],
        )
        summary = aggregate([all_positive_pair], [result], "my-adapter")
        assert summary.pair_count == 0

    def test_ignores_non_primary_shuffles(self, all_positive_pair: Pair) -> None:
        # shuffle_index == 0 is the primary run; others are for order sensitivity only
        results = [
            AdapterResult(
                pair_id=all_positive_pair.id,
                adapter_name="adp",
                selected_ids=["a"],
                shuffle_index=0,
            ),
            AdapterResult(
                pair_id=all_positive_pair.id,
                adapter_name="adp",
                selected_ids=["b"],
                shuffle_index=1,
            ),
        ]
        summary = aggregate([all_positive_pair], results, "adp")
        assert summary.pair_count == 1
