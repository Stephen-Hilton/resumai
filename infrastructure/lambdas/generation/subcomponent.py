"""
Subcomponent Generation Lambda Handler (SQS Triggered)

Processes generation requests from SQS queue.

Requirements: 7.5, 8.1, 8.2, 8.4, 8.5, 8.6, 9.3, 16.3
"""
import json
import os
import sys
import boto3
from typing import Dict, Optional

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from shared.dynamodb import DynamoDBClient
from shared.validation import VALID_SUBCOMPONENTS

# Bedrock client
bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-west-2')


def generate_ai_content(resume_section: Dict, job_desc: str, component: str) -> str:
    """
    Generate AI content using AWS Bedrock Nova Micro.
    
    Requirements: 8.1, 8.2, 8.4
    """
    # Build prompt based on component type
    prompts = {
        'contact': f"""Generate a professional contact section HTML for a resume.
Use the following contact information:
{json.dumps(resume_section, indent=2)}

Return clean HTML without inline styles. Use semantic tags like <address>, <a>, etc.""",

        'summary': f"""Generate a tailored professional summary for this job application.

Base Summary: {resume_section}

Job Description:
{job_desc}

Create a compelling 2-3 sentence summary that highlights relevant experience and skills for this specific role.
Return clean HTML in a <section class="summary"> tag.""",

        'skills': f"""Generate a tailored skills section for this job application.

Available Skills: {json.dumps(resume_section)}

Job Description:
{job_desc}

Select and organize the most relevant skills for this role. Group them logically.
Return clean HTML with <ul> and <li> tags in a <section class="skills"> tag.""",

        'highlights': f"""Generate tailored career highlights for this job application.

Available Highlights: {json.dumps(resume_section)}

Job Description:
{job_desc}

Select the most relevant highlights that demonstrate qualifications for this role.
Return clean HTML with <ul> and <li> tags in a <section class="highlights"> tag.""",

        'experience': f"""Generate a tailored experience section for this job application.

Experience:
{json.dumps(resume_section, indent=2)}

Job Description:
{job_desc}

Emphasize achievements and responsibilities most relevant to this role.
Return clean HTML with proper semantic structure in a <section class="experience"> tag.""",

        'education': f"""Generate an education section HTML for a resume.

Education:
{json.dumps(resume_section, indent=2)}

Return clean HTML with proper semantic structure in a <section class="education"> tag.""",

        'awards': f"""Generate an awards/certifications section HTML for a resume.

Awards:
{json.dumps(resume_section, indent=2)}

Return clean HTML with proper semantic structure in a <section class="awards"> tag.""",

        'keynotes': f"""Generate a keynotes/speaking engagements section HTML for a resume.

Keynotes:
{json.dumps(resume_section, indent=2)}

Return clean HTML with proper semantic structure in a <section class="keynotes"> tag.""",

        'coverletter': f"""Generate a tailored cover letter for this job application.

Candidate Summary: {resume_section.get('summary', '')}
Key Skills: {json.dumps(resume_section.get('skills', []))}
Key Highlights: {json.dumps(resume_section.get('highlights', []))}

Job Description:
{job_desc}

Write a compelling cover letter that connects the candidate's experience to the job requirements.
Return clean HTML with proper paragraph structure.""",
    }
    
    prompt = prompts.get(component, f"Generate HTML content for {component} section.")
    
    # Call Bedrock Nova Micro
    try:
        response = bedrock_runtime.invoke_model(
            modelId='amazon.nova-micro-v1:0',
            contentType='application/json',
            accept='application/json',
            body=json.dumps({
                'inputText': prompt,
                'textGenerationConfig': {
                    'maxTokenCount': 2048,
                    'temperature': 0.7,
                    'topP': 0.9,
                }
            })
        )
        
        result = json.loads(response['body'].read())
        return result.get('results', [{}])[0].get('outputText', '')
        
    except Exception as e:
        print(f"Bedrock error: {e}")
        raise


