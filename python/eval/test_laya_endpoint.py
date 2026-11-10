"""Tests for the standalone endpoint evaluator; no Laya server is required."""

from __future__ import annotations

import pytest

from eval import run_laya_endpoint
from eval.schema import Pair


def test_endpoint_must_be_local() -> None:
    run_laya_endpoint._validate_local_endpoint("http://localhost:8000/v1/systemone")
    run_laya_endpoint._validate_local_endpoint("http://[::1]:8000/v1/systemone")

    with pytest.raises(ValueError, match="loopback"):
        run_laya_endpoint._validate_local_endpoint("http://example.com/v1/systemone")


def test_standalone_evaluator_maps_answers_to_pool_items(
    monkeypatch: pytest.MonkeyPatch,
    simple_pair: Pair,
) -> None:
    def fake_query(
        endpoint: str,
        state: str,
        questions: dict[str, dict[str, str]],
        timeout: float,
        model: str,
    ) -> dict[str, dict[str, dict[str, float]]]:
        assert endpoint == "http://127.0.0.1:8000/v1/systemone"
        assert "Frontend Developer" in state
        assert set(questions) == {"item-01", "item-02"}
        assert timeout > 0
        assert model == "english-local"
        return {
            "answers": {
                "item-01": {"noul": 0.9},
                "item-02": {"noul": 0.1},
            }
        }

    monkeypatch.setattr(run_laya_endpoint, "_query_laya", fake_query)
    result = run_laya_endpoint.evaluate_pair(
        simple_pair,
        "http://127.0.0.1:8000/v1/systemone",
        shuffle_index=0,
        timeout=10.0,
        model="english-local",
    )

    assert result.selected_ids == ["item-01"]
    assert result.cost_usd == 0.0
