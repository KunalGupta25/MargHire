# Evaluation pairs and benchmark dataset

This directory houses the synthetic benchmark fixtures used to evaluate MargHire's **Role Lens** engine across local and hosted decision models (including Clef-Flash, Gemini-Flash, Laya, and baseline stubs).

Each `.json` file in `pairs/` represents one evaluation unit consisting of:
1. A candidate's verified professional pool (skills, projects, work experience, education, certifications).
2. A realistic target job description (title and specification).
3. Ground-truth binary inclusion labels (`true` = should appear on tailored resume, `false` = should be excluded).

All public benchmark data is **100% synthetic**. No real candidate names, actual corporate employers, private repositories, or copyrighted resumes are stored or processed.

---

## 1. Provenance and privacy guardrails

MargHire adheres to strict privacy and non-fabrication principles (see `AGENTS.md` and `docs/MargHire Privacy, Security and Compliance Checklist.md`). The benchmark fixtures reflect these standards:

- **Origin & authorship**: Public pairs are procedurally synthesized and human-curated specifically for evaluating fresher resume tailoring. Every file records its provenance via the metadata fields:
  - `"created_by": "synthetic"`: Identifies the fixture as part of the public synthetic benchmark.
  - `"created_at": "YYYY-MM-DD"`: ISO-8601 date of synthesis and ground-truth verification.
- **Zero personal data**: Candidates, colleges, company names, and project titles are synthetic composites inspired by the Indian tech fresher ecosystem. They do not correspond to living individuals or private corporate codebases.
- **Auditable ground truth**: Every label has been assigned and reviewed against an explicit fresher-role labeling rubric (detailed in Section 3), ensuring deterministic, reproducible precision and recall measurements.
- **Private evaluation datasets**: Users wishing to run evaluations against proprietary, campus-specific, or personal resumes can do so without committing confidential records to source control. Set the `EVAL_PRIVATE_PAIRS_DIR` environment variable to a directory outside the repository:
  ```bash
  EVAL_PRIVATE_PAIRS_DIR=/path/to/private/pairs python -m eval.run --adapter clef-flash
  ```
  Private pairs are loaded and validated alongside public pairs, but remain isolated on the user's local disk.

---

## 2. Synthetic pair generation methodology

### 2.1 Target persona: The Indian IT fresher
The benchmark is tailored specifically to Indian engineering and design graduates (B.Tech, B.E., B.Des graduating batches 2022–2026) seeking entry-level software engineering, design, or data roles across:
- Indian product startups (fintech, quick commerce, healthtech, edtech, SaaS).
- Global Capability Centers (GCCs) and IT services companies.
- Technology studios and agile digital agencies.

A typical fresher profile has accumulated **10 to 14 pool items** across college years:
- 1–2 educational qualifications (degree, university/institute, CGPA).
- 1–2 internships (2 to 6 months duration) or academic capstone projects.
- 2–4 personal or hackathon software projects.
- 4–7 technical skills, frameworks, and developer tools.
- 1–3 non-technical, extracurricular, or hobby activities (e.g., cultural fest video editing, hobby robotics, sports fest management).

### 2.2 Job description synthesis
Job postings in the benchmark simulate realistic entry-level job descriptions encountered on Indian tech hiring channels (campus placement cells, AngelList/Wellfound, LinkedIn, Instahyre, Naukri). Each job description includes:
- Role title and organizational context.
- Explicit primary requirements (e.g., React 18, TypeScript, Node.js/Express, PyTorch, Docker).
- Secondary expectations (testing with Vitest/Pytest, SQL queries, RESTful design).
- Collaboration tooling (Git/GitHub, CI/CD, Agile).

### 2.3 Pool construction and distractor injection
For every pair, the candidate pool is populated with:
- **Core matches (50–65%)**: Items directly aligned with the core technical requirements of the job.
- **Supporting engineering items (15–25%)**: General engineering best practices (version control, automated testing, API validation) that strengthen a fresher resume.
- **Negative distractors (20–30%)**: Deliberately injected items that must be rejected by the Role Lens. These evaluate the decision model's ability to maintain high precision and avoid cluttering a single-page fresher resume with irrelevant skills.

---