def generate_manual_content(resume_section: Dict, component: str) -> str:
    """
    Generate manual (static) HTML content from resume JSON.
    
    Requirements: 9.3
    """
    if component == 'contact':
        contact = resume_section
        html = '<section class="contact">'
        html += f'<h1>{contact.get("name", "")}</h1>'
        html += '<address>'
        if contact.get('email'):
            html += f'<a href="mailto:{contact["email"]}">{contact["email"]}</a>'
        if contact.get('phone'):
            html += f'<span class="phone">{contact["phone"]}</span>'
        if contact.get('location'):
            html += f'<span class="location">{contact["location"]}</span>'
        if contact.get('linkedin'):
            html += f'<a href="{contact["linkedin"]}" class="linkedin">LinkedIn</a>'
        if contact.get('website'):
            html += f'<a href="{contact["website"]}" class="website">Website</a>'
        html += '</address></section>'
        return html
    
    elif component == 'summary':
        return f'<section class="summary"><p>{resume_section}</p></section>'
    
    elif component == 'skills':
        html = '<section class="skills"><h2>Skills</h2><ul>'
        for skill in resume_section:
            html += f'<li>{skill}</li>'
        html += '</ul></section>'
        return html
    
    elif component == 'highlights':
        html = '<section class="highlights"><h2>Highlights</h2><ul>'
        for highlight in resume_section:
            html += f'<li>{highlight}</li>'
        html += '</ul></section>'
        return html
    
    elif component == 'experience':
        html = '<section class="experience"><h2>Experience</h2>'
        for exp in resume_section:
            html += '<article class="job">'
            html += f'<h3>{exp.get("title", "")}</h3>'
            html += f'<p class="company">{exp.get("company", "")}</p>'
            dates = exp.get('startDate', '')
            if exp.get('current'):
                dates += ' - Present'
            elif exp.get('endDate'):
                dates += f' - {exp["endDate"]}'
            html += f'<p class="dates">{dates}</p>'
            html += f'<p class="description">{exp.get("description", "")}</p>'
            if exp.get('achievements'):
                html += '<ul class="achievements">'
                for achievement in exp['achievements']:
                    html += f'<li>{achievement}</li>'
                html += '</ul>'
            html += '</article>'
        html += '</section>'
        return html
    
    elif component == 'education':
        html = '<section class="education"><h2>Education</h2>'
        for edu in resume_section:
            html += '<article class="degree">'
            html += f'<h3>{edu.get("degree", "")} in {edu.get("field", "")}</h3>'
            html += f'<p class="institution">{edu.get("institution", "")}</p>'
            html += f'<p class="graduation">{edu.get("graduationDate", "")}</p>'
            if edu.get('gpa'):
                html += f'<p class="gpa">GPA: {edu["gpa"]}</p>'
            html += '</article>'
        html += '</section>'
        return html
    
    elif component == 'awards':
        html = '<section class="awards"><h2>Awards & Certifications</h2>'
        for award in resume_section:
            html += '<article class="award">'
            html += f'<h3>{award.get("title", "")}</h3>'
            html += f'<p class="issuer">{award.get("issuer", "")}</p>'
            html += f'<p class="date">{award.get("date", "")}</p>'
            if award.get('description'):
                html += f'<p class="description">{award["description"]}</p>'
            html += '</article>'
        html += '</section>'
        return html
    
    elif component == 'keynotes':
        html = '<section class="keynotes"><h2>Speaking Engagements</h2>'
        for keynote in resume_section:
            html += '<article class="keynote">'
            html += f'<h3>{keynote.get("title", "")}</h3>'
            html += f'<p class="event">{keynote.get("event", "")}</p>'
            html += f'<p class="date">{keynote.get("date", "")}</p>'
            if keynote.get('location'):
                html += f'<p class="location">{keynote["location"]}</p>'
            html += '</article>'
        html += '</section>'
        return html
    
    elif component == 'coverletter':
        # For manual cover letter, just return a template
        return '''<article class="cover-letter">
<p>Dear Hiring Manager,</p>
<p>[Your cover letter content here]</p>
<p>Sincerely,<br>[Your Name]</p>
</article>'''
    
    return f'<section class="{component}"></section>'


def handler(event, context):
    """
    Process SQS generation messages.
    
    Message format:
    {
        "userid": "string",
        "jobid": "string",
        "resumeid": "string",
        "component": "string",
        "generationType": "manual" | "ai",
        "timestamp": "string"
    }
    """
    db = DynamoDBClient()
    
    for record in event.get('Records', []):
        try:
            message = json.loads(record['body'])
            
            userid = message['userid']
            jobid = message['jobid']
            resumeid = message['resumeid']
            component = message['component']
            generation_type = message['generationType']
            
            print(f"Processing {component} generation for job {jobid}")
            
            # Validate component
            if component not in VALID_SUBCOMPONENTS:
                print(f"Invalid component: {component}")
                continue
            
            # Get resume
            resume = db.get_resume(userid, resumeid)
            if not resume:
                print(f"Resume not found: {resumeid}")
                db.update_user_job(userid, jobid, {f'state{component}': 'error'})
                continue
            
            resume_json = resume.get('resumejson', {})
            
            # Get job description
            job = db.get_job(jobid)
            if not job:
                print(f"Job not found: {jobid}")
                db.update_user_job(userid, jobid, {f'state{component}': 'error'})
                continue
            
            job_desc = job.get('jobdesc', '')
            
            # Get the relevant resume section for this component
            section_map = {
                'contact': resume_json.get('contact', {}),
                'summary': resume_json.get('summary', ''),
                'skills': resume_json.get('skills', []),
                'highlights': resume_json.get('highlights', []),
                'experience': resume_json.get('experience', []),
                'education': resume_json.get('education', []),
                'awards': resume_json.get('awards', []),
                'keynotes': resume_json.get('keynotes', []),
                'coverletter': resume_json,  # Full resume for cover letter
            }
            
            resume_section = section_map.get(component, {})
            
            # Generate content
            try:
                if generation_type == 'ai':
                    content = generate_ai_content(resume_section, job_desc, component)
                else:
                    content = generate_manual_content(resume_section, component)
                
                # Update user-job with generated content
                db.update_user_job(userid, jobid, {
                    f'data{component}': content,
                    f'state{component}': 'complete'
                })
                
                print(f"Successfully generated {component} for job {jobid}")
                
            except Exception as gen_error:
                print(f"Generation error for {component}: {gen_error}")
                db.update_user_job(userid, jobid, {f'state{component}': 'error'})
                
        except Exception as e:
            print(f"Error processing message: {e}")
            # Message will be retried or sent to DLQ
            raise
    
    return {'statusCode': 200, 'body': 'Processing complete'}
