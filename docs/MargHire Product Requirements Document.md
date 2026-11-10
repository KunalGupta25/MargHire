# MargHire: Product Requirements Document

Nov 9, 2026 · @Kunal Gupta

## Overview

MargHire is a free, self-hostable, open-source (AGPL-3.0) tool that turns one pool of a fresher's professional data into a resume, cover letter and HR email tailored to each job. It is built for Indian IT freshers and is personal-use first.

**Problem.** A fresher has design, video, frontend, backend, cloud and AI skills, plus projects and education. Putting all of it on every resume dilutes the match for a given role and can hurt ATS ranking. Existing tools import a resume and find jobs; none lets you choose, per job, which parts of your pool to show.

**Solution.** MargHire gathers the pool from GitHub, Hugging Face, GitLab, a LinkedIn data export, uploaded resumes and manual entry. For each job it scores pool items against the job description (the Role Lens), then either edits an existing resume (Mode A) or generates a new one from the pool (Mode B). It also drafts the cover letter and HR email, tracks applications, and exposes everything through an MCP server so other AI agents can use it.

**Success looks like** (targets to confirm in Phase 0):

- A user reaches a first tailored resume as fast as possible. There is no fixed time target; measure it in Phase 1 and keep improving it.
- Every line on a generated resume traces to a verified pool item; nothing is invented.
- The default setup costs nothing to run.

## Goals and non-goals

**Goals for v1**

- Build one editable pool of skills, projects, experience, education and contact details from multiple sources.
- Produce a job-specific resume in two modes: edit an existing resume, or generate from the pool.
- Draft a cover letter and HR email per job, and track every application.
- Run free by default, using free-tier and local AI providers with automatic fallback.
- Expose pool, resume, job and tracker functions through an MCP server.
- Show an ATS score for each resume. Indian IT ATS style profiles come later, once verified.

**Non-goals for v1**

- Auto-submitting applications on job portals.
- Scraping LinkedIn or Naukri in the core product.
- Multi-user accounts, teams or billing. The schema keeps an `owner_id` so this can come later.
- A hosted SaaS. Docker self-hosting comes first; Cloudflare is an AI provider, not a deploy target.

## Users and personas

| Persona | Context | Needs |
| --- | --- | --- |
| Fresher applicant | Final-year or recent graduate in India applying for IT roles, with several skill areas and little experience | A resume per job that shows only relevant skills; ATS-safe output; no cost |
| Self-hoster | Developer who runs MargHire from GitHub with their own API keys | Simple Docker setup, pluggable providers and sources, clear data ownership |
| AI agent user | Someone driving MargHire from Claude, Cursor or another MCP client | Stable tools to read the pool, build resumes and log applications |

## Feature requirements

Priority: P0 = needed for v1, P1 = v1 if time allows, P2 = after v1.

| ID | Feature | Requirement | Priority |
| --- | --- | --- | --- |
| F1 | Pool | Store skills, projects, experience, education, about, contact and links. Every item has a source, an evidence link, a verified flag and tags. Imported items start unverified. | P0 |
| F2 | Pool import | Import from GitHub (through GitHub sign-in, so private repos can be read), Hugging Face Hub API, GitLab API, LinkedIn data export ZIP, resume upload (PDF, DOCX, TeX, JSON Resume) and manual entry. No LinkedIn scraping in core. | P0 |
| F3 | Role Lens | Given a job description, score and select pool items. Use verified pool items only. Sections with no pool items, such as About me, are written from the user's basic details, the job description and the pooled information. The LLM may reword but never invent. A truthfulness check compares output against the pool. | P0 |
| F4 | Mode A | Parse an existing resume, propose changes as a tracked diff, let the user accept or reject each. In-place edit for TeX, DOCX and JSON; PDF is re-rendered. | P0 |
| F5 | Mode B | Generate a resume per job from the pool into a chosen template. | P0 |
| F6 | Resume output | Render LaTeX (Tectonic) or Typst to PDF, with a visual editor and live preview. | P0 |
| F7 | ATS profiles | One ATS score for each generated resume (text extraction, headings, single-column layout). Separate service-company and product-company profiles are deferred until their rules are verified. | P1 |
| F8 | Cover letter and HR email | Draft both per job from the pool and job description; user edits before use. | P0 |
| F9 | Application tracker | Record company, role, date, status, resume version and contacts. | P0 |
| F10 | Job discovery | Pluggable sources: Greenhouse, Lever and Ashby public JSON, Adzuna, Jooble, Careerjet, plus paste-a-job. Dedupe across sources; mark each job's description quality as full or snippet. | P1 |
| F11 | Provider router | OpenAI, Gemini, Anthropic, Cloudflare Workers AI, NVIDIA, OpenRouter, Kilo, Ollama and custom endpoints. Free-first or quality-first order, usage ledger, budget guard, automatic fallback. | P0 |
| F12 | Decision models | Optional Laya (local), Clef and Clef-flash (Cloudflare), Jev (own key). Low-confidence results fall back to the LLM or ask the user. | P1 |
| F13 | MCP server | Tools for pool, jobs, resume build, drafts and tracker. | P1 |
| F14 | Onboarding | Six-step first-run setup: welcome, decision models, AI providers, profile sources, resume mode, ready. | P0 |
| F15 | Optional aggregator plugins | Apify, Bright Data, PDL and similar, off by default, self-profile only. | P2 |