## 3. Labeling taxonomy and selection criteria

The ground truth in `labels` reflects whether a professional recruiter or senior engineer would include an item on a tightly focused **one-page fresher resume** for the targeted role.

### 3.1 Positive selection criteria (`true`)
An item is labeled `true` if it meets any of the following conditions:

1. **Direct technical requirement match**:
   - The item explicitly demonstrates competence in a language, framework, database, or tool requested in the job description (e.g., `item-010-01` React 18 & TypeScript for a Junior React Frontend Developer role).
2. **Foundational software engineering hygiene**:
   - Core tools universal to modern engineering teams that hiring managers expect from IT graduates, provided they do not conflict with the role focus:
     - Version control (Git, GitHub pull request workflows).
     - Automated testing (Vitest, Jest, Pytest, Supertest).
     - REST API integration / OpenAPI / Zod schema validation.
3. **Primary qualifying education**:
   - The candidate's primary university degree (e.g., B.Tech in IT / Computer Science, B.Des Visual Communication) establishing basic eligibility for fresher recruitment drives.
4. **Relevant work experience & capstone projects**:
   - Internships, freelance contracts, or major academic/hackathon projects whose tech stack or domain aligns with the target job (e.g., an e-commerce cart project for a backend role).
5. **Directly adjacent design or engineering skills**:
   - Skills that provide direct synergistic value (e.g., WCAG accessibility auditing for frontend/design roles; Linux shell scripting for DevOps or backend roles).

### 3.2 Negative selection criteria (`false`)
An item is labeled `false` if it falls under any of the following categories:

1. **Cross-domain technical distractors**:
   - Technical competencies belonging to an entirely different engineering track with no relevance to the target job:
     - *Example*: Arduino / embedded C robotics hobby on a Junior UI/UX Designer resume (`item-001-10` in `pair-001.json`).
     - *Example*: PyTorch / YOLOv8 computer vision model on a Junior React Frontend resume (`item-010-11` in `pair-010.json`).
     - *Example*: Figma mobile UI layouts on a high-throughput Node.js backend resume (`item-019-08` in `pair-019.json`).
2. **Mismatched infrastructure or database depth**:
   - Heavy infrastructure or database operations on a specialized frontend or design profile where it distracts from core competencies:
     - *Example*: PostgreSQL schema migrations and multi-stage Docker deployment on a junior frontend UI posting (`item-010-09`, `item-010-10` in `pair-010.json`).
3. **Non-technical and extracurricular hobbies**:
   - Extracurricular, cultural, or social activities that add no signal to an engineering or product design evaluation:
     - *Example*: Editing promotional video reels for a college cultural festival (`item-045-11` in `pair-045.json`).
     - *Example*: Sports tournament coordination or high school club memberships.
4. **Obsolete, secondary school, or trivial coursework**:
   - Secondary school (10th/12th grade) certifications, outdated tools, or trivial classroom exercises with negligible engineering substance.

### 3.3 Fresher-specific edge-case rules
- **Generalist vs. Specialized Roles**: For generalist roles (e.g., Full Stack Fresher, Software Engineer Trainee in `pair-045` to `pair-050`), items spanning both frontend and backend are labeled `true`, but non-software hardware (Arduino) or media hobbies remain `false`.
- **Limited Pool Size**: When a candidate pool has fewer than 10 items, standard engineering hygiene items (Git, basic SQL) are kept as `true` to ensure the candidate has sufficient substance for a full page.
- **Unverified Claims**: In the MargHire system, only items with `verified = true` are supplied to the Role Lens. All benchmark items represent verified pool facts; the model's job is purely relevance selection.

---

## 4. Dataset composition and role families

The 50 synthetic benchmark pairs are partitioned into 6 role families covering the primary hiring tracks for Indian freshers:

