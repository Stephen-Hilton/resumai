"""
Event: upload_s3

Uploads resume.pdf and coverletter.pdf to S3 bucket.
This is an optional event - failures don't move job to Errored phase.

Requirements: 13.1, 13.2, 13.3, 13.4, 13.5
"""

from pathlib import Path
from src.lib.types import EventContext, EventResult
from src.lib.logging_utils import append_app_log, append_job_log
from src.lib.yaml_utils import load_yaml
import os

# Logs directory
LOGS_DIR = Path("src/logs")


async def execute(job_path: Path, ctx: EventContext) -> EventResult:
    """
    Upload resume.pdf and coverletter.pdf to S3 bucket.
    
    Args:
        job_path: Path to the job folder
        ctx: Event context with configuration
        
    Returns:
        EventResult with S3 URLs in artifacts
    """
    try:
        # Get S3 bucket from environment
        bucket_name = os.getenv("S3_RESUME_BUCKET")
        
        if not bucket_name:
            message = "S3_RESUME_BUCKET not configured - skipping S3 upload"
            append_app_log(LOGS_DIR, f"upload_s3: {message}")
            append_job_log(job_path, f"upload_s3: {message}")
            return EventResult(ok=True, message=message, job_path=job_path)
        
        # Load job.yaml to get job ID
        job_yaml_path = job_path / "job.yaml"
        if not job_yaml_path.exists():
            message = "job.yaml not found"
            append_app_log(LOGS_DIR, f"upload_s3: ERROR: {message}")
            append_job_log(job_path, f"upload_s3: ERROR: {message}")
            return EventResult(ok=False, message=message, job_path=job_path)
        
        job_data = load_yaml(job_yaml_path)
        job_id = job_data.get("id", "unknown")
        
        # Check if PDF files exist
        resume_pdf = job_path / "resume.pdf"
        coverletter_pdf = job_path / "coverletter.pdf"
        
        if not resume_pdf.exists() and not coverletter_pdf.exists():
            message = "No PDF files found to upload"
            append_app_log(LOGS_DIR, f"upload_s3: {message}")
            append_job_log(job_path, f"upload_s3: {message}")
            return EventResult(ok=False, message=message, job_path=job_path)
        
        # Import boto3 (AWS SDK)
        try:
            import boto3
            from botocore.exceptions import ClientError, NoCredentialsError
        except ImportError:
            message = "boto3 not installed - run: pip install boto3"
            append_app_log(LOGS_DIR, f"upload_s3: ERROR: {message}")
            append_job_log(job_path, f"upload_s3: ERROR: {message}")
            return EventResult(ok=False, message=message, job_path=job_path)
        
        # Create S3 client
        try:
            s3_client = boto3.client('s3')
        except NoCredentialsError:
            message = "AWS credentials not configured - set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY"
            append_app_log(LOGS_DIR, f"upload_s3: ERROR: {message}")
            append_job_log(job_path, f"upload_s3: ERROR: {message}")
            return EventResult(ok=False, message=message, job_path=job_path)
        
        uploaded_files = []
        s3_urls = []
        
        # Upload resume.pdf
        if resume_pdf.exists():
            s3_key = f"resume.{job_id}.pdf"
            try:
                s3_client.upload_file(
                    str(resume_pdf),
                    bucket_name,
                    s3_key,
                    ExtraArgs={'ContentType': 'application/pdf'}
                )
                s3_url = f"https://{bucket_name}.s3.amazonaws.com/{s3_key}"
                uploaded_files.append("resume.pdf")
                s3_urls.append(s3_url)
                append_app_log(LOGS_DIR, f"upload_s3: Uploaded resume.pdf to {s3_url}")
                append_job_log(job_path, f"upload_s3: Uploaded resume.pdf to {s3_url}")
            except ClientError as e:
                error_msg = f"Failed to upload resume.pdf: {str(e)}"
                append_app_log(LOGS_DIR, f"upload_s3: ERROR: {error_msg}")
                append_job_log(job_path, f"upload_s3: ERROR: {error_msg}")
        
        # Upload coverletter.pdf
        if coverletter_pdf.exists():
            s3_key = f"coverletter.{job_id}.pdf"
            try:
                s3_client.upload_file(
                    str(coverletter_pdf),
                    bucket_name,
                    s3_key,
                    ExtraArgs={'ContentType': 'application/pdf'}
                )
                s3_url = f"https://{bucket_name}.s3.amazonaws.com/{s3_key}"
                uploaded_files.append("coverletter.pdf")
                s3_urls.append(s3_url)
                append_app_log(LOGS_DIR, f"upload_s3: Uploaded coverletter.pdf to {s3_url}")
                append_job_log(job_path, f"upload_s3: Uploaded coverletter.pdf to {s3_url}")
            except ClientError as e:
                error_msg = f"Failed to upload coverletter.pdf: {str(e)}"
                append_app_log(LOGS_DIR, f"upload_s3: ERROR: {error_msg}")
                append_job_log(job_path, f"upload_s3: ERROR: {error_msg}")
        
        if not uploaded_files:
            message = "Failed to upload any files to S3"
            return EventResult(ok=False, message=message, job_path=job_path)
        
        message = f"Uploaded {len(uploaded_files)} file(s) to S3: {', '.join(uploaded_files)}"
        return EventResult(
            ok=True,
            message=message,
            job_path=job_path,
            artifacts=s3_urls
        )
    
    except Exception as e:
        import traceback
        error_msg = f"Unexpected error during S3 upload: {str(e)}"
        append_app_log(LOGS_DIR, f"upload_s3: ERROR: {error_msg}")
        append_app_log(LOGS_DIR, f"upload_s3: TRACEBACK: {traceback.format_exc()}")
        append_job_log(job_path, f"upload_s3: ERROR: {error_msg}")
        return EventResult(
            ok=False,
            message=error_msg,
            job_path=job_path,
            errors=[{"exception": repr(e), "traceback": traceback.format_exc()}]
        )


async def test(job_path: Path, ctx: EventContext) -> EventResult:
    """Test mode - same as execute but with test_mode flag."""
    return await execute(job_path, ctx)
