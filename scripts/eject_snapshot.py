#!/usr/bin/env python3
"""Eject snapshot files from golden_project_target to ./ejected directory."""

import json
import os
import shutil
from pathlib import Path
import stat

def load_manifest(manifest_path: Path) -> dict:
    """Load the snapshot manifest JSON file."""
    with open(manifest_path) as f:
        return json.load(f)

def create_directory_structure(source_root: Path, target_root: Path, structure: dict) -> None:
    """Recreate the directory structure and copy files based on manifest."""
    # Ensure target root exists
    target_root.mkdir(parents=True, exist_ok=True)
    
    # Process top-level files
    for file_info in structure.get("files", []):
        source_path = source_root / file_info["path"]
        target_path = target_root / file_info["path"]
        
        # Ensure parent directory exists
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy file
        if source_path.exists():
            shutil.copy2(source_path, target_path)
            
            # Set executable permission if needed
            if file_info.get("executable", False):
                st = os.stat(target_path)
                os.chmod(target_path, st.st_mode | stat.S_IEXEC)
            
            print(f"✓ Copied: {file_info['path']}")
        else:
            print(f"✗ Missing: {file_info['path']}")
    
    # Process directories
    for dir_info in structure.get("directories", []):
        dir_path = Path(dir_info["path"])
        target_dir = target_root / dir_path
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # Process files in directory
        for file_info in dir_info.get("files", []):
            source_path = source_root / dir_path / file_info["path"]
            target_path = target_dir / file_info["path"]
            
            if source_path.exists():
                shutil.copy2(source_path, target_path)
                
                # Set executable permission if needed
                if file_info.get("executable", False):
                    st = os.stat(target_path)
                    os.chmod(target_path, st.st_mode | stat.S_IEXEC)
                
                print(f"✓ Copied: {dir_path}/{file_info['path']}")
            else:
                print(f"✗ Missing: {dir_path}/{file_info['path']}")

def main():
    """Main entry point."""
    # Define paths
    project_root = Path(__file__).parent.parent
    manifest_path = project_root / "golden_project_target" / "snapshot_manifest.json"
    source_root = project_root / "golden_project_target"
    target_root = project_root / "ejected"
    
    # Check if manifest exists
    if not manifest_path.exists():
        print(f"Error: Manifest not found at {manifest_path}")
        return 1
    
    # Load manifest
    print(f"Loading manifest from: {manifest_path}")
    manifest = load_manifest(manifest_path)
    
    # Clean and recreate target directory
    if target_root.exists():
        print(f"Cleaning existing directory: {target_root}")
        shutil.rmtree(target_root)
    
    print(f"\nEjecting snapshot to: {target_root}")
    print("=" * 50)
    
    # Create directory structure and copy files
    create_directory_structure(source_root, target_root, manifest["structure"])
    
    # Copy the manifest itself for reference
    shutil.copy2(manifest_path, target_root / "snapshot_manifest.json")
    print(f"✓ Copied: snapshot_manifest.json")
    
    # Create justfile for the ejected snapshot
    justfile_content = """# Justfile for running smoke tests on the ejected snapshot

# Default recipe - show available commands
default:
    @just --list

# Run smoke tests against the FastAPI application
smoke:
    @echo "🔥 Running smoke tests..."
    @echo "Building Docker containers..."
    docker-compose build
    @echo "Starting services..."
    docker-compose up -d
    @echo "Waiting for services to be ready..."
    sleep 5
    @echo "Running smoke tests..."
    ./scripts/smoke_test_target.sh
    @echo "Shutting down services..."
    docker-compose down
    @echo "✅ Smoke tests complete!"

# Build the Docker image
build:
    docker-compose build

# Start services in detached mode
up:
    docker-compose up -d

# Stop all services
down:
    docker-compose down

# View logs
logs:
    docker-compose logs -f

# Clean up containers and volumes
clean:
    docker-compose down -v
    docker system prune -f

# Run tests without rebuilding
test:
    ./scripts/smoke_test_target.sh

# Check if services are healthy
health:
    @curl -s http://localhost:8000/health | jq . || echo "Service not responding"
"""
    
    justfile_path = target_root / "justfile"
    with open(justfile_path, 'w') as f:
        f.write(justfile_content)
    print(f"✓ Created: justfile")
    
    print("\n✅ Snapshot ejection complete!")
    print(f"📁 Files ejected to: {target_root}")
    
    return 0

if __name__ == "__main__":
    exit(main())