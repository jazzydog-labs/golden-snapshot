# CLAUDE.md — Genesis Golden Snapshot Contributor Guide

This document guides Claude Code (claude.ai/code) and human contributors working inside this repository.

---
## 🚀 Immediate Mission: Bootstrap the Golden Snapshot
Genesis must first produce a **manually-verified, fully-functional FastAPI “Todo” application**.  This application – the *Golden Snapshot* – becomes the canonical baseline against which every future template or generator change will be tested.

The work is split into three sequential phases (see `epics/001_golden_snapshot.md` for detailed acceptance criteria):
1. **Phase 1 — Manually Author the Target**  → temporary folder `golden_project_target/`
2. **Phase 2 — Implement Code Generators**   → `genesis_core/generators/*`
3. **Phase 3 — Finalise the Snapshot Test** → permanent folder `tests/snapshots/golden_project/`

Commit-sized task descriptions live in `./commits/open/000x_*.md`.  Complete them **in order** and move each file to `commits/closed/` once the corresponding git commit is created.

---
## Repository Conventions

• **Python 3.11**, Poetry for dependency management, pytest for tests, Black + Isort + Ruff for linting.
• Use Click or Typer for any CLI entry-points.
• The `justfile` is the single source of truth for common developer commands.
• Use `python -m pytest` (wrapped by `just test`) for running tests [[memory:2356247]].

---
## Working Philosophy

1. ***Template-first.***  All generated code **must** come from Jinja2 templates.
2. ***Generator-only runtime.***  Genesis writes code; it never executes the user’s app.
3. ***Fast feedback.***  Start minimal, iterate quickly, keep CI green.
4. ***Golden Snapshot is law.***  Any change that breaks `tests/test_golden_snapshot.py` is a regression unless explicitly intended.

---
## Key Commands (to be implemented incrementally)
- `genesis init`      – Scaffold a new generator project
- `genesis parse`     – Parse & validate YAML schema
- `genesis generate`  – Generate FastAPI project
- `genesis test`      – Run generator unit tests
- `genesis snapshot`  – Re-create Golden Snapshot (helper behind `just update-snapshots`)

---
## Development Checklist

- [ ] Phase 1 tasks complete and smoke-tested via Docker Compose
- [ ] Phase 2 generators render **byte-for-byte** identical output
- [ ] Phase 3 snapshot test passes

Once all three check-boxes are ticked, the Golden Snapshot era begins and regular feature work may resume.
