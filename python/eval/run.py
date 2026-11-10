"""CLI entry point for the evaluation harness.

Usage:
    python -m eval.run --adapter llm-stub --output results/
    python -m eval.run --adapter laya-stub --shuffles 3
    python -m eval.run --help

Real provider adapters are available for Clef and Gemini. Laya and the generic
LLM adapters remain stubs until their runtimes are selected and configured.
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

from .adapters.clef import ClefAdapter
from .adapters.gemini import GeminiAdapter
from .adapters.laya import LayaAdapter
from .adapters.llm import LLMAdapter
from .loader import load_pairs
from .metrics import aggregate
from .schema import AdapterResult

ADAPTERS = {
    "llm-stub": LLMAdapter(),
    "laya-stub": LayaAdapter(),
    "clef-stub": ClefAdapter(flash=False),
    "clef-flash-stub": ClefAdapter(flash=True),
    "clef-flash": ClefAdapter(flash=True),
    "clef": ClefAdapter(flash=False),
    "gemini-flash": GeminiAdapter(),
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the MargHire Role Lens evaluation harness.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--adapter",
        choices=list(ADAPTERS.keys()),
        default="llm-stub",
        help="Which adapter to run (default: llm-stub).",
    )
    parser.add_argument(
        "--shuffles",
        type=int,
        default=1,
        help="Number of shuffle runs per pair for order-sensitivity measurement (default: 1).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).parent / "results",
        help="Directory to write results JSON (default: eval/results/).",
    )
    parser.add_argument(
        "--pairs-dir",
        type=Path,
        default=None,
        help="Override the synthetic pairs directory.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.shuffles < 1:
        parser.error("--shuffles must be at least 1")

    print("Loading pairs...")
    pairs = load_pairs(pairs_dir=args.pairs_dir)
    print(f"  {len(pairs)} pairs loaded.")

    adapter = ADAPTERS[args.adapter]
    all_results: list[AdapterResult] = []

    print(f"Running adapter '{adapter.name}' with {args.shuffles} shuffle(s) per pair...")
    for idx, pair in enumerate(pairs, 1):
        for shuffle_index in range(args.shuffles):
            result = adapter.select(pair, shuffle_index=shuffle_index)
            all_results.append(result)
        if idx % 10 == 0 or idx == len(pairs):
            print(f"  Processed {idx}/{len(pairs)} pairs...", flush=True)

    summary = aggregate(pairs, all_results, adapter.name)

    print(f"\nResults for {adapter.name}:")
    print(f"  Pairs evaluated : {summary.pair_count}")
    print(f"  Macro precision : {summary.macro_precision:.3f}")
    print(f"  Macro recall    : {summary.macro_recall:.3f}")
    print(f"  Macro F1        : {summary.macro_f1:.3f}")
    if summary.median_latency_s is not None:
        print(f"  Median latency  : {summary.median_latency_s:.2f}s")
    if summary.mean_order_sensitivity is not None:
        print(f"  Order sensitivity (mean item diff) : {summary.mean_order_sensitivity:.2f}")
    if summary.total_cost_usd is not None:
        print(f"  Total cost      : ${summary.total_cost_usd:.4f}")

    args.output.mkdir(parents=True, exist_ok=True)
    run_at = datetime.now(UTC)
    ts = run_at.strftime("%Y%m%dT%H%M%SZ")
    out_path = args.output / f"{adapter.name}_{ts}.json"
    out_path.write_text(
        json.dumps(
            {
                "run_at_utc": run_at.isoformat(),
                "adapter": adapter.name,
                "model_id": adapter.model_id,
                "shuffle_count": args.shuffles,
                "metrics": dataclasses.asdict(summary),
            },
            indent=2,
            default=str,
        ),
        encoding="utf-8",
    )
    print(f"\nFull results written to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
