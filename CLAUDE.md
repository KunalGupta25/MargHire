# CLAUDE.md

@AGENTS.md

The rules in `AGENTS.md` apply in full. This file adds Claude Code specifics: how to use the Ponytail and Graphify skills in this repo.

## Skills used in this repo

### Ponytail (keep code small)

Ponytail is an MIT-licensed skill (`DietrichGebert/ponytail`) that makes the agent reuse existing code, the standard library and native platform features before writing new code.

Already installed by the maintainer. If a skill or command below is missing, tell the maintainer; do not reinstall on your own. The hooks need `node` on the PATH to switch it on each session.

How to use it here:

- Default mode is `full`. Use `/ponytail lite` when exploring, and avoid `ultra` for requirement work, since it challenges the requirement itself.
- Run `/ponytail-review` on the current diff before opening a pull request. It checks for over-engineering only, not bugs or security, so it does not replace tests or review.
- Run `/ponytail-audit` at the end of each phase to find the biggest cuts.
- Run `/ponytail-debt` before a release to list deliberate shortcuts marked with `ponytail:` comments and their upgrade triggers.
- `stop ponytail` turns it off for the session.

Where Ponytail must not cut (these always win over "write less"):

- Input validation at trust boundaries: uploads, imports, job descriptions, MCP arguments.
- Error handling that prevents data loss, such as saving a version before a model call.
- The truthfulness check, secret handling, and the router's error policy.
- Accessibility basics in the UI.
- Tests for any requirement in the Test Plan.

### Graphify (map the codebase and docs)

Graphify turns a folder into a queryable knowledge graph, so you can find how parts connect without reading every file. It needs Python 3.10+ and Claude Code.

Already installed by the maintainer (the command is `graphify`). If it is missing, tell the maintainer; do not reinstall on your own.

Use:

- `/graphify .` builds the graph for the repo.
- `/graphify . --update` reprocesses only changed files.
- `/graphify query "..."`, `/graphify path "A" "B"` and `/graphify explain "X"` answer questions from the existing graph.
- `graphify hook install` rebuilds the graph on each git commit.

Output goes to `graphify-out/`, including `GRAPH_REPORT.md` (central nodes and surprising connections), `graph.json` and an interactive `graph.html`.

Rules for this repo:

- Before searching many files to understand how modules connect, check `graphify-out/GRAPH_REPORT.md` and query the graph first.
- Rebuild or update the graph after large refactors and at the end of each phase.
- Add `graphify-out/cache/` to `.gitignore`. Decide whether to commit the rest.
- Run Graphify on the repo and `docs/` only. Never point it at real resumes, exports or any folder with personal data or keys. Check what it sends to a model before running it on private material; this document does not confirm that, so verify it first.
- Treat the graph as a guide, not proof. Confirm in the source before changing code.

## Claude Code working notes

- Start a task by reading the planning document that matches it (see `AGENTS.md`), then the files you will change.
- Use plan mode for anything touching the schema, the router, Role Lens or the truthfulness check, and describe the plan before editing.
- Prefer small commits, one requirement each. Run the relevant tests before saying a task is done, and report what you ran.
- Use subagents for broad searches so the main context stays focused.
- When the user's request conflicts with `AGENTS.md` rule 1 to 10, say so and ask before proceeding.
- Never run commands that send personal data, resumes or keys to external services, except through the provider router with the user's enabled providers.
