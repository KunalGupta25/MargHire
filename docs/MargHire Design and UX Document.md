# MargHire: Design and UX Document

Nov 10, 2026 · @Kunal Gupta

## Design principles and visual language

The interface should feel calm and trustworthy, since users are putting their career data into it. The onboarding canvas is the visual reference for the rest of the app.

**Principles**

- **Show the reason.** Every pick Role Lens makes shows why an item was kept or dropped.
- **Nothing invented.** Unverified items are visibly marked and never reach a resume without the user's say.
- **Free first.** Free and local options come first on every provider and model list; paid ones are labelled.
- **Always recoverable.** Every generation is a saved version; every import can be reviewed or undone.
- **Plain language.** Short labels, no jargon, no model names without a one-line explanation.

**Visual language** (from the onboarding canvas)

| Token | Value | Use |
| --- | --- | --- |
| Ground | `#FAF8F4` | Page background |
| Rail | `#F1EEE6` | Side navigation, quiet panels |
| Surface | `#FFFFFF` | Cards and inputs |
| Ink | `#16181D` | Body text |
| Muted | `#5B606B` | Secondary text |
| Line | `#E4DFD5` | Borders |
| Accent | `#0B6E6E` | Primary buttons, selected state, links |
| Saffron | `#B45309` | Badges such as Recommended and Paid |

Fonts are Inter for text and Space Grotesk for headings. A dark theme is a later addition; define every colour as a token from the start so it is a swap, not a rewrite.

## Sitemap: 28 pages

The phase column uses the build phases in the implementation plan (0 to 7). All 28 pages are in the first usable version. The MVP column shows build order: Yes means build first.

| # | Group | Page | Purpose | Phase | MVP |
| --- | --- | --- | --- | --- | --- |
| 1 | Entry | Login | Optional local password | 2 |  |
| 2 | Entry | Setup wizard | First run: decision models, AI providers, profile sources, resume mode | 2 |  |
| 3 | Entry | Dashboard | Pipeline summary, follow-ups, provider quota, recent resumes | 5 |  |
| 4 | Pool | Pool | Tabs for about, experience, education, projects, skills, certifications. Verified badge | 1 | Yes |
| 5 | Pool | Item detail | Source, evidence links, role tags, edit history | 1 | Yes |
| 6 | Pool | Review queue | Unverified imports and conflicts | 1 | Yes |
| 7 | Imports | Import center | LinkedIn ZIP, resume upload, GitHub, Hugging Face, GitLab, manual | 1 | Yes |
| 8 | Imports | Plugins | Source plugins with tier, risk badge, key, quota. Off by default | 1 and 5 |  |
| 9 | Jobs | Job search | Search enabled sources, deduped results, India defaults | 5 |  |
| 10 | Jobs | Add job | Paste a URL or description | 3 | Yes |
| 11 | Jobs | Job detail | Parsed requirements, fit score, description quality, actions | 3 | Yes |
| 12 | Resumes | Resume library | Versions, which job each went to, original uploads | 3 | Yes |
| 13 | Resumes | New resume wizard | Pick job, Mode A or B, template | 3 | Yes |
| 14 | Resumes | Resume editor | Visual editor, live PDF preview, Role Lens side panel | 3 and 4 | Yes |
| 15 | Resumes | Tailor diff review | Mode A accept or reject each change | 3 | Yes |
| 16 | Resumes | Templates and ATS score | Template picker and ATS score report | 4 |  |
| 17 | Applications | Application kit | Resume, cover letter, HR email together; `.eml` and PDF export | 5 |  |
| 18 | Applications | Tracker | Board and list: saved, applied, interview, offer, rejected | 5 |  |
| 19 | Applications | Application detail | Timeline, notes, resume version sent, job snapshot, reminders | 5 |  |
| 20 | Applications | Companies | Companies applied to, with ATS type | 5 |  |
| 21 | AI | Providers | Add providers, fetch or add models, tier tags, keys, test | 2 | Yes |
| 22 | AI | Chains and modes | Fallback chains; Decision + LLM or LLM only | 2 | Yes |
| 23 | AI | Usage and budget | Ledger, Cloudflare daily Neuron counter, spend caps | 2 |  |
| 24 | AI | Decision lab | Compare decision models on a question | 0 and 3 |  |
| 25 | System | MCP and API | Server status, tokens, tools, copy-paste client configs | 6 |  |
| 26 | System | Settings | General, privacy, backup and export, delete all data | 2 | Yes |
| 27 | System | Activity log | Provider calls, fallbacks, errors | 2 |  |
| 28 | System | Help and about | Self-hosting notes, legal notices, licence | 6 |  |

Pages that can merge if the scope needs trimming: 5 into 4, 6 into 7, 27 into 23, and 28 into 26.

## Onboarding screens

