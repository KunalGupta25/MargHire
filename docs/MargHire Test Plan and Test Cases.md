# MargHire: Test Plan and Test Cases

Nov 10, 2026 · @Kunal Gupta

## Test strategy, levels and CI gates

| Level | Tool | What it covers | Runs |
| --- | --- | --- | --- |
| Unit | Vitest (TypeScript), pytest (Python) | Pure logic: scoring, dedupe, parsers, router policy, truthfulness check | Every commit |
| Integration | Vitest with a test database | API and service layer against SQLite and Postgres; importers against recorded responses | Every pull request |
| Contract | Recorded provider responses | Each provider adapter against sample success and error replies | Every pull request |
| Evaluation | Python scripts | Role Lens quality and decision-model comparison on the labelled set | Before a release and when models change |
| End to end | Playwright | Onboarding, core loop, tracker, in a browser against the Docker stack | Every pull request (short set), nightly (full) |
| Security and accessibility | Dependency audit, secret scan, axe checks | See the security checklist | Every pull request |

**CI gates (a pull request cannot merge unless):** lint and type-check pass; unit, integration and contract tests pass on both SQLite and Postgres; no new high-severity audit findings; secret scan is clean; licence check passes; migrations apply cleanly from empty and from the previous release.

## Test data policy and the evaluation set

### Test data policy and privacy guardrails
- **Zero personal data**: Fixtures and benchmark suites use fake candidates, companies, and repositories only. Real resumes, personal phone numbers, emails, and API keys never enter the repo or CI.
- **Scrubbed recorded responses**: Recorded provider responses used for contract and unit tests are scrubbed of personal data and credentials before being committed.
- **Private evaluation isolation**: Evaluators testing against proprietary or personal candidate resumes must keep those files in a directory outside the repository using `EVAL_PRIVATE_PAIRS_DIR`. Private results are excluded from version control via `.gitignore`.

### Dataset specifications
The Phase 0 benchmark dataset resides in `python/eval/data/pairs/` and contains **50 synthetic evaluation pairs** (~580 total pool items, averaging 11.6 items per candidate) partitioned across 6 fresher role families:

| Family | Pair Range | Target Roles | Core Tech & Competencies Evaluated |
| --- | --- | --- | --- |
| **Designer** | `pair-001` – `pair-009` | Junior UI/UX Designer, Product Design Intern | Figma, wireframing, user research, WCAG accessibility, design systems, usability testing |
| **Frontend** | `pair-010` – `pair-018` | Junior Frontend Developer, React Developer | React 18, TypeScript, Next.js, Tailwind CSS, Zustand, Vitest/RTL, HTML5/CSS3 |
| **Backend** | `pair-019` – `pair-027` | Junior Backend Developer, Node.js Engineer | Node.js, Express, PostgreSQL, Prisma, Redis caching, JWT auth, REST APIs, Docker |
| **AI / ML** | `pair-028` – `pair-036` | Junior ML Engineer, Data Science Intern | Python, PyTorch, Scikit-learn, Pandas, Hugging Face transformers, FastAPI, NumPy |
| **Cloud / DevOps** | `pair-037` – `pair-044` | Cloud Engineer Trainee, Junior DevOps Intern | AWS (S3, EC2, Lambda), Docker, Terraform, GitHub Actions, Linux/Bash, Kubernetes |
| **Mixed / Generalist** | `pair-045` – `pair-050` | Full Stack Developer Fresher (MERN), SE Trainee | Full-stack MERN, React, Node.js, MongoDB, REST integration, Git, Postman |

### Synthetic labeling methodology and provenance
- **Target persona**: The dataset models the profile of Indian IT freshers (B.Tech, B.E., B.Des graduating batches 2022–2026) applying to campus placements and entry-level junior positions across startups, GCCs, and IT services.
- **Label provenance**: Public benchmark pairs carry immutable provenance metadata (`"created_by": "synthetic"` and ISO-8601 `"created_at": "2026-11-10"`). Ground-truth inclusion labels (`labels: { "<item_id>": true/false }`) are hand-curated and audited against a deterministic labeling taxonomy.
- **Labeling taxonomy & selection criteria**:
  - **Positive selection (`true`, ~74% of items)**:
    - *Direct technical match*: Languages, frameworks, and databases explicitly required by the job posting.
    - *Core engineering hygiene*: Universal fresher practices including version control (Git/GitHub), automated unit/integration testing (Vitest, Jest, Pytest), and REST API integration.
    - *Qualifying education*: Relevant degree (B.Tech CSE/IT, B.Des) and CGPA confirming eligibility.
    - *Domain-aligned experience*: Internships and capstones demonstrating practical application of the target stack.
  - **Negative selection / Distractor rejection (`false`, ~26% of items)**:
    - *Cross-domain technical distractors*: Technical skills from unrelated domains (e.g., embedded Arduino robotics on a UI/UX or React resume; PyTorch computer vision on a pure frontend role; Figma UI design on a high-throughput backend role).
    - *Mismatched stack depth*: Complex infrastructure or database items injected into frontend-specific roles that dilute relevance.
    - *Non-technical & extracurricular activities*: College fest promotional video editing, cultural club management, or sports fest coordination.
    - *Pre-college / obsolete entries*: High school achievements or outdated tools.
