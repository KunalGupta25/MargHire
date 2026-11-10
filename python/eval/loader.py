"""Load evaluation pairs from JSON files.

Public pairs live in eval/data/pairs/*.json (committed to the repo, synthetic data only).
Private pairs come from EVAL_PRIVATE_PAIRS_DIR in the environment (outside the repo).
Both sets are merged; duplicates on pair id raise an error.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from .schema import Job, Pair, PoolItem

# Default location for the synthetic pairs bundled with the repo
_DEFAULT_PAIRS_DIR = Path(__file__).parent / "data" / "pairs"


def load_pairs(
    pairs_dir: Path | None = None,
    private_pairs_dir: Path | None = None,
) -> list[Pair]:
    """Load and validate all pairs from both public and private directories.

    Args:
        pairs_dir: Directory of synthetic pair JSON files. Defaults to eval/data/pairs/.
        private_pairs_dir: Directory of private pair JSON files. Falls back to the
            EVAL_PRIVATE_PAIRS_DIR environment variable.

    Returns:
        List of validated Pair objects, sorted by id.

    Raises:
        ValueError: If any pair fails validation or if two pairs share the same id.
        FileNotFoundError: If the specified pairs_dir does not exist.
    """
    public_dir = pairs_dir or _DEFAULT_PAIRS_DIR
    if not public_dir.exists():
        raise FileNotFoundError(f"Pairs directory not found: {public_dir}")

    private_dir: Path | None = private_pairs_dir
    if private_dir is None:
        env_path = os.getenv("EVAL_PRIVATE_PAIRS_DIR")
        if env_path:
            private_dir = Path(env_path)

    pairs: dict[str, Pair] = {}

    for source_dir in [d for d in [public_dir, private_dir] if d is not None]:
        if not source_dir.exists():
            continue
        for path in sorted(source_dir.glob("*.json")):
            pair = _load_one(path)
            if pair.id in pairs:
                raise ValueError(
                    f"Duplicate pair id '{pair.id}' found in {path} "
                    f"(already loaded from another file)"
                )
            pairs[pair.id] = pair

    return sorted(pairs.values(), key=lambda p: p.id)


def _load_one(path: Path) -> Pair:
    """Parse and validate one pair JSON file."""
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path}: {exc}") from exc

    try:
        pair = _parse(raw, path)
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(f"Schema error in {path}: {exc}") from exc

    errors = pair.validate()
    if errors:
        raise ValueError(f"Validation errors in {path}:\n" + "\n".join(f"  - {e}" for e in errors))

    return pair


def _parse(raw: object, path: Path) -> Pair:
    """Convert a raw JSON object to a Pair. Raises KeyError/TypeError on bad shape."""
    if not isinstance(raw, dict):
        raise TypeError(f"Expected a JSON object, got {type(raw).__name__}")

    job_raw = raw["job"]
    pool_raw = raw["pool"]
    labels_raw = raw["labels"]

    if not isinstance(labels_raw, dict):
        raise TypeError("labels must be a JSON object mapping item id to bool")

    return Pair(
        id=str(raw["id"]),
        created_by=str(raw.get("created_by", "unknown")),
        created_at=str(raw.get("created_at", "")),
        job=Job(
            title=str(job_raw["title"]),
            description=str(job_raw["description"]),
        ),
        pool=[
            PoolItem(
                id=str(item["id"]),
                kind=item["kind"],
                text=str(item["text"]),
                tags=list(item.get("tags", [])),
            )
            for item in pool_raw
        ],
        labels={str(k): bool(v) for k, v in labels_raw.items()},
    )
