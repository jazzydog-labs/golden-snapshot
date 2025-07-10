# CLAUDE.md — Golden Snapshot Contributor Guide

This repository is **only** for crafting the reference FastAPI application that future tools (e.g., Genesis) will one-day generate automatically.  Think of it as the hand-crafted masterpiece every generator must imitate.

---
## 🎯 Objective
Build a **fully-functional FastAPI “Todo” service** based on `examples/todo.yaml`, complete with Docker packaging and a smoke-test script.  When finished, the directory `golden_project_target/` will contain:

• FastAPI app (`main.py`)
• SQLAlchemy database layer (`database.py`, `models/*`)
• Pydantic schemas (`schemas/*`)
• CRUD routes (`routes/*`)
• Tooling files (`requirements.txt`, `Dockerfile`, `docker-compose.yml`)
• Verification script (`scripts/smoke_test_target.sh`)

Nothing about code generators, templates, or CI snapshot tests lives here — those belong in the Genesis repo.  This project’s *sole* deliverable is the working FastAPI reference implementation.

---
## Workflow
1. Complete the tasks in `commits/open/0001_create_golden_snapshot.md` (see below).
2. Run `just smoke` (to be added) which builds the Docker stack and executes the smoke test.
3. Once the server passes the smoke test, move the commit file to `commits/closed/` and push.

---
## Development Conventions
• **Python 3.11** (manage with Poetry).
• Black + Isort + Ruff; enforce via pre-commit.
• Prefer Click/Typer for any helper CLI scripts.
• Use `python -m pytest` for tests [[memory:2356247]].

---
## Open Commit(s)
Only one commit spec is open:

```
commits/open/0001_create_golden_snapshot.md
```

Get that done and we’re finished. 🎉


## Demo Guidelines

When creating demos, ALWAYS start with a "killer feature" that is:
- **Concise**: Show the most impressive capability in 2-3 lines of code
- **Attention-grabbing**: Demonstrate immediate value
- **To the point**: No setup, just the wow factor
- **Practical**: Show why users should care

Example format:
```python
def demo_killer_feature():
    """The ONE thing that makes this feature amazing."""
    print("=== KILLER FEATURE: Transform any idea into 10 refined versions in seconds ===")
    idea = Idea.create("Basic concept", score=5.0)
    best_version = idea.auto_refine(iterations=10).get_best_version()
    print(f"Original score: 5.0 → Best score: {best_version.score} (+{best_version.score - 5.0} improvement!)")
```

Then proceed with the detailed demo sections.