# 0003 – Finalise Golden Snapshot Test (Phase 3)

See epic: `epics/001_golden_snapshot.md` → *Phase 3: Lock-in the Official Snapshot*

## Story
As a **Genesis Developer** I promote the generator output to the official snapshot and add automated tests so future changes are guarded.

## Tasks
1. Run `genesis generate` one final time → `./tmp/final_gen`.
2. Delete `golden_project_target/`.
3. Move generated output to `tests/snapshots/golden_project/`.
4. Create `tests/test_golden_snapshot.py`:
   - Generate to temp dir
   - Recursively compare against snapshot
   - Fail if any difference
5. Add helper script + `just update-snapshots` to refresh snapshot intentionally.
6. Update CI workflow to run snapshot test on every PR.

## Acceptance Criteria
- Snapshot test passes locally and in CI.
- `just update-snapshots` replaces snapshot and fails if not committed.
- Repo no longer contains `golden_project_target/`.

## Commit Guidance
After this commit, Golden Snapshot becomes the contract for all generator changes.  Move this file to `commits/closed/` and celebrate 🎉 