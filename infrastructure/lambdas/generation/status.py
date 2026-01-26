"""
Generation Status Lambda Handler

Returns the current generation status for all subcomponents.

Requirements: 7.4, 7.5
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from shared.response import api_response, bad_request, not_found, internal_error
from shared.dynamodb import DynamoDBClient
from shared.validation import VALID_SUBCOMPONENTS


def handler(event, context):
    """
    Get generation status for all subcomponents.
    
    Path parameters:
    - jobid: ID of the job
    """
    try:
        # Get user ID from Cognito authorizer
        claims = event.get('requestContext', {}).get('authorizer', {}).get('claims', {})
        userid = claims.get('custom:userid') or claims.get('sub')
        
        if not userid:
            return bad_request("User ID not found in token")
        
        # Get job ID from path
        path_params = event.get('pathParameters', {}) or {}
        jobid = path_params.get('jobid')
        
        if not jobid:
            return bad_request("jobid is required")
        
        db = DynamoDBClient()
        
        # Get user-job
        user_job = db.get_user_job(userid, jobid)
        if not user_job:
            return not_found(f"Job '{jobid}' not found")
        
        # Build status response
        subcomponents = {}
        all_complete = True
        any_generating = False
        any_error = False
        
        for component in VALID_SUBCOMPONENTS:
            state = user_job.get(f'state{component}', 'locked')
            gen_type = user_job.get(f'type{component}', 'ai')
            data = user_job.get(f'data{component}', '')
            
            subcomponents[component] = {
                'state': state,
                'type': gen_type,
                'hasContent': bool(data),
            }
            
            if state != 'complete':
                all_complete = False
            if state == 'generating':
                any_generating = True
            if state == 'error':
                any_error = True
        
        # Determine overall status
        if all_complete:
            overall_status = 'complete'
        elif any_error:
            overall_status = 'error'
        elif any_generating:
            overall_status = 'generating'
        else:
            overall_status = 'ready'
        
        # Final files status
        final_files = {
            'resumeHtml': {
                'ready': all_complete,
                'generated': bool(user_job.get('s3locresumehtml')),
                's3loc': user_job.get('s3locresumehtml', '')
            },
            'resumePdf': {
                'ready': all_complete,
                'generated': bool(user_job.get('s3locresumepdf')),
                's3loc': user_job.get('s3locresumepdf', '')
            },
            'coverLetterHtml': {
                'ready': all_complete,
                'generated': bool(user_job.get('s3loccoverletterhtml')),
                's3loc': user_job.get('s3loccoverletterhtml', '')
            },
            'coverLetterPdf': {
                'ready': all_complete,
                'generated': bool(user_job.get('s3loccoverletterpdf')),
                's3loc': user_job.get('s3loccoverletterpdf', '')
            },
        }
        
        return api_response(200, {
            'jobid': jobid,
            'phase': user_job.get('jobphase', 'Search'),
            'overallStatus': overall_status,
            'subcomponents': subcomponents,
            'finalFiles': final_files,
            'allComplete': all_complete
        })
        
    except Exception as e:
        print(f"Error getting status: {e}")
        return internal_error("Failed to get generation status")
