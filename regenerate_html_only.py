#!/usr/bin/env python3
"""
Regenerate HTML resume AND cover letter from existing content without AI calls
"""

import sys
import yaml
from pathlib import Path

# Add src to path
sys.path.append('src')

from utils.template_engine import TemplateEngine
from utils.content_aggregator import ContentAggregator

def regenerate_html_from_existing(job_folder_path):
    """
    Regenerate BOTH HTML resume and cover letter from existing YAML content without AI calls
    
    Args:
        job_folder_path: Path to job folder (e.g., "src/jobs/2_generated/JobName.../")
    """
    job_path = Path(job_folder_path)
    
    if not job_path.exists():
        print(f"❌ Job folder not found: {job_path}")
        return False
    
    # Find the YAML file with job data
    yaml_files = list(job_path.glob("*.yaml"))
    if not yaml_files:
        print(f"❌ No YAML file found in {job_path}")
        return False
    
    yaml_file = yaml_files[0]  # Use first YAML file found
    print(f"📄 Using content from: {yaml_file.name}")
    
    # Load existing content
    try:
        with open(yaml_file, 'r') as f:
            job_data = yaml.safe_load(f)
    except Exception as e:
        print(f"❌ Error loading YAML: {e}")
        return False
    
    # Initialize template engine
    template_engine = TemplateEngine()
    
    # Extract content sections for both resume and cover letter
    content_data = {
        'name': job_data.get('resume', {}).get('name', 'Name Not Found'),
        'email': job_data.get('resume', {}).get('email', ''),
        'phone': job_data.get('resume', {}).get('phone', ''),
        'location': job_data.get('resume', {}).get('location', ''),
        'summary': job_data.get('resume', {}).get('summary', ''),
        'skills': job_data.get('resume', {}).get('skills', {}),
        'experience': job_data.get('resume', {}).get('experience', []),
        'education': job_data.get('resume', {}).get('education', []),
        'awards': job_data.get('resume', {}).get('awards', []),
        'cover_letter': job_data.get('cover_letter', {})
    }
    
    success_count = 0
    
    # Generate resume HTML
    print("\n🔄 Regenerating Resume HTML...")
    try:
        resume_html = template_engine.render_resume(content_data)
        resume_file = job_path / f"{yaml_file.stem}.resume.html"
        
        with open(resume_file, 'w') as f:
            f.write(resume_html)
        print(f"✅ Resume HTML regenerated: {resume_file.name}")
        success_count += 1
    except Exception as e:
        print(f"❌ Error generating resume HTML: {e}")
    
    # Generate cover letter HTML
    print("\n🔄 Regenerating Cover Letter HTML...")
    try:
        cover_letter_html = template_engine.render_cover_letter(content_data, job_data)
        cover_letter_file = job_path / f"{yaml_file.stem}.coverletter.html"
        
        with open(cover_letter_file, 'w') as f:
            f.write(cover_letter_html)
        print(f"✅ Cover Letter HTML regenerated: {cover_letter_file.name}")
        success_count += 1
    except Exception as e:
        print(f"❌ Error generating cover letter HTML: {e}")
    
    return success_count == 2

def main():
    if len(sys.argv) != 2:
        print("🔄 HTML Regeneration Tool (Resume + Cover Letter)")
        print("=" * 50)
        print("Usage: python regenerate_html_only.py <job_folder_path>")
        print("Example: python regenerate_html_only.py 'src/jobs/2_generated/Ladders.Senior_Vice_President.../")
        print("\nThis tool regenerates BOTH resume and cover letter HTML files")
        print("from existing YAML content without making any AI calls.")
        return
    
    job_folder = sys.argv[1]
    print("🔄 HTML Regeneration Tool (Resume + Cover Letter)")
    print("=" * 50)
    print(f"📁 Target folder: {job_folder}")
    
    success = regenerate_html_from_existing(job_folder)
    
    if success:
        print("\n🎉 Both HTML files regenerated successfully!")
        print("📋 Generated files:")
        print("   • Resume HTML (with updated formatting)")
        print("   • Cover Letter HTML (with corrected spacing)")
        print("\n💡 Next steps:")
        print("   • View HTML files in browser to verify formatting")
        print("   • Use 'Regenerate PDFs' in web interface if needed")
    else:
        print("\n💥 HTML regeneration failed!")
        print("💡 Check that the YAML file exists and contains valid content")

if __name__ == "__main__":
    main()