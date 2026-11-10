# Graph Report - MargHire  (2026-11-10)

## Corpus Check
- Corpus is ~12,667 words - fits in a single context window. You may not need a graph.

## Summary
- 108 nodes · 74 edges · 38 communities (15 shown, 23 thin omitted)
- Extraction: 76% EXTRACTED · 24% INFERRED · 0% AMBIGUOUS · INFERRED: 18 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Job Application Schema
- Core Rules & UX Principles
- Data Pool & Architecture
- Data Provenance Schema
- Resume Generation & Templates
- Role Lens & Truthfulness
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

## God Nodes (most connected - your core abstractions)
1. `Database Table: pool_item` - 6 edges
2. `Database Table: job` - 5 edges
3. `Rule 1: Nothing Invented` - 4 edges
4. `TR-POOL-1: Pool Schema Storage and Default Verification` - 4 edges
5. `Definition of Done (AGENTS)` - 3 edges
6. `Feature F1: Professional Data Pool` - 3 edges
7. `Feature F2: Multi-Source Pool Importer` - 3 edges
8. `Feature F3: Role Lens Scoring and Selection` - 3 edges
9. `Feature F6: Resume Output & PDF Rendering` - 3 edges
10. `TR-RES-3: Sandboxed Tectonic & Typst PDF Compilation` - 3 edges

## Surprising Connections (you probably didn't know these)
- `Implementation Plan: Definition of Done` --semantically_similar_to--> `Definition of Done (AGENTS)`  [INFERRED] [semantically similar]
  docs/MargHire Implementation Plan and Build Order.md → AGENTS.md
- `Rule 1: Nothing Invented` --rationale_for--> `Truthfulness Verification Engine`  [INFERRED]
  AGENTS.md → docs/MargHire Technical Requirements (TRD SRS).md
- `Rule 9: Dual-Database Schema & UUIDs` --rationale_for--> `Database Table: pool_item`  [INFERRED]
  AGENTS.md → docs/MargHire Database Schema and Data Blueprint.md
- `Rule 2: Verified Items Only` --rationale_for--> `TR-POOL-1: Pool Schema Storage and Default Verification`  [INFERRED]
  AGENTS.md → docs/MargHire Technical Requirements (TRD SRS).md
- `Rule 3: Secrets Protection` --conceptually_related_to--> `Security Controls Checklist (Secrets, Sandbox, ORM)`  [INFERRED]
  AGENTS.md → docs/MargHire Data Privacy, Security and Compliance Checklist.md

## Hyperedges (group relationships)
- **Verified Resume Tailoring Pipeline** — docs_marghire_product_requirements_document_feature_f1, docs_marghire_product_requirements_document_feature_f3, docs_marghire_technical_requirements_trd_srs_truthfulness_checker, docs_marghire_technical_requirements_trd_srs_tr_res_1 [EXTRACTED 1.00]
- **Provider Router Resilience & Fallback Engine** — agents_rule_router_owns_fallback, docs_marghire_product_requirements_document_feature_f11, docs_marghire_technical_requirements_trd_srs_provider_router_spec, docs_marghire_database_schema_and_data_blueprint_table_usage_ledger [INFERRED 0.95]
- **Zero-Trust Verification and Secrets Perimeter** — agents_rule_verified_only, agents_rule_nothing_invented, agents_rule_secrets, docs_marghire_data_privacy_security_and_compliance_checklist_security_checklist [INFERRED 0.95]

## Communities (38 total, 23 thin omitted)

### Community 0 - "Job Application Schema"
Cohesion: 0.22
Nodes (10): Database Table: application, Database Table: application_event, Database Table: company, Database Table: job, Database Table: job_analysis, Database Table: resume, Database Table: resume_change, Database Table: resume_version (+2 more)

### Community 1 - "Core Rules & UX Principles"
Cohesion: 0.25
Nodes (4): Claude Agent Integration & AGENTS.md Inclusion, Ponytail Code-Reuse Skill, Privacy Controls Checklist (Minimisation, Erasure, No Telemetry), Multi-Level Test Strategy & CI Quality Gates

### Community 2 - "Data Pool & Architecture"
Cohesion: 0.29
Nodes (6): MargHire Repository Architecture Layout, Graphify Knowledge Graph Skill, Phase 1: Pool Schema, Upload & Connected Sources, Feature F1: Professional Data Pool, TR-POOL-1: Pool Schema Storage and Default Verification, Test Suite: Pool and Importers (T-POOL, T-IMP)

### Community 3 - "Data Provenance Schema"
Cohesion: 0.29
Nodes (6): Database Table: evidence, Database Table: import_run, Database Table: item_revision, Database Table: pool_bullet, Database Table: pool_item, Database Table: source

### Community 4 - "Resume Generation & Templates"
Cohesion: 0.29
Nodes (7): Resume Editor Three-Pane Interface Spec, Phase 4: LaTeX/Typst Templates & ATS Scoring, Feature F5: Mode B (Pool-to-Resume Generation), Feature F6: Resume Output & PDF Rendering, TR-RES-1: Mode B Resume Generation to Template, TR-RES-3: Sandboxed Tectonic & Typst PDF Compilation, Test Suite: Resume Engines & Rendering (T-RES)

### Community 5 - "Role Lens & Truthfulness"
Cohesion: 0.33
Nodes (6): Phase 3: Role Lens, Truthfulness & Resumes, Feature F3: Role Lens Scoring and Selection, TR-LENS-1: Role Lens Scoring, Ranking & Explanations, TR-LENS-2: Sentence-Level Truthfulness Enforcement, Truthfulness Verification Engine, Test Suite: Role Lens and Truthfulness (T-LENS, T-TRUTH)

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

## Knowledge Gaps
- **61 isolated node(s):** `Claude Agent Integration & AGENTS.md Inclusion`, `Graphify Knowledge Graph Skill`, `Claude Code Working Practices`, `Feature F4: Mode A (Tracked Diff Resume Edit)`, `Feature F5: Mode B (Pool-to-Resume Generation)` (+56 more)
  These have ≤1 connection - possible missing edges. (Counts symbols only; 73 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **23 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Truthfulness Verification Engine` connect `Role Lens & Truthfulness` to `Core Rules & UX Principles`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `Database Table: pool_item` (e.g. with `Rule 9: Dual-Database Schema & UUIDs` and `TR-POOL-1: Pool Schema Storage and Default Verification`) actually correct?**
  _`Database Table: pool_item` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Claude Agent Integration & AGENTS.md Inclusion`, `Graphify Knowledge Graph Skill`, `Claude Code Working Practices` to the rest of the system?**
  _61 weakly-connected nodes found - possible missing edges._
- **Why does `TR-LENS-1: Role Lens Scoring, Ranking & Explanations` connect `Role Lens & Truthfulness` to `Job Application Schema`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `TR-POOL-1: Pool Schema Storage and Default Verification` (e.g. with `Rule 2: Verified Items Only` and `Database Table: pool_item`) actually correct?**
  _`TR-POOL-1: Pool Schema Storage and Default Verification` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `Definition of Done (AGENTS)` (e.g. with `Ponytail Code-Reuse Skill` and `Implementation Plan: Definition of Done`) actually correct?**
  _`Definition of Done (AGENTS)` has 3 INFERRED edges - model-reasoned connections that need verification._