# 0001 – Create Golden Snapshot FastAPI App

## Story
As a **Genesis Developer** I would like to be able to eject into a `./ejected` directory, all the files that are in `./golden_project_target/snapshot_manifest.json`.

## Tasks
1. Create script `./scripts/eject_snapshot.py` that ejects all the files in snapshot_manifest.json from this directory
2. create a smoketest snapshot recipe inside the snapshot directory, along with a justfile, that when we move that directory anyway, it can run the smoketest and validate that the snapshot that's been ejected works
3. gitignore the snapshot dir
## Acceptance Criteria
- Smoke test exits 0 locally and in CI.
- we can copy the snapshot directory somewhere
- Nothign else changes in this directory
