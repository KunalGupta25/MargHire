# MargHire: Database Schema and Data Blueprint

Nov 9, 2026 · @Kunal Gupta

## Conventions

- **Engine:** SQLite by default, Postgres optional, through Drizzle ORM. Column types below are the portable subset.
- **IDs:** UUID text primary keys.
- **Timestamps:** `created_at` and `updated_at` as UTC ISO-8601 text on every table.
- **Owner:** every user-data table has `owner_id` (text). v1 uses one fixed owner; multi-user later needs no migration of shape.
- **Soft delete:** user-facing records use `deleted_at` (nullable); hard delete is a separate "erase my data" action.
- **Schema shape:** pool items follow JSON Resume sections (basics, work, education, skills, projects), extended with `evidence`, `verified`, `source` and `tags`.
- **Secrets:** API keys are never stored in plain text in the database. Store them encrypted with a key from the environment, or reference an environment variable name.

## Pool tables

| Table | Key columns | Notes |
| --- | --- | --- |
| `profile` | id, owner\_id, full\_name, headline, about, email, phone, location, links (JSON) | One row per owner. Maps to JSON Resume `basics`. |
| `pool_item` | id, owner\_id, kind, title, org, start\_date, end\_date, summary, tags (JSON), source\_id, verified (bool), include\_default (bool), sort\_key | `kind` is one of work, education, project, skill, certification, award, publication, link. |
| `pool_bullet` | id, item\_id, text, impact\_note, verified, sort\_key | Achievement lines under an item. Resume lines are chosen from these. |
| `skill` | id, owner\_id, name, category, level, years, verified | Separate from `pool_item` so skills can be scored on their own. Category examples: design, frontend, backend, cloud, AI, video. |
| `evidence` | id, item\_id, type, url, excerpt, fetched\_at | Proof for an item: repo URL, README excerpt, certificate link, export file row. |
| `source` | id, owner\_id, type, label, config (JSON), last\_sync\_at | Types: github, huggingface, gitlab, linkedin\_export, resume\_upload, manual. Tokens go through the secrets rule. GitHub connects through GitHub sign-in so private repos can be read. |
| `import_run` | id, source\_id, status, started\_at, finished\_at, items\_added, items\_changed, error | One row per import, so a bad import can be reviewed or undone. |
| `item_revision` | id, item\_id, changed\_by, before (JSON), after (JSON), created\_at | Edit history for pool items. |

Rules: an item created by an import has `verified = false`. Only verified items are eligible for Role Lens. A bullet is verified only if its item is.

## Jobs, applications and contacts

| Table | Key columns | Notes |
| --- | --- | --- |
| `company` | id, owner\_id, name, website, ats\_vendor (nullable), notes | `ats_vendor` stays empty unless confirmed. |
| `job` | id, owner\_id, company\_id, title, location, work\_mode, employment\_type, description\_text, description\_quality, source\_type, source\_url, external\_id, posted\_at, dedupe\_hash, status | `description_quality` is `full` or `snippet`. `dedupe_hash` is built from company, title and location. |
| `job_analysis` | id, job\_id, required\_skills (JSON), nice\_to\_have (JSON), seniority, keywords (JSON), model\_used, created\_at | Output of reading a job description. |
| `application` | id, owner\_id, job\_id, resume\_id, status, applied\_at, channel, follow\_up\_on, notes | Status: saved, preparing, applied, interview, offer, rejected, withdrawn, no\_response. |
| `application_event` | id, application\_id, type, occurred\_at, note | Timeline of status changes and follow-ups. |
| `contact` | id, owner\_id, company\_id, name, role, email, source, note | HR or recruiter contacts the user entered or found through allowed sources. |

Uniqueness: one `application` per `job_id`. Duplicate jobs from different sources collapse on `dedupe_hash`.

## Resume, draft and template tables

