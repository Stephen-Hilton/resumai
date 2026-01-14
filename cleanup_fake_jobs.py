#!/usr/bin/env python3
"""
Cleanup Fake Job Data
====================

This script removes job YAML files that have less than 15 rows, 
indicating they contain fabricated/incomplete data rather than real job postings.
"""

import sys
import yaml
from pathlib import Path

def count_yaml_lines(yaml_file_path):
    """Count the number of lines in a YAML file"""
    try:
        with open(yaml_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # Count non-empty lines
            non_empty_lines = [line for line in lines if line.strip()]
            return len(non_empty_lines)
    except Exception as e:
        print(f"❌ Error reading {yaml_file_path}: {e}")
        return 0

def cleanup_fake_jobs():
    """Remove job YAML files with less than 15 rows"""
    
    queued_dir = Path('src/jobs/1_queued')
    
    if not queued_dir.exists():
        print(f"❌ Directory not found: {queued_dir}")
        return
    
    print("🧹 CLEANING UP FAKE JOB DATA")
    print("="*50)
    print(f"Scanning: {queued_dir}")
    print()
    
    deleted_count = 0
    kept_count = 0
    
    # Check all subfolders in queued directory
    for subfolder in queued_dir.iterdir():
        if not subfolder.is_dir():
            continue
            
        print(f"📁 Checking subfolder: {subfolder.name}")
        
        # Find YAML files in the subfolder
        yaml_files = list(subfolder.glob('*.yaml'))
        
        for yaml_file in yaml_files:
            line_count = count_yaml_lines(yaml_file)
            
            if line_count < 15:
                print(f"  ❌ DELETING: {yaml_file.name} (only {line_count} lines)")
                try:
                    yaml_file.unlink()
                    deleted_count += 1
                    
                    # If the subfolder is now empty, remove it too
                    remaining_files = list(subfolder.glob('*'))
                    if not remaining_files:
                        print(f"  🗑️  Removing empty subfolder: {subfolder.name}")
                        subfolder.rmdir()
                        
                except Exception as e:
                    print(f"  ❌ Error deleting {yaml_file}: {e}")
            else:
                print(f"  ✅ KEEPING: {yaml_file.name} ({line_count} lines)")
                kept_count += 1
    
    print()
    print("🎯 CLEANUP SUMMARY")
    print("="*30)
    print(f"Deleted files: {deleted_count}")
    print(f"Kept files: {kept_count}")
    
    if deleted_count > 0:
        print(f"\n✅ Successfully removed {deleted_count} fake job files")
    else:
        print("\n✅ No fake job files found to remove")

def main():
    """Main function"""
    
    print("⚠️  WARNING: This will permanently delete job YAML files with less than 15 lines")
    print("This is intended to remove fabricated/incomplete job data.")
    print()
    
    response = input("Continue? (y/N): ").strip().lower()
    
    if response == 'y':
        cleanup_fake_jobs()
    else:
        print("❌ Cleanup cancelled")

if __name__ == "__main__":
    main()