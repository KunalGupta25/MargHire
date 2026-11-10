"""Evaluate Laya through a separately installed local laya-serve endpoint.

Start laya-serve in its own environment with LAYA_HOST=127.0.0.1, then run:
    python -m eval.run_laya_endpoint --shuffles 3 --output results/
"""

from __future__ import annotations

import argparse
import dataclasses
import http.client
import ipaddress
import json
import os
import random
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from .loader import load_pairs
from .metrics import aggregate
from .schema import AdapterResult, Pair

MODEL_ID = "convaiinnovations/laya (english)"
ADAPTER_NAME = "laya-standalone"
DEFAULT_ENDPOINT = "http://127.0.0.1:8000/v1/systemone"


def _validate_local_endpoint(endpoint: str) -> None:
    parsed = urlparse(endpoint)
    if parsed.scheme != "http" or not parsed.hostname:
        raise ValueError("Laya endpoint must be an http URL on localhost")
    if parsed.username or parsed.password:
        raise ValueError("Do not put credentials in the endpoint URL")
    if parsed.query or parsed.fragment:
        raise ValueError("Laya endpoint must not include a query or fragment")
    hostname = parsed.hostname.lower()
    if hostname == "localhost":
        return
    try:
        if ipaddress.ip_address(hostname).is_loopback:
            return
    except ValueError:
        pass
    raise ValueError("Laya endpoint must use localhost or a loopback IP address")


def _query_laya(
    endpoint: str,
    state: str,
    questions: dict[str, dict[str, str]],
    timeout: float,
    model: str,
) -> dict[str, Any]:
    _validate_local_endpoint(endpoint)
    parsed = urlparse(endpoint)
    if parsed.hostname is None:
        raise ValueError("Laya endpoint must name a loopback host")
    payload = json.dumps(
        {"state": state, "questions": questions, "model": model}
    ).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    api_key = os.environ.get("LAYA_API_KEY", "").strip()
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    connection = http.client.HTTPConnection(
        parsed.hostname,
        port=parsed.port or 80,
        timeout=timeout,
    )
    try:
        connection.request("POST", parsed.path or "/", body=payload, headers=headers)
        response = connection.getresponse()
        if response.status < 200 or response.status >= 300:
            raise RuntimeError(f"Laya endpoint returned HTTP {response.status}")
        result = json.loads(response.read().decode("utf-8"))
    except (http.client.HTTPException, OSError) as exc:
        raise RuntimeError("Could not reach the local Laya endpoint") from exc
    finally:
        connection.close()
    if not isinstance(result, dict) or not isinstance(result.get("answers"), dict):
        raise RuntimeError("Laya endpoint returned an invalid response")
    return result


def evaluate_pair(
    pair: Pair,
    endpoint: str,
    shuffle_index: int,
    timeout: float,
    model: str = "english",
    threshold: float = 0.5,
) -> AdapterResult:
    ids = [item.id for item in pair.pool]
    random.Random(f"{pair.id}:{shuffle_index}").shuffle(ids)
    items = {item.id: item for item in pair.pool}
    questions = {
        item_id: {
            "type": "noul",
            "instructions": (
                "Should this item be included on a tailored resume for this job? "
                f"Item ({items[item_id].kind}): {items[item_id].text}"
            ),
        }
        for item_id in ids
    }
    state = f"Job Title: {pair.job.title}\nJob Description:\n{pair.job.description}"

    started = time.perf_counter()
    response = _query_laya(endpoint, state, questions, timeout, model)
    latency = time.perf_counter() - started
    answers = response["answers"]
    selected = [
        item_id
        for item_id in ids
        if answers.get(item_id, {}).get("noul", 0.0) >= threshold
    ]
    return AdapterResult(
        pair_id=pair.id,
        adapter_name=ADAPTER_NAME,
        selected_ids=selected,
        latency_s=latency,
        cost_usd=0.0,
        shuffle_index=shuffle_index,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Evaluate local Laya through laya-serve.")
    parser.add_argument("--endpoint", default=DEFAULT_ENDPOINT)
    parser.add_argument("--shuffles", type=int, default=3)
    parser.add_argument("--timeout", type=float, default=600.0)
    parser.add_argument("--model", default="english", help="model name served by Laya")
    parser.add_argument("--output", type=Path, default=Path(__file__).parent / "results")
    parser.add_argument("--pairs-dir", type=Path, default=None)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.shuffles < 1:
        parser.error("--shuffles must be at least 1")
    if args.timeout <= 0:
        parser.error("--timeout must be greater than zero")
    try:
        _validate_local_endpoint(args.endpoint)
    except ValueError as exc:
        parser.error(str(exc))

    pairs = load_pairs(pairs_dir=args.pairs_dir)
    all_results: list[AdapterResult] = []
    for pair in pairs:
        for shuffle_index in range(args.shuffles):
            all_results.append(
                evaluate_pair(pair, args.endpoint, shuffle_index, args.timeout, args.model)
            )

    summary = aggregate(pairs, all_results, ADAPTER_NAME)
    run_at = datetime.now(UTC)
    args.output.mkdir(parents=True, exist_ok=True)
    output_path = args.output / f"{ADAPTER_NAME}_{run_at:%Y%m%dT%H%M%SZ}.json"
    output_path.write_text(
        json.dumps(
            {
                "run_at_utc": run_at.isoformat(),
                "adapter": ADAPTER_NAME,
                "model_id": MODEL_ID,
                "served_model": args.model,
                "shuffle_count": args.shuffles,
                "provider_cost_usd": 0.0,
                "cost_note": "Local inference; electricity and hardware costs are excluded.",
                "metrics": dataclasses.asdict(summary),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Evaluated {summary.pair_count} pairs with {MODEL_ID}.")
    print(f"Results written to {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