The visual design is on the [MargHire Onboarding canvas](https://claude.ai/artifact/9ssjuZQjSzvrK6c5Cgubfu). Order: Welcome, Decision models, AI providers, Profile sources, Resume mode, Ready. This section records the behaviour behind each screen.

| Step | Behaviour | Rules |
| --- | --- | --- |
| 1 Welcome | Explains the product; Start setup | No sample-data option |
| 2 Decision models | Pick Decision model + LLM (recommended) or LLM only. Lists Laya, Clef and Clef-flash, Jev. Sets the confidence threshold (default 0.70, editable) | The choice decides which variant of step 3 appears. It can be changed later in Settings |
| 3 AI providers, decision + LLM | Add any number of providers. Each has credentials, a model list, Fetch models, add or edit models by hand. Each provider has an "Also use for decision models" checkbox and each model a "Decision model" checkbox | A model can be a decision model only if its provider's box is ticked |
| 3b AI providers, LLM only | Same as 3 without the two decision-model checkboxes | Provider and model data are kept if the user switches mode |
| 4 Profile sources | LinkedIn export ZIP, resume upload, GitHub, Hugging Face, GitLab, manual | Imports start unverified; GitHub connects through GitHub sign-in and reads private repos too; no LinkedIn scraping. Skippable |
| 5 Resume mode | Default to Mode A or Mode B. No ATS style choice; every resume gets an ATS score | ATS style profiles are deferred until the research is done |
| 6 Ready | Summary of choices, each with a Change link, plus next actions | No statistics shown until real data exists |

**Fetch models popup.** Opens from a provider's Fetch models button. It shows the models returned by the provider with a search box, a Select all checkbox, and a checkbox per model, then Add selected and Cancel. It never adds models without the user's selection. If the provider's list call fails, it shows the error and offers manual entry.

**Provider test.** Test connection makes one small call, then shows success, or the provider's error in plain words.

## Key screen specs

Text wireframes for the screens in the first usable version. Each lists regions top to bottom or left to right.

**Pool (page 4)**

- Left: tab list (About and contact, Experience, Education, Projects, Skills, Certifications).
- Centre: item cards with title, dates, tags and a verified badge. Inline edit; drag to reorder.
- Right: source and evidence for the selected item, and an "Add item" button.
- Empty state: "Your pool is empty. Import from GitHub or upload a resume." with two buttons.

**Review queue (page 6)**

- A list of unverified imports and conflicts. Each row shows the item, where it came from, and Verify, Edit or Discard.
- Conflict rows show both values side by side, for example two different dates.

**New resume wizard (page 13)**

1. Choose a job (or add one).
2. Choose Mode A (edit an existing resume, pick which) or Mode B (generate from pool).
3. Choose a template.
4. Review the Role Lens selection, then Generate.

**Resume editor (page 14)**

- Left: structured sections with the items Role Lens kept. Dropped items sit in a collapsed "Left out" list, each with a reason and an Add back button.
- Centre: live PDF preview.
- Right: Role Lens panel with the job's key requirements and a match note per section; truthfulness warnings appear here and block export until resolved.

**Tailor diff review (page 15)**

- A list of changes, each showing before, after and the reason. Accept and Reject per change, plus Accept all safe changes. Added text that is not in the pool is marked and needs confirming.

**Providers (page 21)**

- Same card layout as onboarding step 3: credentials, model list, Fetch models, manual add, optional decision-model checkboxes. A tier tag (local, free, paid) and a test button on every card.

**Tracker (page 18)**

- Board columns: Saved, Applied, Interview, Offer, Rejected, Withdrawn, No response. Cards show company, role and date. A list view toggle and a filter by status. Dragging a card records an event.

## Components, states and microcopy

**Core components:** side rail with step or section list, card, tag, checkbox row, input with label, primary and secondary button, modal dialog, table, tabs, board, diff row, toast, empty state.

**Every data view needs these states:** loading, empty, error, partial (for example a snippet-only job description), and offline or rate-limited for provider-backed actions.

**Microcopy rules**

- Buttons say what happens: "Fetch models", "Add 3 selected", not "Submit".
- Errors say what went wrong and what to do next. Example: "Cloudflare returned a rate limit. MargHire will try NVIDIA next."
- Verified and unverified are always shown with text as well as colour.
- Free, local and paid are shown as text tags.
- Never show a model name alone; add a short plain-language note the first time it appears.

**Destructive actions** (delete item, erase all data, remove provider) use a confirmation dialog that names what will be lost.

## Accessibility and responsive rules

- Target WCAG 2.1 AA. Body text contrast at least 4.5:1; the accent `#0B6E6E` on white is about 6:1.
- Every control is reachable and usable by keyboard, with a visible focus ring.
- Touch targets are at least 44px.
- State is never colour-only: verified, tier and status always carry text.
- Modals trap focus and return it on close; Escape closes them.
- Form fields have visible labels, not placeholders alone.
- The step list marks the current step with `aria-current="step"`.
- Layout works from phone width (side rail collapses to a top step bar) up to desktop. The resume editor is desktop-first; on narrow screens it shows one pane at a time with tabs.
- Respect reduced-motion settings.