## User flows and onboarding

**First run** (six screens, designed on the onboarding canvas):

1. Welcome: what MargHire does, then start setup.
2. Decision models: choose "Decision model + LLM" or "LLM only"; set the confidence threshold.
3. AI providers: add any number of providers; fetch each provider's model list or add models by hand. In decision-model mode, mark providers and individual models as decision models.
4. Profile sources: LinkedIn export, resume upload, GitHub, Hugging Face, GitLab, manual.
5. Resume mode: default to edit-existing (Mode A) or generate-from-pool (Mode B). Every resume also gets an ATS score.
6. Ready: summary, then review the pool, add a first job, open the dashboard.

**Core loop per job**

1. Add a job by pasting its description, a link, or picking one from discovery.
2. Role Lens scores the pool and shows what it would include and leave out.
3. User adjusts the selection.
4. Generate or edit the resume (Mode A or B), then review the diff and the PDF preview.
5. Draft the cover letter and HR email; edit.
6. Export, apply outside MargHire, and mark the job as applied in the tracker.

## Non-functional requirements and constraints

- **Cost:** default setup is free. Paid providers are opt-in with the user's own keys.
- **Licence:** AGPL-3.0.
- **Deployment:** Docker first, SQLite by default, Postgres optional. Single user in v1.
- **Privacy:** data stays on the user's machine; the only outbound traffic is to providers and sources the user enabled. See the privacy and security checklist.
- **Resilience:** when a provider hits a limit or fails, fall back automatically; the app stays usable with no decision model.
- **Accuracy:** no invented facts on any generated document.
- **Accessibility:** UI meets WCAG 2.1 AA basics; touch targets at least 44px.
- **Legal:** LinkedIn and Naukri terms prohibit scraping, so the core uses official or export routes. The DPDP Rules 2025 main obligations apply from 13 May 2027. The author is not a lawyer; get advice before any hosted use.

## Release phases and acceptance criteria

The build order and tasks are in the implementation plan; this table holds the acceptance gates, using the same phase numbers.

| Phase | Scope | Done when |
| --- | --- | --- |
| 0 | Repo, CI, Docker skeleton; spike comparing Laya, Clef and an LLM on about 50 labelled pairs | A written result and a decision on the default mode |
| 1 | Pool, imports (LinkedIn ZIP, resume upload, GitHub, Hugging Face, GitLab), verification gate | A real profile loads with evidence links |
| 2 | Provider router, fallback, ledger, setup wizard | All forced-failure tests pass |
| 3 | Role Lens, truthfulness check, Mode A and Mode B, job analysis | Designer and backend resumes from one pool differ correctly |
| 4 | Templates, ATS score, export | PDF text extracts cleanly |
| 5 | Cover letter, HR email, tracker, job sources | One job goes from paste to tracked draft |
| 6 | MCP server and docs | Another agent builds a resume through MCP |
| 7 | India pack (ongoing) | Verified against real postings |

## Risks, open questions and unverified facts

| Item | Why it matters | Plan |
| --- | --- | --- |
| Decision models are order-sensitive and untested on this task | Wrong picks would hurt resumes | Shuffle and average options, calibrate thresholds, fall back to the LLM; verify in Phase 0 |
| Jev pricing and signup status | May not be free | Treat as optional, own key |
| Whether Clef and Clef-flash run inside Cloudflare's free allowance | Affects the free-by-default promise | Check before shipping the Cloudflare default |
| LinkedIn Member Data Portability API for India | Could replace the ZIP export | Unconfirmed; keep ZIP as the main route |
| Free-tier limits for Gemini, OpenRouter, Workers AI, Kilo, Adzuna | Drive the router's rate limits | Read each provider's current docs when building its adapter |
| Which ATS each Indian company uses | Drives ATS profiles | Sources conflict; test on real postings before claiming |
| Name availability for MargHire | Near names exist (MarqHire, MarHire SARL, Marg HR) | Check GitHub, PyPI, npm, domain and IP India before launch |
| Scraping and terms of service | Legal exposure | Official and export routes only; aggregator plugins off by default |

## Decisions log, 10 November 2026

Answers to the open-questions form. Items not listed were confirmed as written.

| Topic | Decision |
| --- | --- |
| Time to first resume | No fixed target; as fast as possible |
| Unverified items | Never on a resume. Sections with no pool items are written from basic details, the job description and the pool |
| Tracker columns | Saved, Applied, Interview, Offer, Rejected, Withdrawn, No response (you listed all but Saved; I kept Saved, confirm) |
| First usable version | All pages, including Job search |
| Welcome screen | No sample-data option |
| Usage log | Keep all rows, no roll-up |
| Bad key or bad request from a provider | Try the next provider and warn afterwards |
| API framework | Left to me; Hono stays |
| Python helper | Kept, but optional |
| Record IDs | UUID |
| GitHub | Sign in with GitHub, private repos imported by default |
| ATS | One ATS score; no style choice until the research is done |
| Phase 0 data | A mix of your own and synthetic pairs |
| Cloudflare | You have a free account |
| Role Lens precision and recall targets | Still open (question 27 was not answered) |
