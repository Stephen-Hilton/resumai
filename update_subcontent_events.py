#!/usr/bin/env python3
"""
Update all existing job.yaml files to use the template's subcontent_events configuration.
"""

from pathlib import Path
from src.lib.yaml_utils import load_yaml, dump_job_yaml

# Template subcontent_events (from src/templates/job.yaml)
TEMPLATE_SUBCONTENT_EVENTS = [
    {"contacts": "gen_static_subcontent_contacts"},
    {"summary": "gen_llm_subcontent_summary"},
    {"skills": "gen_llm_subcontent_skills"},
    {"highlights": "gen_llm_subcontent_highlights"},
    {"experience": "gen_llm_subcontent_experience"},
    {"education": "gen_static_subcontent_education"},
    {"awards": "gen_static_subcontent_awards"},
    {"coverletter": "gen_llm_subcontent_awards"}
]


def update_job_yaml(job_yaml_path: Path) -> bool:
    """Update a single job.yaml file with template subcontent_events."""
    try:
        # Load the job data
        job_data = load_yaml(job_yaml_path)
        
        # Get current subcontent_events
        current_events = job_data.get('subcontent_events', [])
        
        # Check if it matches the template
        if current_events == TEMPLATE_SUBCONTENT_EVENTS:
            return False  # No change needed
        
        # Update to template
        job_data['subcontent_events'] = TEMPLATE_SUBCONTENT_EVENTS
        
        # Save the updated data
        dump_job_yaml(job_yaml_path, job_data)
        return True
        
    except Exception as e:
        print(f"Error updating {job_yaml_path}: {e}")
        return False


def main():
    """Update all job.yaml files in the jobs directory."""
    jobs_root = Path('jobs')
    
    if not jobs_root.exists():
        print("Jobs directory not found")
        return
    
    updated_count = 0
    total_count = 0
    
    # Find all job.yaml files
    for job_yaml in jobs_root.glob('*/*/job.yaml'):
        total_count += 1
        if update_job_yaml(job_yaml):
            updated_count += 1
            print(f"Updated: {job_yaml.parent.name}")
    
    print(f"\nProcessed {total_count} job.yaml files")
    print(f"Updated {updated_count} files to use template subcontent_events")
    print(f"Skipped {total_count - updated_count} files (already using template)")


if __name__ == '__main__':
    main()
