# Graph Report - MargHire  (2026-11-10)

## Corpus Check
- 64 files · ~19,514 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 8 file(s) not represented in the graph (top: (none) 3, .example 1, .api 1)

## Summary
- 649 nodes · 854 edges · 80 communities (36 shown, 44 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 46 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `6ff44724`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Database Table: job
- Pair
- Database Table: pool_item
- _load_one
- Resume Generation & Templates
- with
- Provider Router & Fallback
- Security & Accessibility Compliance
- Provider & Usage Schema
- Onboarding Wizard & Navigation
- Application Tracking System
- Decision Models & Evaluation
- Source Importers & Integrations
- Mode A Resume Tailoring
- MCP Server & Service Layer
- Scraping & Legal Compliance
- Profile Data & Threat Model
- India Pack & ATS Profiles
- Job Discovery & Deduplication
- Cover Letter & Email Drafting
- Agent Workflow Guidelines
- ATS Profile Schema
- Audit Log Schema
- Contact Information Schema
- Drafts Storage Schema
- Routing Rule Schema
- User Settings Schema
- Skill Taxonomy Schema
- Resume Template Schema
- Uploaded Resume Schema
- Design Tokens & Palettes
- Core Tailoring Workflow
- Aggregator Plugin System
- package.json
- api
- web/package.json
- api/package.json
- db/package.json
- compilerOptions
- mcp/package.json
- compilerOptions
- db
- core/package.json
- providers/package.json
- sources/package.json
- run.py
- MargHire
- api/tsconfig.json
- mcp/tsconfig.json
- providers/tsconfig.json
- sources/tsconfig.json
- precision
- core/tsconfig.json
- db/tsconfig.json
- recall
- f1
- templates/package.json
- mcp/src/index.ts
- MargHire Python helper
- core/src/index.ts
- db/src/index.ts
- providers/src/index.ts
- sources/src/index.ts
- marghire-python
- Adapter
- schema.py
- ClefAdapter
- order_sensitivity
- Role Lens Model Comparison Spike Report
- GeminiAdapter
- LLMAdapter

## God Nodes (most connected - your core abstractions)
1. `Pair` - 42 edges
2. `AdapterResult` - 35 edges
3. `Adapter` - 15 edges
4. `aggregate()` - 15 edges
5. `compilerOptions` - 15 edges
6. `load_pairs()` - 14 edges
7. `_load_one()` - 14 edges
8. `pair_metrics()` - 14 edges
9. `compilerOptions` - 10 edges
10. `scripts` - 10 edges

## Surprising Connections (you probably didn't know these)
- `Implementation Plan: Definition of Done` --semantically_similar_to--> `Definition of Done (AGENTS)`  [INFERRED] [semantically similar]
  docs/MargHire Implementation Plan and Build Order.md → AGENTS.md
- `Rule 9: Dual-Database Schema & UUIDs` --rationale_for--> `Database Table: pool_item`  [INFERRED]
  AGENTS.md → docs/MargHire Database Schema and Data Blueprint.md
- `Rule 1: Nothing Invented` --rationale_for--> `Truthfulness Verification Engine`  [INFERRED]
  AGENTS.md → docs/MargHire Technical Requirements (TRD SRS).md
- `Multi-Level Test Strategy & CI Quality Gates` --conceptually_related_to--> `Definition of Done (AGENTS)`  [INFERRED]
  docs/MargHire Test Plan and Test Cases.md → AGENTS.md
- `Rule 2: Verified Items Only` --rationale_for--> `TR-POOL-1: Pool Schema Storage and Default Verification`  [INFERRED]
  AGENTS.md → docs/MargHire Technical Requirements (TRD SRS).md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Verified Resume Tailoring Pipeline** — docs_marghire_product_requirements_document_feature_f1, docs_marghire_product_requirements_document_feature_f3, docs_marghire_technical_requirements_trd_srs_truthfulness_checker, docs_marghire_technical_requirements_trd_srs_tr_res_1 [EXTRACTED 1.00]
- **Provider Router Resilience & Fallback Engine** — agents_rule_router_owns_fallback, docs_marghire_product_requirements_document_feature_f11, docs_marghire_technical_requirements_trd_srs_provider_router_spec, docs_marghire_database_schema_and_data_blueprint_table_usage_ledger [INFERRED 0.95]
- **Zero-Trust Verification and Secrets Perimeter** — agents_rule_verified_only, agents_rule_nothing_invented, agents_rule_secrets, docs_marghire_data_privacy_security_and_compliance_checklist_security_checklist [INFERRED 0.95]

## Communities (80 total, 44 thin omitted)

### Community 0 - "Database Table: job"
Cohesion: 0.09
Nodes (20): Claude Agent Integration & AGENTS.md Inclusion, Ponytail Code-Reuse Skill, Privacy Controls Checklist (Minimisation, Erasure, No Telemetry), Database Table: application, Database Table: application_event, Database Table: company, Database Table: job, Database Table: job_analysis (+12 more)

### Community 1 - "Pair"
Cohesion: 0.18
Nodes (7): aggregate(), pair_metrics(), AdapterResult, Pair, PairMetrics, TestAggregate, TestPairMetrics

### Community 2 - "Database Table: pool_item"
Cohesion: 0.14
Nodes (12): MargHire Repository Architecture Layout, Graphify Knowledge Graph Skill, Database Table: evidence, Database Table: import_run, Database Table: item_revision, Database Table: pool_bullet, Database Table: pool_item, Database Table: source (+4 more)

### Community 3 - "_load_one"
Cohesion: 0.11
Nodes (12): all_negative_pair(), all_positive_pair(), make_pair(), simple_pair(), _load_one(), load_pairs(), _parse(), Job (+4 more)

### Community 4 - "Resume Generation & Templates"
Cohesion: 0.29
Nodes (7): Resume Editor Three-Pane Interface Spec, Phase 4: LaTeX/Typst Templates & ATS Scoring, Feature F5: Mode B (Pool-to-Resume Generation), Feature F6: Resume Output & PDF Rendering, TR-RES-1: Mode B Resume Generation to Template, TR-RES-3: Sandboxed Tectonic & Typst PDF Compilation, Test Suite: Resume Engines & Rendering (T-RES)

### Community 5 - "with"
Cohesion: 0.07
Nodes (40): name, runs-on, steps, concurrency, cancel-in-progress, group, GITHUB_TOKEN, jobs (+32 more)

### Community 6 - "Provider Router & Fallback"
Cohesion: 0.40
Nodes (4): Phase 2: Provider Router, Key Storage & Fallback, Feature F11: Provider Router & Budget Guard, Provider Router Architecture & Wire Formats, Test Suite: Router Failure & Decision Fallback (T-RTR, T-DEC)

### Community 7 - "Security & Accessibility Compliance"
Cohesion: 0.50
Nodes (3): Security Controls Checklist (Secrets, Sandbox, ORM), WCAG 2.1 AA Accessibility & Responsive Standards, Test Suite: Security, Privacy & Accessibility (T-SEC, T-PRV, T-A11Y)

### Community 8 - "Provider & Usage Schema"
Cohesion: 0.50
Nodes (4): Database Table: model, Database Table: provider, Database Table: provider_state, Database Table: usage_ledger

### Community 9 - "Onboarding Wizard & Navigation"
Cohesion: 0.50
Nodes (4): Six-Screen First-Run Onboarding Flow, MargHire 28-Page Sitemap Architecture, Feature F14: First-Run Onboarding Wizard, TR-ONB-1: Onboarding Configuration Persistence

### Community 10 - "Application Tracking System"
Cohesion: 0.50
Nodes (4): Application Tracker Kanban & List Interface Spec, Phase 5: Drafts, Tracker, Dashboard & Job Sources, Feature F9: Application Tracker, TR-TRK-1: Application Timeline & Event Tracking

### Community 11 - "Decision Models & Evaluation"
Cohesion: 0.50
Nodes (3): Phase 0: Foundations, Evaluation Harness & Spike, Feature F12: Decision Models (Laya, Clef, Jev), Decision Model Architecture & Shuffling Strategy

### Community 12 - "Source Importers & Integrations"
Cohesion: 0.50
Nodes (4): Feature F2: Multi-Source Pool Importer, TR-POOL-2: Importer Plugin Interface Lifecycle, TR-POOL-3: LinkedIn ZIP Importer (No Core Scraping), TR-POOL-4: GitHub Sign-in with Private Repo Access

### Community 13 - "Mode A Resume Tailoring"
Cohesion: 0.67
Nodes (3): Tailor Diff Review Interface Spec, Feature F4: Mode A (Tracked Diff Resume Edit), TR-RES-2: Mode A Tracked Diff & In-Place Editing

### Community 14 - "MCP Server & Service Layer"
Cohesion: 0.67
Nodes (3): Phase 6: MCP Server & Open Documentation, Feature F13: MCP Server, Shared Service Layer (REST API & MCP Server)

### Community 38 - "package.json"
Cohesion: 0.05
Nodes (37): description, devDependencies, eslint@^9.0.0, @eslint/js@^9.0.0, license-checker@^25.0.1, prettier@^3.0.0, typescript@^5.5.0, typescript-eslint@^8.0.0 (+29 more)

### Community 39 - "api"
Cohesion: 0.07
Nodes (33): build, depends_on, environment, ports, restart, user, volumes, context (+25 more)

### Community 40 - "web/package.json"
Cohesion: 0.09
Nodes (26): dependencies, react@^18.3.0, react-dom@^18.3.0, devDependencies, @types/react@^18.3.0, @types/react-dom@^18.3.0, vite@^6.0.0, @vitejs/plugin-react@^4.3.0 (+18 more)

### Community 41 - "api/package.json"
Cohesion: 0.10
Nodes (19): dependencies, hono@^4.0.0, devDependencies, @types/node@^22.0.0, @types/node, name, private, scripts (+11 more)

### Community 42 - "db/package.json"
Cohesion: 0.11
Nodes (20): dependencies, drizzle-orm@^0.45.4, devDependencies, drizzle-kit@^0.31.0, @types/node@^22.0.0, exports, @types/node, name (+12 more)

### Community 43 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, composite, declaration, declarationMap, exactOptionalPropertyTypes, incremental, lib, module (+10 more)

### Community 44 - "mcp/package.json"
Cohesion: 0.15
Nodes (14): dependencies, @modelcontextprotocol/sdk@^1.0.0, devDependencies, @types/node@^22.0.0, @types/node, name, private, scripts (+6 more)

### Community 45 - "compilerOptions"
Cohesion: 0.13
Nodes (14): compilerOptions, emitDeclarationOnly, exactOptionalPropertyTypes, jsx, lib, module, moduleResolution, outDir (+6 more)

### Community 46 - "db"
Cohesion: 0.14
Nodes (14): environment, healthcheck, image, ports, restart, volumes, POSTGRES_DB, POSTGRES_PASSWORD (+6 more)

### Community 47 - "core/package.json"
Cohesion: 0.15
Nodes (13): devDependencies, @types/node@^22.0.0, exports, @types/node, name, private, scripts, build (+5 more)

### Community 48 - "providers/package.json"
Cohesion: 0.15
Nodes (13): devDependencies, @types/node@^22.0.0, exports, @types/node, name, private, scripts, build (+5 more)

### Community 49 - "sources/package.json"
Cohesion: 0.15
Nodes (13): devDependencies, @types/node@^22.0.0, exports, @types/node, name, private, scripts, build (+5 more)

### Community 51 - "MargHire"
Cohesion: 0.20
Nodes (9): Commands, Contributing, Development setup (without Docker), Licence, MargHire, Planning documents, Quick start, Repository layout (+1 more)

### Community 52 - "api/tsconfig.json"
Cohesion: 0.25
Nodes (7): compilerOptions, outDir, rootDir, extends, include, ../../tsconfig.json, references

### Community 53 - "mcp/tsconfig.json"
Cohesion: 0.25
Nodes (7): compilerOptions, outDir, rootDir, extends, include, ../../tsconfig.json, references

### Community 54 - "providers/tsconfig.json"
Cohesion: 0.25
Nodes (7): compilerOptions, outDir, rootDir, extends, include, ../../tsconfig.json, references

### Community 55 - "sources/tsconfig.json"
Cohesion: 0.25
Nodes (7): compilerOptions, outDir, rootDir, extends, include, ../../tsconfig.json, references

### Community 57 - "core/tsconfig.json"
Cohesion: 0.29
Nodes (6): compilerOptions, outDir, rootDir, extends, include, ../../tsconfig.json

### Community 58 - "db/tsconfig.json"
Cohesion: 0.29
Nodes (6): compilerOptions, outDir, rootDir, extends, include, ../../tsconfig.json

### Community 61 - "templates/package.json"
Cohesion: 0.40
Nodes (4): description, name, private, version

### Community 76 - "Role Lens Model Comparison Spike Report"
Cohesion: 0.29
Nodes (6): Architecture Decision & Recommendation, Benchmark Results, Executive Summary, Key Findings, Recommendation: **Hybrid Mode (Decision Model Default, LLM-Only Fallback)**, Role Lens Model Comparison Spike Report

## Knowledge Gaps
- **69 isolated node(s):** `../../tsconfig.json`, `../../tsconfig.json`, `../../tsconfig.json`, `../../tsconfig.json`, `../../tsconfig.json` (+64 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 356 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **44 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Pair` connect `Pair` to `_load_one`, `Adapter`, `schema.py`, `ClefAdapter`, `GeminiAdapter`, `LLMAdapter`, `.validate`, `run.py`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `Pair` (e.g. with `Adapter` and `ClefAdapter`) actually correct?**
  _`Pair` has 14 INFERRED edges - model-reasoned connections that need verification._
- **What connects `../../tsconfig.json`, `../../tsconfig.json`, `../../tsconfig.json` to the rest of the system?**
  _69 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Database Table: job` be split into smaller, more focused modules?**
  _Cohesion score 0.08695652173913043 - nodes in this community are weakly interconnected._
- **Why does `AdapterResult` connect `Pair` to `Adapter`, `schema.py`, `ClefAdapter`, `order_sensitivity`, `GeminiAdapter`, `LLMAdapter`, `run.py`?**
  _High betweenness centrality (0.009) - this node is a cross-community bridge._
- **Are the 12 inferred relationships involving `AdapterResult` (e.g. with `Adapter` and `ClefAdapter`) actually correct?**
  _`AdapterResult` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Should `Database Table: pool_item` be split into smaller, more focused modules?**
  _Cohesion score 0.14285714285714285 - nodes in this community are weakly interconnected._