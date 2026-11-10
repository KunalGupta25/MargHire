# MargHire

A free, self-hostable, open-source tool for Indian IT freshers. It keeps one pool of your
professional data, then builds a resume, cover letter and HR email tailored to each job. It also
tracks applications and exposes everything through an MCP server.

**Status:** Phase 0 (repo skeleton and evaluation harness). Not yet usable end-to-end.

## What it does

- Builds one editable pool from GitHub, Hugging Face, GitLab, a LinkedIn data export, uploaded
  resumes and manual entry.
- For each job, Role Lens scores your pool against the job description and selects the most
  relevant items.
- Produces a job-specific resume in two modes: edit an existing resume (Mode A) or generate one
  from the pool (Mode B).
- Drafts a cover letter and HR email, tracks every application.
- Exposes pool, resume, job and tracker functions through an MCP server.
- Runs free by default, using free-tier and local AI providers with automatic fallback.

## Quick start

Requirements: Docker and Docker Compose.

```sh
git clone https://github.com/yourusername/marghire.git
cd marghire
cp .env.example .env
# Edit .env if needed (the defaults work for local development)
docker compose up
```

The API starts at `http://localhost:3000` and the UI at `http://localhost:5173`.

The Python helper (Laya local inference, evaluation scripts) is off by default:

```sh
docker compose --profile python up
```

## Development setup (without Docker)

Requirements: Node 20+, npm 10+, Python 3.10+.

```sh
npm install
cp .env.example .env
# Set DATABASE_URL to a SQLite path (see .env.example)
npm run dev
```

## Commands

| Task | Command |
|---|---|
| Install | `npm install` |
| Run everything | `docker compose up` |
| Lint and type-check | `npm run lint && npm run typecheck` |
| Unit tests (TS) | `npm test` |
| Unit tests (Python) | `cd python && pytest` |
| End-to-end tests | `npx playwright test` |
| Create a migration | `npx drizzle-kit generate` |

## Repository layout

```
apps/api         Hono API and service layer (TypeScript)
apps/web         React UI
apps/mcp         MCP server, a thin wrapper over the services
packages/core    pool, Role Lens, resume engine, truthfulness check
packages/providers   provider router and adapters
packages/sources     profile importers and job sources (plugins)
packages/db      Drizzle schema and migrations
packages/templates   LaTeX and Typst templates, ATS profiles
python/          optional Laya sidecar, embeddings, evaluation scripts
docs/            planning documents
docker/          Dockerfiles and compose files
```

## Planning documents

The `docs/` folder contains all planning documents:

- **Product Requirements Document** - what to build and why (features F1-F15)
- **Technical Requirements (TRD/SRS)** - architecture, module requirements (TR-*)
- **Database Schema and Data Blueprint** - tables, columns, rules
- **Implementation Plan and Build Order** - phases 0-7
- **Test Plan and Test Cases** - test IDs (T-*), CI gates, acceptance criteria
- **Design and UX Document** - pages, screens, components, accessibility
- **Privacy, Security and Compliance Checklist** - rules every change must respect

## Licence

AGPL-3.0. See [LICENSE](LICENSE).

Every dependency licence is checked in CI. If you add a dependency, make sure its licence is
compatible with AGPL-3.0.

## Contributing

Read `AGENTS.md` and `CLAUDE.md` before making any change. The working style, definition of done
and rules are there.

Data policy: fixtures use fake people, companies and repos only. Real resumes, API keys and
personal data must never be committed to the repository.
