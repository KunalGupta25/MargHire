# MargHire: Implementation Plan and Build Order

Nov 10, 2026 · @Kunal Gupta

## Build principles and dependency order

The plan is about 10 weeks for one person. Build the data first, because every other part depends on it.

1. **Schema and pool** come first. Nothing else can be tested without real pool data.
2. **Provider router** next, so every AI feature has one way to call models.
3. **Role Lens and the truthfulness check** use the pool and the router.
4. **Rendering and templates** turn a selection into a PDF.
5. **Drafts and tracker** reuse the pool, job analysis and router.
6. **MCP server** wraps the service layer last, because it adds no new logic.

**Working rules**

- Ship a thin end-to-end path early: paste a job, get a PDF. Widen it afterwards.
- Phase 0 decides whether decision models are worth building around. If they do not beat a cheap LLM on the test pairs, ship LLM-only first and keep decision models as an option.
- Every phase ends with its "done when" check passing, not just code written.
- The agent files (Agent.md, Claude.md) and the test plan apply from day one.

## Phases

| Phase | Weeks | Deliverable | Done when |
| --- | --- | --- | --- |
| 0 | 0.5 | Repo, AGPL-3.0, CI, compose skeleton. Spike: run Laya, Clef and an LLM on about 50 hand-labelled resume and job pairs (a mix of your own and synthetic) | We know which model handles which task, and whether Clef runs in the free allowance |
| 1 | 2 | Pool: schema, editor, resume upload, LinkedIn export (1a); GitHub, Hugging Face, GitLab importers, skill inference, verification gate (1b) | A real profile loads with evidence links |
| 2 | 2 | Provider router, key storage, fallback, usage ledger, budget guard, Cloudflare Neuron counter, setup wizard | All forced-failure tests pass |
| 3 | 2 | Decision layer, Role Lens, selection explanations, truthfulness check, Mode A and Mode B, job add and analysis | Designer and backend resumes from one pool differ correctly |
| 4 | 1 | LaTeX and Typst templates, ATS profiles, export, PDF re-render for Mode A | PDF text extracts cleanly |
| 5 | 1 | Cover letter and HR email drafts (`.eml`), tracker, dashboard; 5b: job-source registry, job schema, Tier A adapters, paste intake | One job goes from paste to tracked draft |
| 6 | 1 | MCP server, API docs, help and about | Another agent builds a resume through MCP |
| 7 | Ongoing | India pack: ATS profiles, job-title taxonomy, verified company list, portal export formats | Verified against real postings |

Phase 0 is the most important phase. It tests whether decision models beat a cheap LLM for this work before the build commits to them.

## Tasks: phases 0 to 3

**Phase 0: foundations and spike**

- [ ] Create the `marghire` repo with AGPL-3.0 licence, README, `.gitignore` (data directory, `.env`), and the folder layout from the technical requirements.
- [ ] Add CI: lint, type-check, tests, dependency audit, licence check, secret scan.
- [ ] Write `docker-compose.yml` with API, web, Python helper and SQLite volume.
- [ ] Build the spike harness: about 50 resume and job pairs (a mix of your own and synthetic ones), with hand-labelled "should this item appear" answers.
- [ ] Run Laya, Clef or Clef-flash, and a chosen LLM on the pairs. Record accuracy, order sensitivity, latency and cost.
- [ ] Test whether Clef and Clairic run inside Cloudflare's free allowance, using your free Cloudflare account.
- [ ] Write a one-page result and decide: Decision + LLM, or LLM only as the default.

**Phase 1a: pool basics**

- [ ] Drizzle schema and migrations for pool tables (see the data blueprint).
- [ ] Pool CRUD API and the Pool, Item detail and Review queue pages.
- [ ] Resume upload (PDF, DOCX, TeX, JSON Resume) with parsing into JSON Resume.
- [ ] LinkedIn export ZIP importer.
- [ ] Manual entry forms.

**Phase 1b: connected sources**

- [ ] Source plugin interface and registry (`connect`, `fetch`, `normalize`, `dedupe`).
- [ ] GitHub (through GitHub sign-in, including private repos), Hugging Face and GitLab importers with evidence links.
- [ ] Skill inference from repos, marked unverified.
- [ ] Verification gate: nothing unverified reaches a resume.

**Phase 2: provider router**

