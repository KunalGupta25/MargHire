"""Unit tests for eval/loader.py.

All pairs used are synthetic. No personal data.
Test IDs map to Test Plan: loader tests underpin T-LENS-* (Role Lens receives correct input).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from eval.loader import _load_one, load_pairs


def _write_pair(tmp_path: Path, pair_id: str, data: dict) -> Path:  # type: ignore[type-arg]
    path = tmp_path / f"{pair_id}.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


VALID_PAIR = {
    "id": "pair-valid",
    "created_by": "synthetic",
    "created_at": "2026-11-10",
    "job": {"title": "Frontend Developer", "description": "Build React UIs for fintech apps."},
    "pool": [
        {"id": "item-01", "kind": "skill", "text": "React"},
        {"id": "item-02", "kind": "skill", "text": "Django"},
    ],
    "labels": {"item-01": True, "item-02": False},
}


class TestLoadOne:
    def test_valid_pair(self, tmp_path: Path) -> None:
        path = _write_pair(tmp_path, "valid", VALID_PAIR)
        pair = _load_one(path)
        assert pair.id == "pair-valid"
        assert len(pair.pool) == 2
        assert pair.labels["item-01"] is True
        assert pair.positive_ids() == {"item-01"}

    def test_invalid_json(self, tmp_path: Path) -> None:
        path = tmp_path / "bad.json"
        path.write_text("{not valid json", encoding="utf-8")
        with pytest.raises(ValueError, match="Invalid JSON"):
            _load_one(path)

    def test_missing_field(self, tmp_path: Path) -> None:
        broken = {**VALID_PAIR}
        del broken["job"]
        path = _write_pair(tmp_path, "broken", broken)
        with pytest.raises(ValueError, match="Schema error"):
            _load_one(path)

    def test_unlabelled_item(self, tmp_path: Path) -> None:
        bad = {
            **VALID_PAIR,
            "labels": {"item-01": True},  # item-02 is unlabelled
        }
        path = _write_pair(tmp_path, "bad-labels", bad)
        with pytest.raises(ValueError, match="without labels"):
            _load_one(path)

    def test_phantom_label(self, tmp_path: Path) -> None:
        bad = {
            **VALID_PAIR,
            "labels": {"item-01": True, "item-02": False, "item-99": True},
        }
        path = _write_pair(tmp_path, "phantom", bad)
        with pytest.raises(ValueError, match="not in pool"):
            _load_one(path)

    def test_empty_pool_raises(self, tmp_path: Path) -> None:
        bad = {**VALID_PAIR, "pool": [], "labels": {}}
        path = _write_pair(tmp_path, "empty-pool", bad)
        with pytest.raises(ValueError, match="pool is empty"):
            _load_one(path)


class TestLoadPairs:
    def test_loads_valid_pairs(self, tmp_path: Path) -> None:
        for i in range(3):
            data = {
                **VALID_PAIR,
                "id": f"pair-{i:03d}",
                "labels": {"item-01": i % 2 == 0, "item-02": i % 2 != 0},
            }
            _write_pair(tmp_path, f"pair-{i:03d}", data)
        pairs = load_pairs(pairs_dir=tmp_path)
        assert len(pairs) == 3
        assert [p.id for p in pairs] == ["pair-000", "pair-001", "pair-002"]

    def test_missing_directory_raises(self, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError):
            load_pairs(pairs_dir=tmp_path / "nonexistent")

    def test_duplicate_ids_raise(self, tmp_path: Path) -> None:
        pub = tmp_path / "pub"
        priv = tmp_path / "priv"
        pub.mkdir()
        priv.mkdir()
        _write_pair(pub, "dup", VALID_PAIR)
        _write_pair(priv, "dup", VALID_PAIR)
        with pytest.raises(ValueError, match="Duplicate pair id"):
            load_pairs(pairs_dir=pub, private_pairs_dir=priv)

    def test_private_dir_via_env(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        pub = tmp_path / "pub"
        priv = tmp_path / "priv"
        pub.mkdir()
        priv.mkdir()
        _write_pair(pub, "pub-pair", {**VALID_PAIR, "id": "pub-pair"})
        priv_pair = {**VALID_PAIR, "id": "priv-pair"}
        priv_pair["labels"] = {"item-01": False, "item-02": True}
        _write_pair(priv, "priv-pair", priv_pair)

        monkeypatch.setenv("EVAL_PRIVATE_PAIRS_DIR", str(priv))
        pairs = load_pairs(pairs_dir=pub)
        ids = {p.id for p in pairs}
        assert "pub-pair" in ids
        assert "priv-pair" in ids

    def test_empty_directory(self, tmp_path: Path) -> None:
        pairs = load_pairs(pairs_dir=tmp_path)
        assert pairs == []
