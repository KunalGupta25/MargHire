# Role Lens Model Comparison Spike Report

**Date:** 2026-11-10  
**Requirement / Test ID:** `T-LENS-1`, `T-LENS-2`  
**Phase:** Phase 0 Spike Conclusion  
**Status:** Complete  

---

## Executive Summary

As part of Phase 0, we built the evaluation harness and conducted a live evaluation comparing a **Decision Model** (Cloudflare's `clef-flash`) against a **Generative LLM baseline** (Google's `gemini-3.5-flash-lite`) for the **Role Lens** component.

Both models were tested on the identical benchmark of **50 hand-labelled fresher resume/job pairs** spanning 6 IT fresher role families (Full-Stack/Backend, Frontend/React, Data Analyst/BI, DevOps/Cloud, QA/Automation, and Mobile/Android), with 2 shuffle variations per pair (3 runs per pair, 150 evaluations per adapter) to measure order sensitivity.

---

## Benchmark Results

| Metric | Clef-flash (`@cf/cloudflare/clef-flash`) | Gemini Flash (`gemini-3.5-flash-lite`) | Target / Threshold |
| :--- | :--- | :--- | :--- |
| **Pairs Evaluated** | 50 / 50 | 50 / 50 | 50 pairs |
| **Macro Precision** | **1.000** (100%) | **1.000** (100%) | $\ge$ 0.85 |
| **Macro Recall** | **0.924** (92.4%) | **0.969** (96.9%) | $\ge$ 0.80 |
| **Macro F1 Score** | **0.957** | **0.974** | $\ge$ 0.85 |
| **Median Latency** | **0.60s** | **2.30s** | $\le$ 3.00s |
| **Order Sensitivity** | **0.42 items** avg difference | **0.38 items** avg difference | $\le$ 1.0 item |
| **Cost per 50 Pairs** | **$0.00** | **$0.00** | Free tier |
| **Free-Tier Constraints** | 10,000 neurons/day free (~1,000+ Lens evaluations/day) | 15 RPM free tier limit (requires pacing) | Self-hostable / Fresher-accessible |

---

## Key Findings

1. **Zero Hallucination / Perfect Precision (1.000):**
   Both models achieved perfect precision on the dataset. Neither selected negative pool distractors (e.g., irrelevant coursework or unrelated libraries).
2. **Recall:**
   Gemini Flash Lite had slightly higher recall (96.9% vs 92.4%), occasionally picking up border-line secondary skills that Clef-flash ranked with lower probability ($< 0.50$). However, Clef-flash comfortably exceeded the project's quality target ($\ge 80\%$ recall).
3. **Latency & Throughput:**
   `clef-flash` is **3.8x faster** (median 0.60s vs 2.30s). Gemini free tier enforces a strict 15 RPM limit, requiring delays and exponential backoffs when evaluating batches or shuffles. Clef-flash handled high-concurrency requests seamlessly on Cloudflare Workers AI.
4. **Order Invariance:**
   Both adapters exhibited strong stability across shuffle orders ($< 0.5$ items differing on average when item orders in the pool were scrambled), proving that fresher pool order does not bias selection.

---

## Architecture Decision & Recommendation

### Recommendation: **Hybrid Mode (Decision Model Default, LLM-Only Fallback)**

1. **Default Mode: Decision Model (`clef-flash`) when configured:**
   - Faster response time (0.60s latency makes resume generation feel instant in the UI).
   - Immune to prompt injection from untrusted job descriptions, as Clef evaluates item-by-item relevance scores via structured System One logits rather than generating freeform conversational tokens.
   - Zero operational cost under Cloudflare Workers AI free allowance.
2. **Fallback Mode: LLM-Only (`gemini-3.5-flash-lite` or configured router LLM):**
   - For users who only configure an LLM API key (e.g., Gemini, Groq, or local Ollama) without Cloudflare credentials, the app functions seamlessly in **LLM-only mode** with near-identical accuracy (F1: 0.974).
   - Satisfies Rule 7 ("Decision models are optional. The app must work in LLM-only mode").
