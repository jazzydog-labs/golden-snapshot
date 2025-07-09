### **Amended Epic: Bootstrap the Golden Snapshot**

**Goal:** To produce the very first, manually-verified, and fully-functional FastAPI project (the "golden snapshot"). This snapshot will become the **single source of truth** for every future generator test, enabling confident and rapid development.

---
### **Phase 1: Manually Author the Target Project**

This phase is about creating a concrete, runnable vision of what "correct" generated code looks like.

#### **Story 1: Create the Manual Target**
* **As a** Genesis Developer,
* **I want** to manually write a complete and working FastAPI application based on the `examples/todo.yaml` schema,
* **So that** we have a clear, verifiable target for the code generators to replicate.

#### **Implementation Guide for Story 1**
1.  **Create the Project Directory:** Create a temporary directory named `golden_project_target/` in the repository root.
2.  **Author the Files:** Based on the `examples/todo.yaml` schema, manually create the following files inside the target directory:
    * `main.py` (with FastAPI app setup, CORS, and router includes)
    * `database.py` (with SQLAlchemy engine/session setup)
    * `models/base.py` (for the declarative base)
    * `models/user.py` and `models/todo.py` (SQLAlchemy ORM classes)
    * `routes/user_routes.py` and `routes/todo_routes.py` (FastAPI routers with CRUD endpoints)
    * `schemas/user_schemas.py` and `schemas/todo_schemas.py` (Pydantic schemas for create, read, update)
    * `requirements.txt` (with all necessary, pinned dependencies)
    * `Dockerfile` and `docker-compose.yml`
3.  **Verify Functionality:**
    * Run `black .` and `isort .` on the `golden_project_target/` directory to ensure formatting is perfect.
    * From within the directory, run `docker-compose up --build -d`.
    * Run a verification script (e.g., `scripts/smoke_test_target.sh`) that uses `curl` to confirm the `/health` endpoint returns `200 OK` and that you can successfully `POST` and `GET` a User and a Todo.

---
### **Phase 2: Implement Generators to Match Target**

This phase is about writing the code that programmatically builds the project we just created by hand.

#### **Story 2: Implement Code Generators**
* **As a** Genesis Developer,
* **I want** to implement the core code generator classes (`ModelGenerator`, `RouteGenerator`, etc.),
* **So that** the `genesis generate` command can use our Jinja2 templates to perfectly replicate the manually-authored target project.

#### **Implementation Guide for Story 2**
1.  **Create Generator Classes:** In `genesis_core/generators/`, create the necessary classes. An `Orchestrator` will be responsible for running each generator in the correct order.
2.  **Develop via "Test-Driven Templating":** For each file in the manual target (e.g., `models/user.py`), write a corresponding unit test for its generator.
    * The test will render the appropriate template (e.g., `model.py.j2`) with the "User" entity's context.
    * It will then **assert** that the rendered string output is **identical** to the content of the target file (`golden_project_target/models/user.py`).
3.  **Final Verification:** Once all individual generators are complete, a final test will run the full `genesis generate` command and use a directory comparison helper to assert that the generated output is a byte-for-byte match of the `golden_project_target/`.

---
### **Phase 3: Lock-in the Official Snapshot**

This is the final step where we make the generator's output the official baseline for all future tests.

#### **Story 3: Finalize the Snapshot Test**
* **As a** Genesis Developer,
* **I want** to replace the manual target with the generator's own output and create an automated snapshot test,
* **So that** all future changes to templates or generators can be automatically verified against this trusted baseline.

#### **Implementation Guide for Story 3**
1.  **Promote the Snapshot:**
    * Run `genesis generate` one last time to create the final output.
    * **Delete** the `golden_project_target/` directory.
    * **Move** the generated output to its permanent home at `tests/snapshots/golden_project/`. Commit this to the repository.
2.  **Create the Automated Test:**
    * Create `tests/test_golden_snapshot.py`.
    * This test will call `genesis generate` into a temporary directory and perform a recursive directory comparison against `tests/snapshots/golden_project/`. The test fails if there is any difference.
3.  **Create the Updater Helper:**
    * Implement a script and a corresponding `just` command (`just update-snapshots`).
    * This command will delete the existing snapshot and replace it with fresh output from the generator, making intentional updates easy.
4.  **Integrate with CI:** Add a new job to the GitHub Actions workflow that runs the `test_golden_snapshot.py` test on every pull request.
