#!/usr/bin/env python3
"""
One-time script to send all jobs from src/jobs/2_generated/ back to src/jobs/1_queued/
This script moves only the original YAML job files back to the queue.
"""

import os
import shutil
from pathlib import Path

def send_back_to_queue():
    """Move all job YAML files from 2_generated back to 1_queued"""
    
    # Define directories
    script_dir = Path(__file__).parent
    generated_dir = script_dir / 'src' / 'jobs' / '2_generated'
    queued_dir = script_dir / 'src' / 'jobs' / '1_queued'
    
    # Ensure queued directory exists
    queued_dir.mkdir(exist_ok=True)
    
    if not generated_dir.exists():
        print(f"Generated directory not found: {generated_dir}")
        return
    
    moved_count = 0
    
    # Iterate through all directories in 2_generated
    for job_dir in generated_dir.iterdir():
        if job_dir.is_dir():
            print(f"Processing directory: {job_dir.name}")
            
            # Look for YAML files in this directory
            yaml_files = list(job_dir.glob('*.yaml'))
            
            for yaml_file in yaml_files:
                try:
                    # Move the YAML file back to queued directory
                    destination = queued_dir / yaml_file.name
                    
                    # If destination exists, remove it first
                    if destination.exists():
                        print(f"  Removing existing file: {destination.name}")
                        destination.unlink()
                    
                    # Move the file
                    shutil.move(str(yaml_file), str(destination))
                    print(f"  Moved: {yaml_file.name} -> 1_queued/")
                    moved_count += 1
                    
                except Exception as e:
                    print(f"  Error moving {yaml_file.name}: {str(e)}")
                    continue
    
    print(f"\nCompleted! Moved {moved_count} job files back to queue.")
    print("Note: Generated HTML/PDF files remain in 2_generated directories.")

if __name__ == '__main__':
    print("Sending all jobs from 2_generated back to 1_queued...")
    send_back_to_queue()