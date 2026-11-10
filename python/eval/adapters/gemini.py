"""Google Gemini LLM adapter for Role Lens evaluation.

Uses the Gemini REST API to select relevant pool items for a given job.
"""

from __future__ import annotations

import json
import os
import re
import time
import urllib.request
from pathlib import Path

from ..schema import AdapterResult, Pair
from .base import Adapter


def _load_gemini_key() -> str:
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        root_env = Path(__file__).resolve().parents[3] / ".env"
        if root_env.exists():
            for line in root_env.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                if k.strip() == "GEMINI_API_KEY":
                    key = v.strip()
                    break
    return key


class GeminiAdapter(Adapter):
    """Adapter calling Gemini 3.5 Flash Lite for Role Lens candidate selection."""

    def __init__(self, model: str = "gemini-3.5-flash-lite") -> None:
        self._model = model
        self._api_key = _load_gemini_key()

    @property
    def name(self) -> str:
        return "gemini-flash"

    @property
    def model_id(self) -> str:
        return self._model

    def select(self, pair: Pair, shuffle_index: int = 0) -> AdapterResult:
        if not self._api_key:
            raise ValueError("GEMINI_API_KEY must be configured in .env or environment")

        item_order = self._shuffled_pool(pair, shuffle_index)
        pool_dict = {item.id: item for item in pair.pool}

        formatted_items = "\n".join(
            f"- [{item_id}] ({pool_dict[item_id].kind}): {pool_dict[item_id].text}"
            for item_id in item_order
        )

        prompt = (
            "You are an expert technical resume tailoring evaluator.\n"
            "Given the Job Title, Job Description, and candidate pool items, "
            "evaluate which items should appear on a tailored resume for this job.\n"
            "A fresher applicant's resume must highlight relevant items matching the role, "
            "while excluding completely unrelated items.\n\n"
            f"Job Title: {pair.job.title}\n"
            f"Job Description:\n{pair.job.description}\n\n"
            "Candidate Pool Items:\n"
            f"{formatted_items}\n\n"
            "Return ONLY a valid JSON array of strings containing the selected item IDs.\n"
            "Example output: [\"item-001-01\", \"item-001-03\"]\n"
            "Do not include explanation or markdown code block formatting."
        )

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self._model}:generateContent"
        body = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseMimeType": "application/json"},
        }
        data = json.dumps(body).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={"x-goog-api-key": self._api_key, "Content-Type": "application/json"},
        )

        start_time = time.perf_counter()
        max_retries = 4
        last_error: Exception | None = None
        for attempt in range(max_retries):
            try:
                with urllib.request.urlopen(req, timeout=30) as resp:
                    resp_data = json.loads(resp.read().decode("utf-8"))
                    break
            except urllib.error.HTTPError as e:
                last_error = e
                wait = 12.0 * (attempt + 1) if e.code == 429 else 3.0 * (attempt + 1)
                time.sleep(wait)
            except Exception as e:
                last_error = e
                time.sleep(2.0 * (attempt + 1))
        else:
            raise RuntimeError(
                f"Gemini API request failed after {max_retries} attempts: {last_error}"
            )

        latency = time.perf_counter() - start_time
        # Keep requests paced; tune this interval for the API project's current limits.
        time.sleep(1.5)

        try:
            raw_text = resp_data["candidates"][0]["content"]["parts"][0]["text"].strip()
            # Clean possible markdown wrapping if returned
            if raw_text.startswith("```"):
                raw_text = re.sub(r"^```(?:json)?\n?", "", raw_text)
                raw_text = re.sub(r"\n?```$", "", raw_text)
            parsed = json.loads(raw_text)
            if isinstance(parsed, list):
                selected = [str(x) for x in parsed if str(x) in pool_dict]
            else:
                selected = []
        except Exception:
            selected = []

        return AdapterResult(
            pair_id=pair.id,
            adapter_name=self.name,
            selected_ids=selected,
            latency_s=latency,
            cost_usd=None,
            shuffle_index=shuffle_index,
        )
