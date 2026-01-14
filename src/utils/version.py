#!/usr/bin/env python3
"""
Version management for ResumeAI

AUTO-INCREMENT LOGIC FOR KIRO:
When making any change to the codebase, auto-increment the version using increment_version():
- Version format: major.minor.date.patch (e.g., 1.5.20260109.1)
- If date is NOT today, update date and reset patch to 1
- If date IS today, increment patch by one
- Always update version in pyproject.toml
"""

import os
import toml
from pathlib import Path
from datetime import datetime

def get_version():
    """Get version from pyproject.toml"""
    try:
        # Look for pyproject.toml in the project root (two levels up from src/utils/)
        project_root = Path(__file__).parent.parent.parent
        pyproject_path = project_root / "pyproject.toml"
        
        if pyproject_path.exists():
            with open(pyproject_path, 'r') as f:
                data = toml.load(f)
                current_date = datetime.now().strftime('%Y%m%d')
                return data.get('project', {}).get('version', f'1.0.{current_date}.1')
        else:
            current_date = datetime.now().strftime('%Y%m%d')
            return f'1.0.{current_date}.1'
    except Exception:
        current_date = datetime.now().strftime('%Y%m%d')
        return f'1.0.{current_date}.1'

def increment_version():
    """
    Auto-increment version following the logic:
    - Version format: major.minor.date.patch
    - If date is NOT today, update date and reset patch to 1
    - If date IS today, increment patch by one
    - Update version in pyproject.toml
    
    Returns the new version string
    """
    try:
        # Look for pyproject.toml in the project root (two levels up from src/utils/)
        project_root = Path(__file__).parent.parent.parent
        pyproject_path = project_root / "pyproject.toml"
        
        current_date = datetime.now().strftime('%Y%m%d')
        
        if not pyproject_path.exists():
            # Create default version with today's date
            new_version = f"1.0.{current_date}.1"
            # Create minimal pyproject.toml
            data = {
                'project': {
                    'name': 'resumai',
                    'version': new_version,
                    'description': 'AI-powered resume and cover letter generation system'
                }
            }
            with open(pyproject_path, 'w') as f:
                toml.dump(data, f)
            return new_version
        
        # Read current version
        with open(pyproject_path, 'r') as f:
            data = toml.load(f)
        
        current_version = data.get('project', {}).get('version', f'1.0.{current_date}.1')
        
        # Parse current version
        parts = current_version.split('.')
        if len(parts) != 4:
            # Invalid format, reset to default but preserve major.minor if possible
            if len(parts) >= 2:
                new_version = f"{parts[0]}.{parts[1]}.{current_date}.1"
            else:
                new_version = f"1.0.{current_date}.1"
        else:
            major, minor, date_str, patch = parts
            
            if date_str != current_date:
                # Date is not today, update date and reset patch to 1
                new_version = f"{major}.{minor}.{current_date}.1"
            else:
                # Date is today, increment patch
                new_patch = int(patch) + 1
                new_version = f"{major}.{minor}.{date_str}.{new_patch}"
        
        # Update pyproject.toml
        data['project']['version'] = new_version
        with open(pyproject_path, 'w') as f:
            toml.dump(data, f)
        
        return new_version
        
    except Exception as e:
        print(f"Error incrementing version: {e}")
        current_date = datetime.now().strftime('%Y%m%d')
        return f"1.0.{current_date}.1"

# Cache the version
VERSION = get_version()

if __name__ == "__main__":
    # When run directly, increment version and output to stdout
    new_version = increment_version()
    print(new_version)