- **Integrity verification**: Pairs enforce a strict bijective mapping between `pool` items and `labels` keys, verified automatically via `Pair.validate()` and CI unit test `python -m pytest python/eval/test_loader.py`.
- **Results provenance**: Public benchmark run summaries are committed to `python/eval/results/` (`*.json`), while private test runs (`*private*`, `*.private.*`, `private/`) remain ignored by git.

**Metrics for Role Lens**

| Metric | Meaning | Target |
| --- | --- | --- |
| Precision | Of items kept, how many a human also kept | Set after the Phase 0 run |
| Recall | Of items a human kept, how many were kept | Set after the Phase 0 run |
| Order sensitivity | Change in picks when option order is shuffled | Report; lower is better |
| Cost and latency | Per resume, by provider | Report |
| Truthfulness | Generated claims not in the pool | Must be zero for export |

Targets for precision and recall are left open on purpose: set them from the Phase 0 numbers, not from a guess.

## Test cases by module

| ID | Module | Case | Expected |
| --- | --- | --- | --- |
| T-POOL-1 | Pool | Create, edit, delete an item | Saved; revision recorded; soft delete hides it |
| T-POOL-2 | Pool | Import creates items | All have `verified = false` and a source |
| T-POOL-3 | Pool | Verify an item | It becomes eligible for Role Lens |
| T-IMP-1 | LinkedIn ZIP | Upload a sample export | Positions, education and skills imported; connections and messages ignored |
| T-IMP-2 | GitHub | Import a fake user with private repos | Private repos are imported, and the user sees which repos were read |
| T-IMP-3 | GitHub | Hit the rate limit | Waits per headers, import resumes, no duplicates |
| T-IMP-4 | Resume upload | PDF, DOCX, TeX and JSON Resume samples | Parsed into JSON Resume; original file untouched |
| T-IMP-5 | Any source | Same item arrives from two sources | One item, two evidence links; conflicts go to the Review queue |
| T-LENS-1 | Role Lens | Designer job on a mixed pool | Design items rank above backend and cloud items |
| T-LENS-2 | Role Lens | Backend job on the same pool | Result differs from T-LENS-1 as expected |
| T-LENS-3 | Role Lens | Only unverified items exist | No pool items are selected; About me is still written from basic details and the job description; user is prompted to verify |
| T-LENS-4 | Role Lens | Low confidence | Falls back to the LLM, then asks the user |
| T-LENS-5 | Role Lens | Shuffle option order | Picks stay stable within the allowed margin |
| T-TRUTH-1 | Truthfulness | LLM adds a skill not in the pool | Flagged; export blocked |
| T-TRUTH-2 | Truthfulness | LLM changes a number or date | Flagged |
| T-TRUTH-3 | Truthfulness | Reworded bullet with the same facts | Passes |
| T-RES-1 | Mode B | Generate for a pasted job | JSON Resume built; PDF renders |
| T-RES-2 | Mode A | Edit an uploaded `.tex` | Change list shown; only accepted changes applied; layout kept |
| T-RES-3 | Mode A | Edit an uploaded PDF | Re-rendered in a template; user warned about layout |
| T-RES-4 | Rendering | Malformed LaTeX input | Compile error shown with the source line; no crash |
| T-RES-5 | ATS check | Extract text from the PDF | Headings and order read cleanly in one column, and an ATS score is shown |
| T-DRAFT-1 | Drafts | Cover letter and HR email for a job | Uses only pool facts; editable; saved |
| T-TRK-1 | Tracker | Create an application, change status | Events recorded in order |
| T-TRK-2 | Tracker | Second application for the same job | Refused |
| T-JOB-1 | Jobs | Same job from two sources | Deduped to one |
| T-JOB-2 | Jobs | Snippet-only description | Marked `snippet`; analysis warns of low quality |

