# 0002 – Implement Code Generators (Phase 2)

See epic: `epics/001_golden_snapshot.md` → *Phase 2: Implement Generators to Match Target*

## Story
As a **Genesis Developer** I implement generator classes so that `genesis generate` recreates the manual target **byte-for-byte** from `examples/todo.yaml`.

## Tasks
1. Create package `genesis_core/generators/`:
   - `base.py` – abstract `Generator` class
   - `model.py`, `route.py`, `schema.py`, `app.py`, `docker.py` subclasses
   - `orchestrator.py` to run generators in correct order.
2. Add Jinja2 templates under `templates/` mirroring manual target files.
3. Write unit tests (`tests/generators/`) following *Test-Driven Templating* pattern:
   - Render template with User/Todo context
   - Assert rendered string equals file in `golden_project_target/`
4. Implement CLI command `genesis generate` (Typer/Click).
5. Ensure `just generate` wrapper exists.

## Acceptance Criteria
- `pytest -k generators` passes.
- Running `genesis generate --schema examples/todo.yaml --out ./tmp/gen` produces output identical to `golden_project_target/` (use dir diff helper).

## Commit Guidance
Keep commits focused: templates + generator logic + tests.  Do **not** delete `golden_project_target/` yet.  Move this file to `commits/closed/` once completed. 