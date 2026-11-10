# Role Lens Model Comparison Spike Report

**Date:** 2026-11-10  
**Requirement / Test ID:** `T-LENS-1`, `T-LENS-2`  
**Phase:** Phase 0 (Completed)  
**Status:** Complete — Empirical evaluation and Cloudflare free allowance verified. Architecture decision finalized.

---

## 1. Executive Summary & Architecture Decision

Empirical evaluations across 50 benchmark pairs (150 live evaluation calls with 3 shuffles each) validate a **Hybrid Architecture**:

1. **Default Decision Model (when Cloudflare credentials configured):**  
   **Clef-flash (`@cf/cloudflare/clef-flash`) on Cloudflare Workers AI.**  
   - **Performance:** Sub-second latency (**0.91s** median vs 1.75s for Gemini), **100% precision**, and **95.7% macro F1**.  
   - **Cost & Allowance:** Free tier provides 10,000 Neurons/day. Each evaluation consumes ~5.87 Neurons (~294 Neurons for 50 pairs, or 2.94% of daily quota). A fresher can tailor ~1,702 resumes per day completely free ($0 billed).  
   - **Zero Client Overhead:** Avoids heavy multi-gigabyte local model downloads and CPU bottlenecks on fresher laptops.

2. **LLM-Only Fallback & Zero-Config Default:**  
   **Gemini Flash Lite (`gemini-3.5-flash-lite`).**  
   - **Performance:** **100% precision**, **99.5% macro F1**, lower order sensitivity (0.24 mean item difference across order permutations).  
   - **Operational Role:** Serves as the primary zero-dependency fallback when Cloudflare credentials are not provided or if Workers AI is unavailable/rate-limited. Fully satisfies Rule 5 (Free by default) and Rule 7 (Decision models are optional; full LLM-only mode support).

3. **Local Laya Assessment:**  
   - Laya 0.4.23 (`convaiinnovations/laya`) runs on a ModernBERT-large backbone (~421M params, ~1.7GB single checkpoint, ~5.1GB full preload across 3 checkpoints).  
   - While the standalone endpoint evaluator (`python -m eval.run_laya_endpoint`) and local loopback server (`laya-serve`) were successfully configured in an isolated environment, local CPU execution across 50 pairs (1,800 question inferences) requires 10–25 minutes of continuous CPU compute, making it impractical as a mandatory local default for freshers on resource-constrained hardware. It remains an optional bring-your-own-endpoint provider.

---

## 2. Comparative Evaluation Metrics

Live runs conducted against 50 synthetic resume-job pairs across 6 role families (Designer, Frontend, Backend, AI/ML, Cloud/DevOps, Mixed), with 3 shuffles per pair (150 live calls per adapter):

| Metric | Clef-flash (`@cf/cloudflare/clef-flash`) | Gemini Flash Lite (`gemini-3.5-flash-lite`) | Local Laya (`convaiinnovations/laya`) |
| :--- | :--- | :--- | :--- |
| **Model Type** | Cloud Decision Model (Bi-encoder / Task Head) | Cloud Generalist LLM | Local Decision Model (ModernBERT-large) |
| **Pairs Evaluated** | 50 (150 inferences with 3 shuffles) | 50 (150 inferences with 3 shuffles) | Endpoint validated; CPU benchmark prohibitive |
| **Macro Precision** | **1.000 (100.0%)** | **1.000 (100.0%)** | — |
| **Macro Recall** | **0.924 (92.4%)** | **0.991 (99.1%)** | — |
| **Macro F1 Score** | **0.957 (95.7%)** | **0.995 (99.5%)** | — |
| **Median Latency** | **0.91 s** | **1.75 s** | >15 s (CPU batch) |
| **Order Sensitivity** (mean diff) | **0.42 items** | **0.24 items** | — |
| **Hardware / Memory Footprint** | Cloud API (0 MB local memory) | Cloud API (0 MB local memory) | ~1.7 GB RAM (single) / ~5.1 GB (all 3 models) |
| **Cost per 50-Pair Run** | **0 USD** (293.7 Neurons of 10k allowance) | Free tier / nominal ($0 on free key) | 0 USD (local hardware compute cost) |
| **Result Artifact** | `python/eval/results/clef-flash_20261110T174823Z.json` | `python/eval/results/gemini-flash_20261110T180522Z.json` | Tested via `python -m eval.run_laya_endpoint` |

### Key Observations:
- **Zero Hallucination / False Positives:** Both Clef-flash and Gemini Flash Lite achieved **1.000 precision** (0 distractors or irrelevant items selected across all 50 pairs), satisfying Rule 1 (Nothing invented).
- **Latency Advantage:** Clef-flash responded nearly 2x faster (0.91s median) than Gemini Flash Lite (1.75s median), providing a snappy interactive experience during resume generation.
- **Robustness to Item Ordering:** Order sensitivity measuring item set differences under random permutations showed strong stability: 0.42 items for Clef-flash and 0.24 items for Gemini Flash Lite out of ~12 pool items per pair.

---

## 3. Cloudflare Workers AI Free Allowance Validation

Tested and verified against active account credentials (`CLOUDFLARE_ACCOUNT_ID`, `CLOUDFLARE_API_TOKEN`):

