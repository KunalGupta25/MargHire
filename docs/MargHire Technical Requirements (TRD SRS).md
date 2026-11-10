# MargHire: Technical Requirements (TRD / SRS)

Nov 9, 2026 · @Kunal Gupta

## Scope and system overview

This document specifies how MargHire is built to meet the product requirements (F1 to F15 in the PRD). It covers one deployable system: a web app and API with a Python helper process, an MCP server, and a SQLite or Postgres database, run through Docker. It does not cover a hosted multi-tenant service.

Requirement IDs here use the form `TR-<module>-<n>`. "Must" means required for v1; "should" means v1 if time allows.

## Architecture

&#91;embedded content: system architecture · 11 components\]

The web UI and MCP clients call the same service layer, so both behave identically. The provider router is the only code that talks to AI providers.

## Technology stack and repository layout

| Layer | Choice | Reason |
| --- | --- | --- |
| API | TypeScript, Hono on Node | Small, and portable to Cloudflare Workers later |
| Database | Drizzle ORM over SQLite (default) or Postgres | Zero-setup default, upgrade path |
| UI | React, TypeScript | Visual resume editor and dashboard |
| Resume rendering | Tectonic (LaTeX) and Typst | Self-contained binaries, no TeX Live install |
| Python helper | Python 3.10+ sidecar (optional) | Laya local inference, embeddings, evaluation scripts |
| MCP | Official MCP TypeScript SDK | Same service layer as the API |
| Packaging | Docker Compose | Docker first, per the product decision |
| Tests | Vitest, Playwright, pytest | See the testing document |

```text
marghire/
  apps/
    api/          Hono API and service layer
    web/          React UI
    mcp/          MCP server (thin wrapper over services)
  packages/
    core/         pool, Role Lens, resume engine, truthfulness check
    providers/    router and provider adapters
    sources/      profile importers and job sources (plugins)
    db/           Drizzle schema and migrations
    templates/    LaTeX and Typst templates, ATS profiles
  python/         Laya sidecar, embeddings, eval
  docs/           product, design and test documents
  docker/         Dockerfiles and compose files
```

## Functional requirements by module

| ID | Requirement | PRD |
| --- | --- | --- |
| TR-POOL-1 | The system must store pool data in the schema in the data blueprint, with `verified` defaulting to false on import. | F1 |
| TR-POOL-2 | Each importer must implement one interface: `connect`, `fetch`, `normalize`, `dedupe`. New sources are added as plugins. | F2 |
| TR-POOL-3 | The LinkedIn importer must read the data-export ZIP (Profile, Positions, Education, Skills and related CSVs) and must not call LinkedIn pages. | F2 |
| TR-POOL-4 | GitHub import must connect through GitHub sign-in, import private repos as well as public ones by default, honour rate-limit headers, and show the user which repos were read. | F2 |
| TR-LENS-1 | Role Lens must take a job analysis and the verified pool and return a ranked selection with a score and reason per item. | F3 |
| TR-LENS-2 | Every sentence in a generated document must map to pool ids. Output that fails this check must be rejected or flagged, never shown as final. | F3 |
| TR-RES-1 | Mode B must build a JSON Resume document from the selection, then render through the chosen template. | F5, F6 |
| TR-RES-2 | Mode A must parse the uploaded resume into the same JSON form, produce a change list, and apply only accepted changes. | F4 |
| TR-RES-3 | Rendering must produce a PDF and report any compile error with the source line. | F6 |
| TR-DRAFT-1 | The cover letter and HR email must be generated from the job analysis and selected pool items, and saved as editable drafts. | F8 |
| TR-JOB-1 | Job sources must be plugins returning a common job object with `description_quality`. Jobs dedupe on a hash of company, title and location. | F10 |
| TR-TRK-1 | The tracker must record status changes as events and allow one application per job. | F9 |
| TR-ONB-1 | First-run setup must persist its choices and let the user change them later in Settings. | F14 |

## Provider router and decision-model specification

**Wire formats.** The router speaks four formats: OpenAI chat, Anthropic Messages, Gemini native, and Cloudflare Workers AI REST. OpenAI-compatible providers (NVIDIA, OpenRouter, Kilo, Ollama, custom) reuse the first.

**Selection.** Each task (rank items, rewrite bullets, draft letter) has an ordered chain of provider and model pairs. Strategy is free-first (local, then free tier, then paid) or quality-first. Paid providers join a chain only when the user adds a key and enables them.

**Fallback and errors**

