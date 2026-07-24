# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A [dlthub](https://dlthub.com) workspace (`dlthub-workspace`, from `pyproject.toml`) — for building dlt data pipelines, plus a small Streamlit app (`app.py`). The workspace is currently a fresh scaffold: `__deployment__.py` has no pipelines registered yet, and `.dlt/secrets.toml` / `.dlt/config.toml` are empty placeholders.

## Environment & commands

- Python 3.13 (`.python-version`), dependencies managed via `uv` (`uv.lock`, `pyproject.toml`).
- Install/sync deps: `uv sync`
- Add a dependency: `uv add <package>`
- Run the Streamlit app: `uv run streamlit run app.py`
- dlthub CLI (pipelines, toolkits, secrets): `uv run dlthub ...` — e.g. `uv run dlthub ai status`, `uv run dlthub ai toolkit install <name>`

## Workflow: use the dlthub skills, not ad-hoc pipeline code

This repo is driven by installed Claude skills under `.claude/skills/` (mirrored in `.agents/skills/`) rather than hand-rolled dlt boilerplate:

- **`dlthub-router`** — entry point. Routes a stated goal (pull from a REST API, ingest from SQL, load CSVs from S3, build reports, add data quality checks, deploy/schedule) to the right toolkit, installs it (`dlthub --non-interactive ai toolkit install <name>`), and hands off to that toolkit's entry skill. Use this whenever the needed toolkit isn't installed yet; skip it if the matching toolkit is already installed — go straight to its entry skill.
- **`setup-secrets`** — the only sanctioned way to read/write `.dlt/secrets.toml` (or profile-scoped `.dlt/<profile>.secrets.toml`). Never read or write secrets files directly. Prefer the `dlt-workspace-mcp` tools (`secrets_list`, `secrets_view_redacted`, `secrets_update_fragment`); fall back to `uv run dlthub ai secrets ...` if MCP isn't connected. When writing fragments, only ever write placeholder values (e.g. `sk-*****-your-key`) — real values are filled in by the user by hand. Secrets are always scoped under `[sources.<name>]` or `[destination.<name>.credentials]`.
- **`improve-skills`** — run at the end of a session (or on request) to fold real learnings (errors hit, schema surprises, auth/pagination quirks, doc links) back into the relevant toolkit's SKILL.md. Read the target skill first, keep edits minimal, get user approval before editing.

A `dlt-workspace-mcp` MCP server is expected to back these skills (health-checked via `dlthub ai status`); prefer its tools over CLI fallbacks when it's connected.

## Secrets & config layout

- `.dlt/config.toml` — non-secret runtime config (e.g. `[runtime] log_level`).
- `.dlt/secrets.toml` and `*.secrets.toml` — gitignored; never commit or print real values.
- `.dlt/data/` and `.dlt/state/` — gitignored local pipeline working dirs (per-profile subfolders, e.g. `dev`).

## Registering pipelines for deployment

`__deployment__.py` is the deployment manifest: import pipeline/notebook objects and list them in `__all__` to have them picked up for deployment. It starts empty — new pipelines built via the dlthub skills should be wired in here.
