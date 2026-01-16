#!/usr/bin/env python3
"""
Fix YAML-incompatible characters in existing job.yaml files
and convert to literal block scalar format for descriptions.
"""

from pathlib import Path
from src.lib.yaml_utils import load_yaml, dump_job_yaml
from src.events.get_gmail_linkedin import sanitize_text_for_yaml

def fix_job_yaml(job_yaml_path: Path) -> bool:
    """Fix a single job.yaml file."""
    try:
        # Load the job data
        job_data = load_yaml(job_yaml_path)
        
        # Sanitize all text fields
        text_fields = ['company', 'title', 'location', 'salary', 'description', 'source']
        changed = False
        
        for field in text_fields:
            if field in job_data and isinstance(job_data[field], str):
                original = job_data[field]
                sanitized = sanitize_text_for_yaml(original)
                if original != sanitized:
                    job_data[field] = sanitized
                    changed = True
        
        # Sanitize tags
        if 'tags' in job_data and isinstance(job_data['tags'], list):
            original_tags = job_data['tags']
            sanitized_tags = [sanitize_text_for_yaml(tag) if isinstance(tag, str) else tag for tag in original_tags]
            if original_tags != sanitized_tags:
                job_data['tags'] = sanitized_tags
                changed = True
        
        # Always rewrite to use new literal block scalar format
        # This will convert quoted descriptions to |- format
        dump_job_yaml(job_yaml_path, job_data)
        return True
        
    except Exception as e:
        print(f"Error fixing {job_yaml_path}: {e}")
        return False


def main():
    """Fix all job.yaml files in the jobs directory."""
    jobs_root = Path('jobs')
    
    if not jobs_root.exists():
        print("Jobs directory not found")
        return
    
    fixed_count = 0
    total_count = 0
    
    # Find all job.yaml files
    for job_yaml in jobs_root.glob('*/*/job.yaml'):
        total_count += 1
        if fix_job_yaml(job_yaml):
            fixed_count += 1
            print(f"Fixed: {job_yaml.parent.name}")
    
    print(f"\nProcessed {total_count} job.yaml files")
    print(f"Converted {fixed_count} files to literal block scalar format")


if __name__ == '__main__':
    main()
