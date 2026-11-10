"""Cloudflare Workers AI Clef / Clef-flash adapter.

Evaluates resume candidate pool items against a job description using
Cloudflare's native System One decision model (@cf/cloudflare/clef or clef-flash).
"""

from __future__ import annotations

import json
import os
import time
import urllib.request
from pathlib import Path

from ..schema import AdapterResult, Pair
from .base import Adapter


def _load_cloudflare_creds() -> tuple[str, str]:
    account_id = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "").strip()
    api_token = os.environ.get("CLOUDFLARE_API_TOKEN", "").strip()

    if not account_id or not api_token:
        # Check .env file at repo root
        root_env = Path(__file__).resolve().parents[3] / ".env"
        if root_env.exists():
            for line in root_env.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip()
                if k == "CLOUDFLARE_ACCOUNT_ID" and not account_id:
                    account_id = v
                elif k == "CLOUDFLARE_API_TOKEN" and not api_token:
                    api_token = v

    return account_id, api_token


class ClefAdapter(Adapter):
    """Adapter for Cloudflare Workers AI Clef & Clef-flash decision models."""

    def __init__(self, flash: bool = True, threshold: float = 0.5) -> None:
        self._flash = flash
        self._threshold = threshold
        self._account_id, self._api_token = _load_cloudflare_creds()

    @property
    def name(self) -> str:
        return "clef-flash" if self._flash else "clef"

    def select(self, pair: Pair, shuffle_index: int = 0) -> AdapterResult:
        if not self._account_id or not self._api_token:
            raise ValueError(
                "CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_API_TOKEN must be configured in .env"
            )

        item_order = self._shuffled_pool(pair, shuffle_index)
        pool_dict = {item.id: item for item in pair.pool}

        model_name = "clef-flash" if self._flash else "clef"
        cf_model_path = f"@cf/cloudflare/{model_name}"

        # Clef questions format: noul (yes/no probability)
        questions = {
            item_id: {
                "type": "noul",
                "instructions": (
                    f"Should this item be included on a tailored resume for this job?\n"
                    f"Item ({pool_dict[item_id].kind}): {pool_dict[item_id].text}"
                ),
            }
            for item_id in item_order
        }

        body = {
            "model": model_name,
            "state": f"Job Title: {pair.job.title}\nJob Description:\n{pair.job.description}",
            "questions": questions,
        }

        url = f"https://api.cloudflare.com/client/v4/accounts/{self._account_id}/ai/run/{cf_model_path}"
        data = json.dumps(body).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "Authorization": f"Bearer {self._api_token}",
                "Content-Type": "application/json",
            },
        )

        start_time = time.perf_counter()
        # Retries with backoff for rate limits / network hiccups
        max_retries = 3
        last_error: Exception | None = None
        for attempt in range(max_retries):
            try:
                with urllib.request.urlopen(req, timeout=30) as resp:
                    resp_data = json.loads(resp.read().decode("utf-8"))
                    break
            except Exception as e:
                last_error = e
                time.sleep(1.5 * (attempt + 1))
        else:
            raise RuntimeError(
                f"Cloudflare Workers AI request failed after {max_retries} attempts: {last_error}"
            )

        latency = time.perf_counter() - start_time

        result = resp_data.get("result", {})
        answers = result.get("answers", {})

        selected: list[str] = []
        for item_id in item_order:
            ans = answers.get(item_id, {})
            score = ans.get("noul", 0.0)
            if score >= self._threshold:
                selected.append(item_id)

        return AdapterResult(
            pair_id=pair.id,
            adapter_name=self.name,
            selected_ids=selected,
            latency_s=latency,
            cost_usd=0.0,  # Free within daily 10,000 Neurons allowance
            shuffle_index=shuffle_index,
        )
