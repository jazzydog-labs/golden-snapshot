# 0001 – Create Golden Snapshot FastAPI App

## Story
As a **Genesis Developer** I manually craft a complete, runnable FastAPI "Todo" application so future generators have an exact blueprint.

## Tasks
1. Create directory `golden_project_target/` at repo root.
2. Author these files:
   - `main.py` – FastAPI app, CORS, include routers
   - `database.py` – SQLAlchemy engine + session
   - `models/base.py`, `models/user.py`, `models/todo.py`
   - `routes/user_routes.py`, `routes/todo_routes.py`
   - `schemas/user_schemas.py`, `schemas/todo_schemas.py`
   - `requirements.txt` with **pinned** versions
   - `Dockerfile`, `docker-compose.yml`
3. Format: `black . && isort .`.
4. Run `docker-compose up --build -d` and verify via `scripts/smoke_test_target.sh`:
   - `GET /health` → **200 OK**
   - Successfully `POST` & `GET` a **User** and a **Todo**.
5. Add `just smoke` command to execute Docker build + smoke test.

## Acceptance Criteria
- Smoke test exits 0 locally and in CI.
- All endpoints behave as expected inside Docker.
- Commit hash recorded here upon closure.

## Schema

This is the schema that we will be using, the fastapi should match this:

```json
{
  "project_name": "BlogAPI",
  "entities": {
    "User": {
      "fields": {
        "email": {
          "type": "string",
          "unique": true,
          "required": true
        },
        "name": "string",
        "is_admin": {
          "type": "boolean",
          "default": false
        }
      }
    },
    "Post": {
      "fields": {
        "title": {
          "type": "string",
          "required": true
        },
        "content": {
          "type": "text"
        },
        "published": {
          "type": "boolean",
          "default": false
        },
        "views": {
          "type": "integer",
          "default": 0
        }
      },
      "belongs_to": "User"
    }
  }
}
```

## Commit Guidance
Focus exclusively on hand-written FastAPI code and infrastructure. When complete, move this file to `commits/closed/`. 