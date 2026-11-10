# Role Lens Model Comparison Spike Report

**Date:** 2026-11-10
**Requirement / Test ID:** `T-LENS-1`, `T-LENS-2`
**Phase:** Phase 0
**Status:** Incomplete; the standalone Laya endpoint evaluator is implemented, but no Laya inference results or account-level allowance evidence are recorded.

## What is implemented

- The evaluation harness loads 50 synthetic resume/job pairs from `python/eval/data/pairs/`.
- Clef and Gemini adapters make provider calls. Laya and the generic LLM adapter are stubs in the main harness.
- The harness records per-pair precision, recall, F1, and order sensitivity in its JSON output. With multiple shuffles, order sensitivity compares the primary run with each additional shuffle and averages the differences.
- Gemini credentials are sent in the `x-goog-api-key` request header, not in the URL.
- Docker Compose defaults to SQLite stored in the `marghire_data` volume.

## Cloudflare documentation check

Checked 2026-11-10: Cloudflare's [Workers AI pricing page](https://developers.cloudflare.com/workers-ai/platform/pricing/) lists 10,000 Neurons per day at no charge on Workers Free, with daily limits resetting at 00:00 UTC. The [Clef model page](https://developers.cloudflare.com/workers-ai/models/clef/) and [Clef-flash model page](https://developers.cloudflare.com/workers-ai/models/clef-flash/) list model-specific input-token prices. This documents the published plan terms; it does not establish the account's current eligibility, remaining allowance, or the cost of this benchmark run.

## What remains open

The previous version of this report included live model metrics, free-tier limits, and a recommendation. The source-controlled evidence does not include a reproducible set of provider outputs, and the benchmark records synthetic origin/date but no individual human labeler. Treat those earlier numbers and conclusions as unverified until a fresh run is saved with the inputs, adapter/model identifiers, shuffle count, timestamp, measured latency, and cost evidence.

Phase 0 still needs:

1. Add labeler provenance for the labels, or explicitly define a documented synthetic-labeling method and review it.
2. Run Laya, Clef or Clef-flash, and a selected live LLM against the same 50 pairs. Laya 0.4.23 and its public checkpoint were installed/downloaded in task scratch, but the sandboxed inference run could not start: Docker's metadata store became read-only during transfer into its offline Linux volume. No Laya metrics or result files were produced.
3. Save each run's JSON output in version control and record exact provider/model IDs. The harness leaves cost unknown unless measured separately.
4. Verify allowance availability and actual consumption in the intended Cloudflare account. Public pricing terms are documented above, but account-level eligibility and benchmark cost are not measured.
5. Recheck lint, type-check, tests, Compose startup, and CI, then record the resulting evidence.

No default-mode recommendation is made until these checks are complete. Phase 0 remains open.