| Family | Pair IDs | Target Roles | Core Technologies Evaluated |
|---|---|---|---|
| **Designer** | `pair-001` – `pair-009` | Junior UI/UX Designer, Product Design Intern, Interaction Designer | Figma, user research, wireframing, WCAG accessibility, design systems, usability testing |
| **Frontend** | `pair-010` – `pair-018` | Junior Frontend Developer, React Developer, Web UI Engineer | React 18, TypeScript, Next.js, Tailwind CSS, Zustand/Redux, Vitest, HTML5/CSS3 |
| **Backend** | `pair-019` – `pair-027` | Junior Backend Developer, Node.js Engineer, Python/FastAPI Associate | Node.js, Express, PostgreSQL, Prisma, Redis, REST APIs, JWT authentication, Docker |
| **AI / ML** | `pair-028` – `pair-036` | Junior ML Engineer, Data Science Intern, Computer Vision / NLP Fresher | Python, PyTorch, Scikit-learn, Pandas, Hugging Face transformers, FastAPI, NumPy |
| **Cloud / DevOps** | `pair-037` – `pair-044` | Cloud Engineer Trainee, Junior DevOps Engineer, Site Reliability Intern | AWS (S3, EC2, Lambda), Docker, Terraform, GitHub Actions, Linux/Bash, Kubernetes |
| **Mixed / Generalist**| `pair-045` – `pair-050` | Full Stack Developer Fresher (MERN), Software Engineer Trainee | Full-stack JavaScript/TypeScript, React, Node.js, MongoDB/PostgreSQL, Git, Postman |

### Aggregate metrics & label distribution:
- **Total evaluation pairs**: 50
- **Total pool items evaluated**: ~580 items across all pairs
- **Mean items per pool**: 11.6 items
- **Positive label ratio**: ~74% (reflecting realistic fresher selection where ~8–9 relevant items out of 12 are selected to populate a standard 1-page resume template)
- **Negative distractor ratio**: ~26% (evaluates precision and distractor rejection)

---

## 5. Schema specification

Each pair file adheres to the following JSON schema:

```json
{
  "id": "pair-001",
  "created_by": "synthetic",
  "created_at": "2026-11-10",
  "job": {
    "title": "Junior UI/UX Designer",
    "description": "Full job description text detailing responsibilities and required qualifications."
  },
  "pool": [
    {
      "id": "item-001-01",
      "kind": "skill | project | work | education | certification | publication",
      "text": "Specific, factual description of candidate experience or capability.",
      "tags": ["tag1", "tag2"]
    }
  ],
  "labels": {
    "item-001-01": true,
    "item-001-02": false
  }
}
```

### Schema invariants:
1. **Bijective key mapping**: Every `id` in `pool` must appear as a key in `labels`, and `labels` must not contain IDs absent from `pool`.
2. **Strict boolean values**: Every label value must be a strict JSON boolean (`true` or `false`).
3. **Valid item kinds**: `kind` must be one of `"skill"`, `"project"`, `"work"`, `"education"`, `"certification"`, or `"publication"`.
4. **ISO-8601 timestamps**: `created_at` must follow `YYYY-MM-DD` or full ISO-8601 formatting.
5. **No empty strings**: `id`, `job.title`, `job.description`, and `pool[].text` must not be blank.

---

## 6. Validation guidelines

All pairs must pass programmatic schema and semantic integrity checks before being utilized for model evaluations or committed to version control.

### 6.1 Automated validation via pytest
The test suite validates all public and private pairs automatically:

```bash
# Run loader and schema validation tests
python -m pytest python/eval/test_loader.py -v
```

This ensures:
- JSON syntactical validity.
- Schema conformity (via `Pair.validate()` in `python/eval/schema.py`).
- Absence of orphaned labels or missing pool item labels.
- Global uniqueness of pair IDs.

### 6.2 Manual validation script
You can validate the entire pair directory from Python directly:

```python
from eval.loader import load_pairs

# Raises ValueError on the first invalid pair encountered
pairs = load_pairs()
print(f"Successfully validated {len(pairs)} evaluation pairs.")
```

### 6.3 Adding or editing benchmark pairs
When contributing new pairs:
1. Follow the naming convention `pair-XXX.json` with contiguous 3-digit identifiers.
2. Ensure the candidate persona matches an Indian fresher graduating cohort.
3. Inject 2 to 4 realistic distractors (cross-domain or non-technical hobby) to stress-test model precision.
4. Set `"created_by": "synthetic"` and `"created_at"` to the current ISO-8601 date.
5. Verify that `python -m pytest python/eval/test_loader.py` passes cleanly.
