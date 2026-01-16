#!/usr/bin/env python3
"""
Cleanup script to remove duplicate CSS files from job folders.

Since we now use shared CSS files in src/templates/css/, we can remove
the CSS files that were previously duplicated in each job folder.
"""

from pathlib import Path
import sys


def cleanup_css_files(jobs_root: Path, dry_run: bool = True) -> dict:
    """
    Remove CSS files from all job folders.
    
    Args:
        jobs_root: Root directory containing phase folders
        dry_run: If True, only report what would be deleted
        
    Returns:
        Dictionary with cleanup statistics
    """
    stats = {
        "folders_checked": 0,
        "css_files_found": 0,
        "css_files_deleted": 0,
        "space_saved_bytes": 0
    }
    
    css_filenames = [
        "main.css",
        "contacts.css",
        "summary.css",
        "skills.css",
        "highlights.css",
        "experience.css",
        "education.css",
        "awards.css"
    ]
    
    if not jobs_root.exists():
        print(f"Jobs root directory not found: {jobs_root}")
        return stats
    
    # Iterate through all phase directories
    for phase_dir in jobs_root.iterdir():
        if not phase_dir.is_dir():
            continue
        
        # Iterate through all job folders in phase
        for job_folder in phase_dir.iterdir():
            if not job_folder.is_dir():
                continue
            
            stats["folders_checked"] += 1
            
            # Check for CSS files
            for css_filename in css_filenames:
                css_file = job_folder / css_filename
                if css_file.exists():
                    stats["css_files_found"] += 1
                    file_size = css_file.stat().st_size
                    stats["space_saved_bytes"] += file_size
                    
                    if dry_run:
                        print(f"Would delete: {css_file} ({file_size} bytes)")
                    else:
                        css_file.unlink()
                        stats["css_files_deleted"] += 1
                        print(f"Deleted: {css_file}")
    
    return stats


def format_bytes(bytes_count: int) -> str:
    """Format bytes as human-readable string."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_count < 1024.0:
            return f"{bytes_count:.2f} {unit}"
        bytes_count /= 1024.0
    return f"{bytes_count:.2f} TB"


def main():
    """Main cleanup function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Cleanup duplicate CSS files from job folders")
    parser.add_argument("--jobs-root", default="jobs", help="Path to jobs root directory")
    parser.add_argument("--execute", action="store_true", help="Actually delete files (default is dry-run)")
    args = parser.parse_args()
    
    jobs_root = Path(args.jobs_root)
    dry_run = not args.execute
    
    print("=" * 70)
    print("CSS Cleanup Script")
    print("=" * 70)
    print(f"Jobs root: {jobs_root}")
    print(f"Mode: {'DRY RUN (no files will be deleted)' if dry_run else 'EXECUTE (files will be deleted)'}")
    print()
    
    if dry_run:
        print("Running in DRY RUN mode. Use --execute to actually delete files.")
        print()
    
    stats = cleanup_css_files(jobs_root, dry_run=dry_run)
    
    print()
    print("=" * 70)
    print("Cleanup Summary")
    print("=" * 70)
    print(f"Folders checked: {stats['folders_checked']}")
    print(f"CSS files found: {stats['css_files_found']}")
    
    if dry_run:
        print(f"CSS files that would be deleted: {stats['css_files_found']}")
        print(f"Space that would be saved: {format_bytes(stats['space_saved_bytes'])}")
    else:
        print(f"CSS files deleted: {stats['css_files_deleted']}")
        print(f"Space saved: {format_bytes(stats['space_saved_bytes'])}")
    
    print()
    
    if dry_run and stats['css_files_found'] > 0:
        print("To actually delete these files, run:")
        print(f"  python cleanup_old_css.py --execute")
    
    return 0 if stats['css_files_found'] == 0 or not dry_run else 1


if __name__ == "__main__":
    sys.exit(main())
