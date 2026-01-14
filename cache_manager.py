#!/usr/bin/env python3
"""
AI Content Cache Manager

Utility script for managing cached AI content across job directories.
"""

import sys
import argparse
from pathlib import Path
from typing import List, Dict

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from utils.ai_content_cache import AIContentCache, get_job_directory_from_id

def list_all_cached_jobs() -> List[Dict]:
    """List all jobs that have cached AI content"""
    jobs_dir = Path("src/jobs/2_generated")
    cached_jobs = []
    
    if not jobs_dir.exists():
        print("No jobs directory found")
        return cached_jobs
    
    for job_dir in jobs_dir.iterdir():
        if job_dir.is_dir():
            cache = AIContentCache(str(job_dir))
            cached_sections = cache.get_cached_sections()
            
            if cached_sections:
                cache_info = cache.get_cache_info()
                cached_jobs.append({
                    'job_name': job_dir.name,
                    'job_path': str(job_dir),
                    'cached_sections': cached_sections,
                    'total_sections': len(cached_sections),
                    'cache_info': cache_info
                })
    
    return cached_jobs

def show_cache_status():
    """Show cache status for all jobs"""
    print("AI Content Cache Status")
    print("=" * 50)
    
    cached_jobs = list_all_cached_jobs()
    
    if not cached_jobs:
        print("No cached AI content found")
        return
    
    print(f"Found {len(cached_jobs)} jobs with cached content:\n")
    
    for job in cached_jobs:
        print(f"Job: {job['job_name']}")
        print(f"  Cached sections: {', '.join(job['cached_sections'])}")
        print(f"  Total sections: {job['total_sections']}")
        
        # Show section details
        cache_info = job['cache_info']
        for section, details in cache_info.get('sections_detail', {}).items():
            generated_at = details.get('generated_at', 'Unknown')
            file_size = details.get('file_size', 0)
            print(f"    {section}: {generated_at[:19]} ({file_size} bytes)")
        print()

def show_job_cache(job_identifier: str):
    """Show detailed cache info for a specific job"""
    # Try to find job directory
    job_dir = get_job_directory_from_id(job_identifier)
    
    if not job_dir:
        # Try direct path
        job_path = Path(f"src/jobs/2_generated/{job_identifier}")
        if job_path.exists():
            job_dir = str(job_path)
    
    if not job_dir:
        print(f"Job not found: {job_identifier}")
        return
    
    print(f"Cache Details for: {Path(job_dir).name}")
    print("=" * 50)
    
    cache = AIContentCache(job_dir)
    cache_info = cache.get_cache_info()
    
    print(f"Cache directory: {cache_info['cache_directory']}")
    print(f"Total sections: {cache_info['total_sections']}")
    print(f"Cached sections: {', '.join(cache_info['cached_sections'])}")
    print()
    
    # Show detailed section info
    for section, details in cache_info.get('sections_detail', {}).items():
        print(f"Section: {section}")
        print(f"  Generated: {details.get('generated_at', 'Unknown')}")
        print(f"  File size: {details.get('file_size', 0)} bytes")
        
        metadata = details.get('metadata', {})
        if metadata:
            print(f"  Generator: {metadata.get('generator_class', 'Unknown')}")
            print(f"  Uses LLM: {metadata.get('uses_llm', 'Unknown')}")
            print(f"  Job title: {metadata.get('job_title', 'Unknown')}")
            print(f"  Company: {metadata.get('company', 'Unknown')}")
        print()

def clear_job_cache(job_identifier: str, section: str = None):
    """Clear cache for a specific job"""
    # Try to find job directory
    job_dir = get_job_directory_from_id(job_identifier)
    
    if not job_dir:
        # Try direct path
        job_path = Path(f"src/jobs/2_generated/{job_identifier}")
        if job_path.exists():
            job_dir = str(job_path)
    
    if not job_dir:
        print(f"Job not found: {job_identifier}")
        return
    
    cache = AIContentCache(job_dir)
    
    if section:
        success = cache.clear_cache(section)
        if success:
            print(f"Cleared cache for section '{section}' in job: {Path(job_dir).name}")
        else:
            print(f"Failed to clear cache for section '{section}'")
    else:
        success = cache.clear_cache()
        if success:
            print(f"Cleared all cache for job: {Path(job_dir).name}")
        else:
            print("Failed to clear cache")

def show_section_content(job_identifier: str, section: str):
    """Show content of a specific cached section"""
    # Try to find job directory
    job_dir = get_job_directory_from_id(job_identifier)
    
    if not job_dir:
        # Try direct path
        job_path = Path(f"src/jobs/2_generated/{job_identifier}")
        if job_path.exists():
            job_dir = str(job_path)
    
    if not job_dir:
        print(f"Job not found: {job_identifier}")
        return
    
    cache = AIContentCache(job_dir)
    content = cache.load_section_content(section)
    
    if content:
        print(f"Content for section '{section}' in job: {Path(job_dir).name}")
        print("=" * 50)
        
        import yaml
        print(yaml.dump(content, default_flow_style=False, indent=2))
    else:
        print(f"No cached content found for section '{section}'")

def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description="AI Content Cache Manager")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Status command
    subparsers.add_parser('status', help='Show cache status for all jobs')
    
    # Show command
    show_parser = subparsers.add_parser('show', help='Show cache details for a specific job')
    show_parser.add_argument('job', help='Job identifier or folder name')
    
    # Content command
    content_parser = subparsers.add_parser('content', help='Show content of a specific section')
    content_parser.add_argument('job', help='Job identifier or folder name')
    content_parser.add_argument('section', help='Section name (summary, skills, experience, etc.)')
    
    # Clear command
    clear_parser = subparsers.add_parser('clear', help='Clear cache for a job')
    clear_parser.add_argument('job', help='Job identifier or folder name')
    clear_parser.add_argument('--section', help='Specific section to clear (optional)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'status':
            show_cache_status()
        elif args.command == 'show':
            show_job_cache(args.job)
        elif args.command == 'content':
            show_section_content(args.job, args.section)
        elif args.command == 'clear':
            clear_job_cache(args.job, args.section)
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())