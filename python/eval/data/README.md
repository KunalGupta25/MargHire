# Evaluation pairs

Each `.json` file in this directory is one evaluation unit: a fake professional pool, a fake job
description, and hand-labelled inclusion decisions.

**All data here is synthetic.** No real names, companies, repos or resumes are used.

If you want to evaluate against your own resumes, put those files in a separate directory outside
the repo, and set `EVAL_PRIVATE_PAIRS_DIR` in your `.env` to that path.

## Schema

```json
{
  "id": "pair-001",
  "created_by": "synthetic",
  "created_at": "2026-11-10",
  "job": {
    "title": "Role title",
    "description": "Full job description text."
  },
  "pool": [
    {
      "id": "item-001",
      "kind": "skill | project | work | education | certification | publication",
      "text": "Human-readable description of this item.",
      "tags": ["optional", "category", "tags"]
    }
  ],
  "labels": {
    "item-001": true,
    "item-002": false
  }
}
```

Rules:
- Every item in `pool` must have a corresponding key in `labels`.
- `labels` must not reference ids not in `pool`.
- `created_by` should be `"synthetic"` for files in this directory.
- If you use a human labeller for private pairs, record their name or initials.

## Role families covered

| Family | Pair ids |
|---|---|
| Designer | pair-001 to pair-009 |
| Frontend | pair-010 to pair-018 |
| Backend | pair-019 to pair-027 |
| AI / ML | pair-028 to pair-036 |
| Cloud / DevOps | pair-037 to pair-044 |
| Mixed / Generalist | pair-045 to pair-050 |
