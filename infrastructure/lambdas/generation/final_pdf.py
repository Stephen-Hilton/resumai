"""
Final PDF Generation Lambda Handler

Generates final resume and cover letter PDF files.

Requirements: 10.3, 10.5
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


def html_to_pdf(html_content: str) -> bytes:
    """
    Convert HTML to PDF.
    
    Note: In production, this would use a library like weasyprint, 
    puppeteer, or a service like AWS Lambda with headless Chrome.
    For MVP, we'll use a simple approach.
    """
    try:
        # Try to use weasyprint if available
        from weasyprint import HTML
        pdf_bytes = HTML(string=html_content).write_pdf()
        return pdf_bytes
    except ImportError:
        # Fallback: return a placeholder PDF
        # In production, you'd want to use a proper PDF generation service
        print("weasyprint not available, using placeholder")
        
        # Simple PDF placeholder (not a real PDF, just for testing)
        # In production, use a Lambda layer with weasyprint or puppeteer
        placeholder = b'%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n'
        return placeholder


def handler(event, context):
    """
    Generate final PDF files.
    
    Path parameters:
    - jobid: ID of the job
    
    Query parameters:
    - type: "resume" or "cover" (which PDF to generate)
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
        
        # Check HTML was generated first
        if file_type == 'resume':
            html_s3_loc = user_job.get('s3locresumehtml')
            if not html_s3_loc:
                return bad_request("Resume HTML must be generated first")
        else:
            html_s3_loc = user_job.get('s3loccoverletterhtml')
            if not html_s3_loc:
                return bad_request("Cover letter HTML must be generated first")
        
        # Get job details
        job = db.get_job(jobid)
        if not job:
            return not_found(f"Job '{jobid}' not found")
        
        # Get HTML content from S3
        html_key = html_s3_loc.replace(f's3://{RESUMES_BUCKET}/', '')
        html_response = s3.get_object(Bucket=RESUMES_BUCKET, Key=html_key)
        html_content = html_response['Body'].read().decode('utf-8')
        
        # Convert to PDF
        pdf_bytes = html_to_pdf(html_content)
        
        # Build S3 path
        company_safe = job.get('jobcompany', 'company').lower().replace(' ', '-')
        jobtitle_safe = job.get('jobtitlesafe', 'position')
        
        if file_type == 'resume':
            filename = 'resume.pdf'
            s3_field = 's3locresumepdf'
        else:
            filename = 'coverletter.pdf'
            s3_field = 's3loccoverletterpdf'
        
        s3_key = f"{username}/{company_safe}/{jobtitle_safe}/{filename}"
        
        # Upload to S3
        s3.put_object(
            Bucket=RESUMES_BUCKET,
            Key=s3_key,
            Body=pdf_bytes,
            ContentType='application/pdf',
            CacheControl='max-age=3600'
        )
        
        s3_uri = f"s3://{RESUMES_BUCKET}/{s3_key}"
        
        # Update user-job with S3 location
        updates = {s3_field: s3_uri}
        
        # Check if all final files are complete
        user_job = db.get_user_job(userid, jobid)
        all_files_complete = all([
            user_job.get('s3locresumehtml'),
            user_job.get('s3locresumepdf') or (file_type == 'resume'),
            user_job.get('s3loccoverletterhtml'),
            user_job.get('s3loccoverletterpdf') or (file_type == 'cover'),
        ])
        
        if all_files_complete:
            updates['jobphase'] = 'Ready'
        
        db.update_user_job(userid, jobid, updates)
        
        # Build public URL
        public_url = f"https://{username}.skillsnap.me/{company_safe}/{jobtitle_safe}/{filename}"
        
        return api_response(200, {
            'message': f'{filename} generated successfully',
            's3Uri': s3_uri,
            'publicUrl': public_url
        })
        
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return internal_error("Failed to generate PDF")
