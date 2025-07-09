#!/usr/bin/env python3
"""
Validates that a generated project matches the golden snapshot structure.

Usage:
    python validate_structure.py <generated_project_path> <manifest_or_filelist_path>

Supports both snapshot_manifest.json and file_list.json formats.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple


def load_manifest(manifest_path: str) -> Dict:
    """Load the snapshot manifest JSON."""
    with open(manifest_path, 'r') as f:
        return json.load(f)


def validate_file_structure(generated_path: Path, manifest: Dict) -> Tuple[bool, List[str]]:
    """Validate the file structure matches the manifest."""
    errors = []
    
    # Check all files exist
    for file_info in manifest['structure']['files']:
        file_path = generated_path / file_info['path']
        if not file_path.exists():
            errors.append(f"Missing file: {file_info['path']}")
        elif file_path.stat().st_size == 0 and not file_info['path'].endswith('__init__.py'):
            errors.append(f"Empty file: {file_info['path']}")
        elif file_info.get('executable') and not os.access(file_path, os.X_OK):
            errors.append(f"File not executable: {file_info['path']}")
    
    # Check directories and their files
    for dir_info in manifest['structure']['directories']:
        dir_path = generated_path / dir_info['path']
        if not dir_path.exists():
            errors.append(f"Missing directory: {dir_info['path']}")
            continue
        
        for file_info in dir_info['files']:
            file_path = dir_path / file_info['path']
            if not file_path.exists():
                errors.append(f"Missing file: {dir_info['path']}/{file_info['path']}")
            elif file_path.stat().st_size == 0 and not file_info['path'].endswith('__init__.py'):
                errors.append(f"Empty file: {dir_info['path']}/{file_info['path']}")
            elif file_info.get('executable') and not os.access(file_path, os.X_OK):
                errors.append(f"File not executable: {dir_info['path']}/{file_info['path']}")
    
    return len(errors) == 0, errors


def validate_file_list(generated_path: Path, file_list_path: str) -> Tuple[bool, List[str]]:
    """Validate against the simple file list."""
    with open(file_list_path, 'r') as f:
        file_list = json.load(f)
    
    errors = []
    
    # Check all files
    for file_path in file_list['files']:
        full_path = generated_path / file_path
        if not full_path.exists():
            errors.append(f"Missing file: {file_path}")
    
    # Check executables
    for file_path in file_list['executable_files']:
        full_path = generated_path / file_path
        if full_path.exists() and not os.access(full_path, os.X_OK):
            errors.append(f"File not executable: {file_path}")
    
    return len(errors) == 0, errors


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    
    generated_path = Path(sys.argv[1])
    manifest_path = sys.argv[2]
    
    if not generated_path.exists():
        print(f"Error: Generated project path does not exist: {generated_path}")
        sys.exit(1)
    
    if not Path(manifest_path).exists():
        print(f"Error: Manifest file does not exist: {manifest_path}")
        sys.exit(1)
    
    # Determine file type and validate accordingly
    with open(manifest_path, 'r') as f:
        data = json.load(f)
    
    if 'structure' in data:
        # Full manifest format
        print("Using snapshot manifest format...")
        valid, errors = validate_file_structure(generated_path, data)
    elif 'files' in data:
        # Simple file list format  
        print("Using file list format...")
        valid, errors = validate_file_list(generated_path, manifest_path)
    else:
        print("Error: Unknown manifest format")
        sys.exit(1)
    
    if valid:
        print("✅ File structure validation passed!")
    else:
        print("❌ File structure validation failed:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()