- Timeouts, 408, 429 and 5xx: retry once with backoff, honouring `Retry-After`, then move to the next entry in the chain.
- 400, 401 and 403: try the next provider in the chain, and warn the user afterwards which provider failed and why. If every provider fails, report all of them.
- A circuit breaker opens after repeated failures and closes after a cool-down.
- Client-side rate limits per provider (for example NVIDIA at about 40 requests a minute, to be confirmed) prevent hitting server limits.
- A budget guard blocks paid calls once the daily limit set by the user is reached.
- Cloudflare's free allowance of 10,000 Neurons a day resets at 00:00 UTC (05:30 IST). The ledger keeps a running count and the router moves on before the cap.
- Cloudflare's AI Gateway universal fallback endpoint is deprecated, so MargHire owns fallback itself.

**Decision models**

- Used for choose-from-a-list tasks, such as which items fit a job. Laya runs locally through the Python helper; Clef and Clef-flash run on Workers AI; Jev uses the user's own key.
- A decision model is used only if its provider has "also use for decision models" ticked and the model is marked as a decision model.
- Each call shuffles option order and repeats to average out order sensitivity. Choices over about 20 options are split into groups.
- If confidence is under the user's threshold, ask the LLM; if that is also unsure, ask the user.
- If no decision model is available or all are rate-limited, the task runs on the LLM chain. The product must work in LLM-only mode.

## Resume engine: Role Lens, Mode A, Mode B, rendering

**Role Lens pipeline**

1. Analyse the job description into required skills, nice-to-haves, keywords and seniority.
2. Score each verified pool item against the analysis. Use embeddings for a first pass, then the decision model or LLM for the final pick.
3. Apply caps: for example the most relevant projects and a bounded skill list, so the resume stays within the template's page limit.
4. Save the result in `role_lens_run`, with a reason for each item kept or dropped.
5. Run the truthfulness check on any reworded text before it is saved.

**Mode B (generate).** Selection becomes a JSON Resume document, which fills a LaTeX or Typst template. The LLM may reword bullets for clarity and keyword match but cannot add a skill, employer, date or metric that is not in the pool. Sections with no pool items, such as About me, are written from the user's basic details, the job description and the pooled information.

**Mode A (edit).** Parse the uploaded file into JSON Resume. Propose changes against the job as a change list with before, after and a reason. The user accepts or rejects each. TeX, DOCX and JSON are edited in place on a copy; PDF input is re-rendered from the parsed content, and the user is told the layout may change.

**Truthfulness check.** Compare every skill, employer, date, number and technology in the output to the pool. Anything not found is flagged and blocks export until the user fixes it or confirms it as a new, verified pool item.

**Rendering.** Tectonic compiles LaTeX; Typst compiles Typst. Render runs in a sandboxed process with a time limit and no network. An ATS score is computed for each resume from checks such as text extraction, headings and single-column layout. Per-company ATS profiles are deferred until verified on real postings.

## API surface and MCP tools

The REST API and the MCP server call the same service layer, so behaviour is identical.

| Area | REST resources | MCP tools |
| --- | --- | --- |
| Pool | `/pool/items`, `/pool/skills`, `/sources`, `/imports` | `pool_search`, `pool_get`, `pool_update`, `import_run` |
| Jobs | `/jobs`, `/jobs/:id/analysis`, `/job-sources` | `job_add`, `job_search`, `job_analyze` |
| Resumes | `/resumes`, `/resumes/:id/versions`, `/resumes/:id/render` | `resume_generate`, `resume_edit`, `resume_render` |
| Drafts | `/drafts` | `draft_cover_letter`, `draft_hr_email` |
| Tracker | `/applications`, `/applications/:id/events` | `application_log`, `application_list` |
| Providers | `/providers`, `/providers/:id/models`, `/providers/:id/fetch-models` | read-only status tool |
| Settings | `/settings`, `/onboarding` | none |

The provider fetch-models endpoint calls the provider's model-list route and returns names for the user to pick from; nothing is saved until the user selects models. MCP tools that change data must require an explicit argument, and tools never return stored API keys.

## Non-functional requirements and deployment

| Area | Requirement |
| --- | --- |
| Deployment | `docker compose up` starts API, web and database, plus the Python helper when enabled. Data lives in one mounted volume. |
| Performance | Targets to set after Phase 1 measurements: resume render time, Role Lens time on a typical pool, and UI load time. |
| Reliability | A provider failure never loses user edits; every generation is saved as a version. |
| Security | Follow the privacy and security checklist. Bind to localhost by default; require explicit config to expose. |
| Observability | Structured logs without personal data; usage ledger visible in the UI. |
| Portability | API code avoids Node-only APIs where practical so it can run on Workers later. |
| Accessibility | WCAG 2.1 AA basics in the UI. |
| Compatibility | Latest two versions of Chrome, Firefox, Safari and Edge. |
| Licence compliance | AGPL-3.0; every dependency licence is checked in CI. |
