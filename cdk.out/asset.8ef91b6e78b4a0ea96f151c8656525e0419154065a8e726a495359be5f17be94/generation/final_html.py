"""
Final HTML Generation Lambda Handler

Generates final resume and cover letter HTML files.

Requirements: 10.2, 10.4, 11.6
"""
import json
import os
import sys
import boto3
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from shared.response import api_response, bad_request, not_found, internal_error
from shared.dynamodb import DynamoDBClient
from shared.validation import VALID_SUBCOMPONENTS

# S3 client
s3 = boto3.client('s3')
RESUMES_BUCKET = os.environ.get('RESUMES_BUCKET', 'skillsnap-public-resumes')


def generate_resume_html(user_job: dict, job: dict, username: str) -> str:
    """Generate complete resume HTML from subcomponents."""
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resume - {job.get('jobtitle', 'Position')} at {job.get('jobcompany', 'Company')}</title>
    <link rel="stylesheet" href="/assets/resume-base.css">
</head>
<body>
    <main class="resume">
        {user_job.get('datacontact', '')}
        {user_job.get('datasummary', '')}
        {user_job.get('dataskills', '')}
        {user_job.get('datahighlights', '')}
        {user_job.get('dataexperience', '')}
        {user_job.get('dataeducation', '')}
        {user_job.get('dataawards', '')}
    </main>
</body>
</html>'''
    return html


def generate_cover_letter_html(user_job: dict, job: dict, username: str) -> str:
    """Generate cover letter HTML."""
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cover Letter - {job.get('jobtitle', 'Position')} at {job.get('jobcompany', 'Company')}</title>
    <link rel="stylesheet" href="/assets/cover-base.css">
</head>
<body>
    <main class="cover-letter">
        {user_job.get('datacoverletter', '')}
    </main>
</body>
</html>'''
    return html


def handler(event, context):
    """
    Generate final HTML files.
    
    Path parameters:
    - jobid: ID of the job
    
    Query parameters:
    - type: "resume" or "cover" (which HTML to generate)
    """
    try:
        # Get user ID from Cognito authorizer
        claims = event.get('requestContext', {}).get('authorizer', {}).get('claims', {})
        userid = claims.get('custom:userid') or claims.get('sub')
        username = claims.get('preferred_username') or claims.get('cognito:username', 'user')
        
        if not userid:
            return bad_request("User ID not found in token")
        
        # Get path parameters
        path_params = event.get('pathParameters', {}) or {}
        jobid = path_params.get('jobid')
        
        if not jobid:
            return bad_request("jobid is required")
        
        # Get query parameters
        query_params = event.get('queryStringParameters', {}) or {}
        file_type = query_params.get('type', 'resume')
        
        if file_type not in ['resume', 'cover']:
            return bad_request("type must be 'resume' or 'cover'")
        
        db = DynamoDBClient()
        
        # Get user-job
        user_job = db.get_user_job(userid, jobid)
        if not user_job:
            return not_found(f"Job '{jobid}' not found")
        
        # Check all subcomponents are complete
        for component in VALID_SUBCOMPONENTS:
            state = user_job.get(f'state{component}', 'locked')
            if state != 'complete':
                return bad_request(f"Cannot generate final files: {component} is not complete (state: {state})")
        
        # Get job details
        job = db.get_job(jobid)
        if not job:
            return not_found(f"Job '{jobid}' not found")
        
        # Generate HTML
        if file_type == 'resume':
            html_content = generate_resume_html(user_job, job, username)
            filename = 'resume.html'
            s3_field = 's3locresumehtml'
        else:
            html_content = generate_cover_letter_html(user_job, job, username)
            filename = 'coverletter.html'
            s3_field = 's3loccoverletterhtml'
        
        # Build S3 path
        company_safe = job.get('jobcompany', 'company').lower().replace(' ', '-')
        jobtitle_safe = job.get('jobtitlesafe', 'position')
        s3_key = f"{username}/{company_safe}/{jobtitle_safe}/{filename}"
        
        # Upload to S3
        s3.put_object(
            Bucket=RESUMES_BUCKET,
            Key=s3_key,
            Body=html_content.encode('utf-8'),
            ContentType='text/html',
            CacheControl='max-age=3600'
        )
        
        s3_uri = f"s3://{RESUMES_BUCKET}/{s3_key}"
        
        # Update user-job with S3 location
        db.update_user_job(userid, jobid, {s3_field: s3_uri})
        
        # Also upload index.html for the directory
        if file_type == 'resume':
            index_key = f"{username}/{company_safe}/{jobtitle_safe}/index.html"
            s3.put_object(
                Bucket=RESUMES_BUCKET,
                Key=index_key,
                Body=html_content.encode('utf-8'),
                ContentType='text/html',
                CacheControl='max-age=3600'
            )
        
        # Create resume URL record
        resume_url = f"https://{username}.skillsnap.me/{company_safe}/{jobtitle_safe}"
        db.create_resume_url(resume_url, userid, jobid)
        
        return api_response(200, {
            'message': f'{filename} generated successfully',
            's3Uri': s3_uri,
            'publicUrl': resume_url if file_type == 'resume' else f"{resume_url}/coverletter.html"
        })
        
    except Exception as e:
        print(f"Error generating HTML: {e}")
        return internal_error("Failed to generate HTML")
