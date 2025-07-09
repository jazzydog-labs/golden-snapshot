# Golden Snapshot Commands

# Run smoke test for the golden project target
smoke:
    @echo "🐳 Building and starting Docker containers..."
    cd golden_project_target && docker-compose up --build -d
    @echo "⏳ Waiting for API to be ready..."
    @sleep 5
    @echo "🧪 Running smoke tests..."
    cd golden_project_target && ./scripts/smoke_test_target.sh
    @echo "🛑 Stopping Docker containers..."
    cd golden_project_target && docker-compose down

# Run validation demo
demo:
    @echo "🔍 Running validation demo..."
    bash scripts/demo_validation.sh