- [ ] Provider and model tables, encrypted key storage.
- [ ] Adapters for OpenAI chat, Anthropic Messages, Gemini native and Cloudflare Workers AI.
- [ ] Fetch-models endpoint per provider, and manual model add or edit.
- [ ] Chains, free-first and quality-first strategies, decision-model flags on providers and models.
- [ ] Error policy (try the next provider on 400, 401 and 403 and warn afterwards), retries, `Retry-After`, circuit breaker, client-side rate limits.
- [ ] Usage ledger, budget guard, Cloudflare Neuron counter resetting at 00:00 UTC.
- [ ] Failure test script: rate limit, timeout, bad key, bad model ID, for each provider; each must end with a warning and a fallback.
- [ ] Setup wizard (the six onboarding screens, with no sample-data option), Providers, Chains and modes, Usage pages.

**Phase 3: Role Lens and resumes**

- [ ] Job add and job analysis (required skills, keywords, seniority, role family).
- [ ] Role Lens scoring with embeddings, then decision model or LLM, with confidence and fallback.
- [ ] Selection explanations stored per item.
- [ ] Truthfulness check on every generated sentence.
- [ ] Mode B: selection to JSON Resume.
- [ ] Mode A: parse, change list, accept and reject, in-place edit for TeX, DOCX and JSON.
- [ ] New resume wizard, Resume library, Tailor diff review, Decision lab.

## Tasks: phases 4 to 7

**Phase 4: templates and export**

- [ ] Two or three ATS-safe LaTeX and Typst templates.
- [ ] Tectonic and Typst render service with time limit, no network, no shell escape.
- [ ] ATS score for each resume (text extraction, headings, columns). Per-company ATS profiles wait for Phase 7.
- [ ] Resume editor with live PDF preview and the Role Lens side panel.
- [ ] PDF re-render path for Mode A when the source is a PDF.
- [ ] Templates and ATS score page.

**Phase 5: drafts, tracker and jobs**

- [ ] Cover letter and HR email drafting from job analysis and selected items.
- [ ] `.eml` and PDF export in the Application kit.
- [ ] Tracker (board and list), Application detail with events and reminders, Companies, Dashboard.
- [ ] 5b: normalised job schema, job-source registry, Tier A adapters (Greenhouse, Lever, Ashby, Adzuna, Jooble, Careerjet), paste intake, dedupe, Job search page.
- [ ] Tier C scrapers only as optional community plugins, last.

**Phase 6: MCP and docs**

- [ ] MCP server with the tool list from the technical requirements; read-only and read-write tokens.
- [ ] MCP and API page with copy-paste client configs.
- [ ] Self-hosting guide, plugin guide, contributor guide, Help and about page.
- [ ] Test: an external agent completes the core loop through MCP only.

**Phase 7: India pack (ongoing)**

- [ ] Verify which ATS each target company uses; fill the company list.
- [ ] Test ATS profile rules against real postings and real resume parsers.
- [ ] Job-title taxonomy for Indian IT roles (for example AI engineer, MERN developer, data analyst).
- [ ] Portal export formats where the portals allow it.

## Cross-cutting work and definition of done

- [ ] Keep Agent.md and Claude.md current as the layout changes.
- [ ] Run the Ponytail review on each pull request, and refresh the Graphify graph after large changes.
- [ ] Update the security checklist items as they are built.
- [ ] Write a migration for every schema change; run it on SQLite and Postgres in CI.
- [ ] Keep fixtures fake; never commit real resumes.
- [ ] Re-check unverified facts (listed in the PRD) as each related feature is built.

**A task is done when:** the code is merged, tests for it pass, the matching checklist items in the test and security documents are ticked, and docs are updated.

## Your first two weeks

1. Day 1: create the repo, licence, `.gitignore`, and commit Agent.md and Claude.md.
2. Day 1 to 2: add the folder layout, CI and the Docker Compose skeleton; confirm `docker compose up` runs an empty API and web page.
3. Day 2 to 3: build the Phase 0 test set (about 50 pairs) and the harness.
4. Day 3 to 5: run Laya, Clef or Clef-flash, and one LLM; write the one-page result.
5. Week 2: start Phase 1a. Schema and migrations first, then Pool CRUD, then resume upload.
6. End of week 2: a manually entered profile and one uploaded resume appear in the Pool page, with unverified items in the Review queue.
