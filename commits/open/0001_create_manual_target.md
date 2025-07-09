# 0001 – Create the Manual Target Project (Phase 1)

See epic: `epics/001_golden_snapshot.md` → *Phase 1: Manually Author the Target Project*

## Story
As a **Genesis Developer** I manually write a complete, runnable FastAPI application based on `examples/todo.yaml` so the generators have an exact blueprint to copy.

## Tasks
1. Create directory `golden_project_target/` at repo root.
2. Author the following files (structure mirrors final generated app):
   - `main.py` – FastAPI app, CORS, include routers
   - `database.py` – SQLAlchemy engine + session
   - `models/base.py`, `models/user.py`, `models/todo.py`
   - `routes/user_routes.py`, `routes/todo_routes.py`
   - `schemas/user_schemas.py`, `schemas/todo_schemas.py`
   - `requirements.txt` with **pinned** versions
   - `Dockerfile`, `docker-compose.yml`
3. Format the directory: `black . && isort .`.
4. Run `docker-compose up --build -d` and verify:
   - `GET /health` returns **200 OK**
   - Can `POST` + `GET` a **User** and **Todo** via API
5. Add `scripts/smoke_test_target.sh` performing the above checks (used by CI).

## Acceptance Criteria
- All endpoints behave as expected inside Docker.
- Smoke test exits **0**.
- CI job `phase1-smoke` passes.

## Commit Guidance
Commit only *hand-written* code for the target; generators come later.  When complete, move this file to `commits/closed/` and reference commit hash in its header. 