| Table | Key columns | Notes |
| --- | --- | --- |
| `resume` | id, owner\_id, job\_id (nullable), mode, base\_resume\_id (nullable), template\_id, ats\_profile, selection (JSON), status, created\_at | `mode` is `edit` (Mode A) or `generate` (Mode B). `selection` lists the pool item and bullet ids chosen. |
| `resume_version` | id, resume\_id, version\_no, source\_format, content (JSON), rendered\_path, truthfulness\_report (JSON), ats\_score (JSON), created\_at | Each save is a version. `content` is the JSON Resume document. |
| `resume_change` | id, version\_id, op, target\_path, before, after, decision, reason | Tracked changes for Mode A. `decision` is pending, accepted or rejected. |
| `uploaded_resume` | id, owner\_id, filename, format, storage\_path, parsed (JSON), uploaded\_at | Original files stay untouched; edits happen on a copy. |
| `template` | id, name, engine, path, ats\_safe (bool), notes | Engine is latex or typst. |
| `ats_profile` | id, name, rules (JSON), verified\_on, source\_notes | Rules are empty until verified. |
| `draft` | id, owner\_id, job\_id, kind, subject, body, status, model\_used, created\_at | Kind is cover\_letter or hr\_email. |
| `role_lens_run` | id, job\_id, resume\_id, scores (JSON), included (JSON), excluded (JSON), decided\_by, confidence | Records why each pool item was kept or left out. `decided_by` is decision\_model, llm or user. |

## Provider, model, usage ledger and settings tables

| Table | Key columns | Notes |
| --- | --- | --- |
| `provider` | id, owner\_id, type, label, wire\_format, base\_url, secret\_ref, tier, enabled, priority, use\_for\_decisions (bool) | `wire_format`: openai, anthropic, gemini, cloudflare. `tier`: local, free, paid. `use_for_decisions` is the "also use for decision models" tick. |
| `model` | id, provider\_id, model\_id, display\_name, source, is\_decision\_model (bool), enabled, context\_window (nullable), notes | `source` is fetched or manual. `is_decision_model` is the per-model tick. |
| `routing_rule` | id, owner\_id, task, chain (JSON), strategy | Task examples: rank\_items, rewrite\_bullets, draft\_letter. Strategy: free\_first or quality\_first. |
| `usage_ledger` | id, provider\_id, model\_id, task, tokens\_in, tokens\_out, neurons (nullable), cost\_estimate, status, latency\_ms, created\_at | Feeds budget guard and the Cloudflare daily counter. |
| `provider_state` | provider\_id, circuit\_state, open\_until, retry\_after, window\_counts (JSON) | Circuit breaker and rate-limit windows. |
| `setting` | owner\_id, key, value (JSON) | Examples: confidence\_threshold, default\_mode, default\_ats\_profile, daily\_budget, onboarding\_step. |
| `audit_log` | id, owner\_id, action, subject, detail (JSON), created\_at | Imports, exports, deletions and key changes. |

## Indexes, constraints, retention and migrations

**Indexes**

- `pool_item (owner_id, kind, verified)`
- `job (owner_id, dedupe_hash)` unique
- `job (owner_id, status, posted_at)`
- `application (owner_id, status)`
- `usage_ledger (provider_id, created_at)`
- `model (provider_id, model_id)` unique

**Constraints**

- Foreign keys on, with `ON DELETE CASCADE` for children (bullets, evidence, versions) and `RESTRICT` for company and provider.
- `pool_item.kind`, `application.status`, `draft.kind` and `resume.mode` are checked against fixed value lists.
- A resume with `mode = edit` requires `base_resume_id`.

**Retention**

- `usage_ledger` rows are kept in full. There is no roll-up or expiry.
- Uploaded originals and rendered PDFs are kept until the user deletes them.
- "Erase my data" removes every row for the owner and the files on disk, and writes one audit entry that holds no personal data.

**Migrations**

Drizzle generates SQL migrations committed to the repo. Every migration must run on both SQLite and Postgres in CI. Never edit a shipped migration; add a new one.

## Example pool item

A verified project with one bullet and its evidence. Values are made up.

```json
{
  "id": "3f2a9c1e-5b7d-4e8a-9c21-7d4e5f6a8b90",
  "kind": "project",
  "title": "Example Notes App",
  "org": null,
  "start_date": "2025-06",
  "end_date": "2025-09",
  "summary": "Offline-first notes app.",
  "tags": ["frontend", "typescript"],
  "verified": true,
  "source": { "type": "github", "label": "example-user" },
  "bullets": [
    { "id": "8b1d2c3e-4f50-4a6b-8c7d-9e0f1a2b3c4d", "text": "Built sync that works without a network connection.", "verified": true }
  ],
  "evidence": [
    { "type": "repo", "url": "https://github.com/example-user/notes-app" }
  ]
}
```
