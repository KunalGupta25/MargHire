# MargHire: Data Privacy, Security and Compliance Checklist

Nov 10, 2026 · @Kunal Gupta

## Scope, data inventory and threats

MargHire stores a person's career history, contact details and provider API keys on the user's own machine. The main risks are a leaked API key, personal data sent to a provider the user did not intend, and a plugin or dependency that misbehaves. Tick each item when it is built and tested.

| Data | Where it lives | Sensitivity |
| --- | --- | --- |
| Profile: name, email, phone, location, links | Database | Personal data |
| Pool items, resumes, drafts | Database and files | Personal data |
| Uploaded resumes and LinkedIn export | Files on disk | Personal data; may contain more than needed |
| Provider API keys and tokens | Encrypted in database or environment | Secret |
| Job descriptions and company notes | Database | Low |
| Usage ledger | Database | Low |

**Data that leaves the machine:** only text sent to AI providers the user enabled, and requests to job and profile sources the user enabled. Nothing is sent to MargHire's authors; there is no telemetry in v1.

## Security checklist

**Secrets**

- [ ] API keys are encrypted at rest with a key from the environment, or stored only as an environment-variable reference.
- [ ] Keys are never written to logs, error messages, exports, the audit log or MCP tool output.
- [ ] `.env`, the data directory and uploaded files are in `.gitignore`; a secret scanner runs in CI.
- [ ] Keys are masked in the UI after saving; only replaced, never shown again.

**Access**

- [ ] The server binds to localhost by default; exposing it needs an explicit setting and a warning.
- [ ] Optional local password uses a slow password hash (argon2 or bcrypt) and rate-limits attempts.
- [ ] MCP and API tokens are random, revocable and scoped read-only or read-write.
- [ ] State-changing MCP tools require an explicit confirmation argument.

**Input and output**

- [ ] Uploaded files are size-limited, type-checked and parsed in a sandboxed process.
- [ ] Job descriptions and imported text are treated as untrusted: they cannot change instructions given to the model (prompt-injection handling), and tool calls triggered by them need user approval.
- [ ] Resume rendering runs with a time limit, no network and no shell escape. LaTeX shell-escape is disabled.
- [ ] All database access uses parameterised queries through the ORM.
- [ ] Output shown in the UI is escaped; the generated PDF is never executed.

**Network**

- [ ] Outbound calls go only to hosts of providers and sources the user enabled.
- [ ] TLS verification is never disabled.
- [ ] Provider and source calls have timeouts and size limits.

**Supply chain and plugins**

- [ ] Dependencies are pinned by lockfile; an audit and licence check run in CI.
- [ ] Plugins run with the least access they need, and risky ones (aggregators) are off by default with a visible risk badge.
- [ ] Docker images run as a non-root user with a read-only filesystem where possible.

**Backups and recovery**

- [ ] One-click export of all data; backups are encrypted or clearly marked as containing personal data.

## Privacy checklist

- [ ] Before the first call to any provider, the UI says what text will be sent (resume content, job description, contact details) and to whom.
- [ ] Data minimisation: prompts include only the pool items needed for the task; contact details are added at render time, not sent to the model, unless a draft needs them.
- [ ] Each provider shows whether it is local, free tier or paid, and links to its own data-use policy. The user is told that free tiers may use inputs differently from paid ones; check each provider's terms.
- [ ] GitHub connects through GitHub sign-in and imports private repos by default. The user sees which repos were read and can exclude any.
- [ ] Imported LinkedIn exports are parsed for the user's own profile only; connections and messages files are ignored and not stored.
- [ ] Aggregator plugins fetch the user's own profile only (self-only guard).
- [ ] The user can export all data in an open format (JSON Resume plus JSON for the rest).
- [ ] "Erase my data" removes database rows, uploaded files, rendered PDFs and cached model outputs, and confirms what was removed.
- [ ] Contact details of third parties (HR contacts) are only those the user entered or found through allowed sources, with a note of the source.
- [ ] No telemetry or analytics in v1. If added later, opt-in only.

## Legal and compliance checklist

This is a working checklist, not legal advice. Get a lawyer's review before anyone hosts MargHire for other people.

| Area | Requirement | Status |
| --- | --- | --- |
| LinkedIn terms | No scraping in core. Use the data export; any official API only after confirming access for India. | Open |
| Naukri terms | Naukri's terms prohibit scraping; no Naukri scraper in the main repo. | Open |
| Aggregator plugins | Off by default, self-profile only, user brings own account and key, clear warning on enable. | Open |
| Job sources | Use public JSON from Greenhouse, Lever and Ashby, and official APIs (Adzuna, Jooble, Careerjet) within their terms and rate limits. | Open |
| DPDP Rules 2025 | The main obligations start 13 May 2027. Personal use on one's own data is lighter; revisit if hosted for others (consent notice, purpose limits, erasure, breach handling). | Open |
| Licence | AGPL-3.0 for MargHire. Check that every dependency and every model licence is compatible; Laya and the Clef weights are Apache-2.0. | Open |
| AI-generated content | The user is responsible for what they send. The truthfulness check helps, but the UI says the user must review every document. | Open |
| Trademark and name | Search IP India, GitHub, PyPI, npm and domains for MargHire before launch; near names exist. | Open |
| Repo hygiene | Fake data only in fixtures; no real personal data or keys in git history. | Open |

## Open items to verify

- [ ] Whether LinkedIn's Member Data Portability API is available for accounts in India.
- [ ] Each provider's current data-retention and training terms for free tiers.
- [ ] Whether Cloudflare Workers AI retains prompts, and for how long.
- [ ] DPDP applicability if a friend or college hosts MargHire for others.
- [ ] Whether storing a recruiter's name and email, entered by the user, needs a notice under DPDP.
- [ ] Name clearance on IP India.

* [ ] Whether private repo contents may be sent to free-tier AI providers, since private repos are now imported by default.
* [ ] Which GitHub sign-in permissions are needed to read private repos, and whether a narrower scope is enough.