## Provider router and decision-model failure tests

A test script force-fails each provider with each condition below and checks the router's behaviour.

| ID | Condition | Expected |
| --- | --- | --- |
| T-RTR-1 | 429 with `Retry-After` | Waits or moves to next provider; ledger records the event |
| T-RTR-2 | 5xx or timeout | One retry with backoff, then next provider |
| T-RTR-3 | 401 or 403 (bad key) | Next provider is tried; a warning afterwards names the provider and the reason |
| T-RTR-4 | 400 (bad model ID) | Next provider is tried; the warning names the bad model ID |
| T-RTR-5 | Repeated failures | Circuit opens; provider skipped until cool-down ends |
| T-RTR-6 | All providers fail | Task fails cleanly; no data lost; user sees which providers failed and why |
| T-RTR-7 | Cloudflare at its daily Neuron count | Router moves on before an error; counter resets at 00:00 UTC |
| T-RTR-8 | Paid provider, budget reached | Call blocked; free chain continues |
| T-RTR-9 | Free-first strategy | Local and free providers tried before paid |
| T-RTR-10 | Fetch models | Provider list returned; nothing saved until selected; failure offers manual entry |
| T-RTR-11 | Manual model add and edit | Saved; appears in chains; removable |
| T-DEC-1 | Decision + LLM mode, model not marked as decision model | It is never used for decision tasks |
| T-DEC-2 | Provider's "also use for decision models" off | Its models are ignored for decisions even if marked |
| T-DEC-3 | Decision model unavailable or limited | Task runs on the LLM chain |
| T-DEC-4 | LLM-only mode | No decision-model call is made |
| T-DEC-5 | More than about 20 options | Options split into groups |
| T-DEC-6 | Confidence below threshold | Falls back to LLM, then to the user |

## Security, privacy and accessibility tests

| ID | Area | Case | Expected |
| --- | --- | --- | --- |
| T-SEC-1 | Secrets | Search logs, errors, exports and MCP output after saving a key | The key never appears |
| T-SEC-2 | Secrets | Read the database | Keys are encrypted or only references |
| T-SEC-3 | Access | Start with defaults | Listens on localhost only |
| T-SEC-4 | MCP | State-changing tool without confirmation argument | Refused |
| T-SEC-5 | Input | Job description containing instructions to the model | Ignored; no tool call without user approval |
| T-SEC-6 | Input | Oversized or malformed upload | Rejected safely |
| T-SEC-7 | Rendering | LaTeX with shell-escape commands | Blocked |
| T-SEC-8 | Network | Request to a host not enabled by the user | Blocked |
| T-PRV-1 | Erase | Run "Erase my data" | Rows, uploads, PDFs and cached outputs are gone; confirmation lists them |
| T-PRV-2 | Export | Export all data | Open-format archive; re-importable |
| T-PRV-3 | Consent | First call to a provider | User is told what is sent and to whom |
| T-A11Y-1 | Keyboard | Complete onboarding with keyboard only | Possible, with visible focus |
| T-A11Y-2 | Contrast | Automated check on all screens | No AA failures |
| T-A11Y-3 | Modals | Open and close the Fetch models popup | Focus trapped and returned; Escape closes |
| T-A11Y-4 | Targets | Measure interactive elements | At least 44px |

## End-to-end scenarios and release acceptance

**Scenarios**

1. **First run, LLM only.** Onboard with one free provider, import a resume, paste a job, generate Mode B, download the PDF.
2. **First run, decision + LLM.** Add Cloudflare and mark Clef-flash as a decision model; same flow; the Role Lens panel shows which model decided.
3. **Mode A.** Upload a `.tex` resume, tailor it for a job, accept some changes and reject others, export.
4. **Fallback in the middle of a task.** Force a rate limit on the first provider during generation; the task finishes on the next one.
5. **Apply and track.** Create a cover letter and HR email, mark the job applied, see it in the Tracker and Companies.
6. **MCP.** From an external agent, list the pool, build a resume, log the application.
7. **Erase.** Run erase-all and confirm nothing remains.

**Release acceptance:** all scenarios pass; every P0 requirement in the PRD has at least one passing test; security and accessibility checklists are fully ticked for the released scope; no open high-severity bugs; Phase 0 and Phase 7 results are documented, with any claim about ATS behaviour backed by a test on real postings.
