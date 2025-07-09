#!/bin/bash
set -e

echo "🔍 Golden Snapshot Validation Demo"
echo "=================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the project root
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
GOLDEN_DIR="$PROJECT_ROOT/golden_project_target"

echo "📁 Project root: $PROJECT_ROOT"
echo "📁 Golden snapshot: $GOLDEN_DIR"
echo ""

# Demo 1: Validate the golden snapshot against itself (should pass)
echo -e "${YELLOW}Demo 1: Validating golden snapshot against its own manifest${NC}"
echo "Command: python scripts/validate_structure.py golden_project_target golden_project_target/snapshot_manifest.json"
echo ""

cd "$PROJECT_ROOT"
if python scripts/validate_structure.py golden_project_target golden_project_target/snapshot_manifest.json; then
    echo -e "${GREEN}✓ Validation passed as expected!${NC}"
else
    echo -e "${RED}✗ Validation failed unexpectedly!${NC}"
fi

echo ""
echo "----------------------------------------"
echo ""

# Demo 2: Create a broken copy and validate it (should fail)
echo -e "${YELLOW}Demo 2: Creating a broken copy with missing files${NC}"
echo ""

# Create a temporary directory with missing files
TEMP_DIR=$(mktemp -d)
echo "📁 Creating broken copy at: $TEMP_DIR/broken_project"

# Copy the golden snapshot but intentionally leave out some files
cp -r "$GOLDEN_DIR" "$TEMP_DIR/broken_project"
rm -f "$TEMP_DIR/broken_project/main.py"  # Remove main.py
rm -rf "$TEMP_DIR/broken_project/routes"  # Remove entire routes directory
chmod -x "$TEMP_DIR/broken_project/entrypoint.sh"  # Remove executable permission

echo "Removed: main.py"
echo "Removed: routes/ directory"
echo "Changed: entrypoint.sh (removed executable permission)"
echo ""

echo "Command: python scripts/validate_structure.py $TEMP_DIR/broken_project golden_project_target/snapshot_manifest.json"
echo ""

if python scripts/validate_structure.py "$TEMP_DIR/broken_project" golden_project_target/snapshot_manifest.json; then
    echo -e "${RED}✗ Validation passed but should have failed!${NC}"
else
    echo -e "${GREEN}✓ Validation failed as expected!${NC}"
fi

# Cleanup
rm -rf "$TEMP_DIR"

echo ""
echo "----------------------------------------"
echo ""

# Demo 3: Show how to use with a generator
echo -e "${YELLOW}Demo 3: Example usage with a hypothetical generator${NC}"
echo ""
echo "If you had a generator that creates projects from schemas:"
echo ""
echo -e "${GREEN}# 1. Generate a project from schema${NC}"
echo "$ genesis generate examples/blog_schema.json --output generated_project/"
echo ""
echo -e "${GREEN}# 2. Validate the generated project matches golden snapshot${NC}"
echo "$ python scripts/validate_structure.py generated_project/ golden_project_target/snapshot_manifest.json"
echo ""
echo -e "${GREEN}# 3. Run smoke tests on generated project${NC}"
echo "$ cd generated_project && ../golden_project_target/scripts/smoke_test_target.sh"
echo ""

echo "----------------------------------------"
echo ""
echo "📚 Additional validation options:"
echo ""
echo "1. Validate against file list:"
echo "   $ python scripts/validate_structure.py <project_path> golden_project_target/file_list.json"
echo ""
echo "2. Compare file contents (not just structure):"
echo "   $ diff -r golden_project_target generated_project"
echo ""
echo "3. Run smoke tests to validate behavior:"
echo "   $ cd generated_project && docker-compose up --build -d"
echo "   $ ./scripts/smoke_test_target.sh"
echo ""
echo "✨ Demo complete!"