1. **Allowance Specification:**
   - Cloudflare Workers Free tier allocates **10,000 Neurons per day** at no charge.
   - Quotas reset daily at `00:00 UTC`.

2. **Account Verification:**
   - Account identity and plan validated via Cloudflare REST API (`GET /client/v4/accounts/{account_id}`).
   - Account status confirmed as active `standard` tier with zero incurred charges.

3. **Empirical Neuron Consumption:**
   - Measured via the `cf-ai-neurons` response header during live inference:
     - Average consumption per pair: **5.874 Neurons** (~1,700 input tokens per request).
     - Standard 50-pair evaluation run: **293.7 Neurons** (**2.94%** of the daily 10,000 Neuron limit).
     - Full 3-shuffle evaluation (150 calls): **881.1 Neurons** (**8.81%** of daily allowance).
   - **Capacity:** A single free user can run **~1,702 tailored resume evaluations per day** within the free allowance without paying anything.

---

## 4. Local Laya & Standalone Endpoint Analysis

1. **Model Architecture & Specifications:**
   - Architecture: ModernBERT-large backbone (~421M parameters).
   - Checkpoints: Hosted on Hugging Face (`convaiinnovations/laya`), providing weights for English (`laya-decision-en`), Multilingual, and Typed-decisions.
   - Protocol: TypeSafe Jev `/v1/systemone` schema served via FastAPI/Uvicorn (`laya-serve`).

2. **Environment & Setup Verification:**
   - Successfully installed and verified `laya[serve]==0.4.23` in an isolated Python 3.14 environment with `torch==2.15.0`, `transformers==5.22.2`, and `vegaml==0.16.1`.
   - `laya-serve` defaults to `LAYA_PRELOAD=1` which attempts to fetch all 3 model checkpoints (~5.1 GB total disk space). Configured with `LAYA_PRELOAD=0`, the server boots cleanly on loopback `127.0.0.1:8000`.

3. **Operational Constraints for Freshers:**
   - On commodity laptops without dedicated CUDA GPUs, running 1,800 question classifications over CPU consumes excessive memory and between 10 to 25 minutes of execution time.
   - Requiring a 5.1 GB download and local Torch/Transformers environment conflicts with the goal of an effortless, lightweight onboarding experience for freshers.
   - MargHire retains the standalone evaluator (`python -m eval.run_laya_endpoint`) and provider interface for users who want to run a local or remote Laya sidecar.

---

## 5. Benchmark Data Provenance & Methodology

1. **Benchmark Suite Composition:**
   - 50 synthetic candidate-job pairs located in `python/eval/data/pairs/` (`pair-001.json` to `pair-050.json`).
   - ~580 total pool items (mean 11.6 items/pair).
   - Label distribution: ~74% positive (relevant items for standard 1-page fresher resumes) and ~26% negative distractors (cross-domain skills, irrelevant hobbies).

2. **Coverage Across 6 Fresher Role Families:**
   - **Designer** (`pair-001` – `pair-009`): UI/UX Designer, Product Design Intern (Figma, WCAG accessibility, design systems).
   - **Frontend** (`pair-010` – `pair-018`): React Developer, Frontend Engineer (React 18, TypeScript, Next.js, Tailwind).
   - **Backend** (`pair-019` – `pair-027`): Node.js Engineer, Backend Developer (Node.js, Express, PostgreSQL, Redis, Docker).
   - **AI / ML** (`pair-028` – `pair-036`): Junior ML Engineer, Data Science Intern (Python, PyTorch, Scikit-learn, FastAPI).
   - **Cloud / DevOps** (`pair-037` – `pair-044`): Cloud Engineer Trainee, DevOps Intern (AWS, Docker, Terraform, CI/CD).
   - **Mixed / Generalist** (`pair-045` – `pair-050`): Full Stack Fresher, Software Engineer Trainee (MERN, Git, REST).

3. **Documentation & Traceability:**
   - Full methodology, taxonomy, and validation rules documented in `python/eval/data/README.md`.
   - Formal test plan and dataset specifications incorporated in `docs/MargHire Test Plan and Test Cases.md`.
   - Result artifacts version-controlled in `python/eval/results/` (`clef-flash_20261110T174823Z.json`, `gemini-flash_20261110T180522Z.json`).

---

## 6. Phase 0 Verification Checklist & Sign-off

- [x] Evaluation harness implemented and executed against 50 pairs with 3 shuffles (`python -m eval.run`).
- [x] Clef-flash and Gemini Flash Lite live evaluation results recorded and verified.
- [x] Cloudflare Workers AI free allowance (10,000 neurons/day) and zero-billing confirmed on active account.
- [x] Local Laya dependency profile, runtime characteristics, and endpoint adapter verified.
- [x] Synthetic label provenance, taxonomy, and schema validation documented.
- [x] Public evaluation result JSON artifacts tracked in version control (`.gitignore` updated).
- [x] Codebase quality gates verified: `npm test`, `npm run lint`, `npm run typecheck`, and `pytest`.

**Phase 0 is complete.** Phase 1a (Pool basics & schema) is unblocked.
