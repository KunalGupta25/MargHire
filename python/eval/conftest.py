"""Shared pytest fixtures for the eval harness tests."""

from __future__ import annotations

import pytest

from eval.schema import Job, Pair, PoolItem


def make_pair(
    pair_id: str = "pair-test",
    pool_items: list[tuple[str, str]] | None = None,
    labels: dict[str, bool] | None = None,
    job_title: str = "Frontend Developer",
    job_desc: str = "Build React UIs.",
) -> Pair:
    """Build a minimal Pair for use in tests. All data is synthetic."""
    if pool_items is None:
        pool_items = [("item-01", "React"), ("item-02", "Django")]
    if labels is None:
        labels = {item_id: i == 0 for i, (item_id, _) in enumerate(pool_items)}

    return Pair(
        id=pair_id,
        created_by="test",
        created_at="2026-11-10",
        job=Job(title=job_title, description=job_desc),
        pool=[
            PoolItem(id=item_id, kind="skill", text=text)
            for item_id, text in pool_items
        ],
        labels=labels,
    )


@pytest.fixture()
def simple_pair() -> Pair:
    return make_pair()


@pytest.fixture()
def all_positive_pair() -> Pair:
    items = [("a", "React"), ("b", "TypeScript")]
    return make_pair(pool_items=items, labels={"a": True, "b": True})


@pytest.fixture()
def all_negative_pair() -> Pair:
    items = [("a", "React"), ("b", "TypeScript")]
    return make_pair(pool_items=items, labels={"a": False, "b": False})
