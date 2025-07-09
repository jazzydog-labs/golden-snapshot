# Golden Snapshot Validation Scripts

This directory contains scripts for validating generated projects against the golden snapshot reference implementation.

## Scripts

### `validate_structure.py`
Validates that a generated project matches the expected file structure.

**Usage:**
```bash
python scripts/validate_structure.py <generated_project_path> <manifest_path>
```

**Examples:**
```bash
# Validate using full manifest
python scripts/validate_structure.py generated_project/ golden_project_target/snapshot_manifest.json

# Validate using simple file list
python scripts/validate_structure.py generated_project/ golden_project_target/file_list.json
```

**Features:**
- Checks file and directory presence
- Validates executable permissions
- Allows empty `__init__.py` files
- Supports both manifest formats

### `demo_validation.sh`
Interactive demonstration of the validation system.

**Usage:**
```bash
bash scripts/demo_validation.sh
```

**What it does:**
1. Validates the golden snapshot against itself (should pass)
2. Creates a broken copy with missing files and tests validation (should fail)
3. Shows example usage patterns

## Integration Example

For a typical code generator workflow:

```bash
# 1. Generate project from schema
genesis generate examples/blog_schema.json --output generated_project/

# 2. Validate structure matches golden snapshot
python scripts/validate_structure.py generated_project/ golden_project_target/snapshot_manifest.json

# 3. Copy smoke test script to generated project
cp golden_project_target/scripts/smoke_test_target.sh generated_project/scripts/

# 4. Run behavioral validation
cd generated_project
docker-compose up --build -d
./scripts/smoke_test_target.sh
docker-compose down
```

## Validation Levels

1. **Structure Validation** - Files and directories exist
2. **Permission Validation** - Executable bits are set correctly  
3. **Content Validation** - Files are not empty (except `__init__.py`)
4. **Behavioral Validation** - Smoke tests pass
5. **Byte-level Validation** - `diff -r` for exact matches

Use the appropriate level based on your generator's requirements.