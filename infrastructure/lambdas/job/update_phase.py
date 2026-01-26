"""
Job Update Phase Lambda Handler

Updates the phase of a job.

Requirements: 6.5, 12.1, 12.6
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from shared.response import api_response, bad_request, not_found, internal_error
from shared.dynamodb import DynamoDBClient
from shared.validation import validate_job_phase, VALID_PHASES


def handler(event, context):
    """
    Update job phase.
    
    Path parameters:
    - jobid: ID of the job to update
    
    Request body:
    {
        "phase": "string" (one of valid phases)
    }
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
        
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        phase = body.get('phase')
        
        if not phase:
            return bad_request("phase is required")
        
        if not validate_job_phase(phase):
            return bad_request(f"Invalid phase. Must be one of: {', '.join(VALID_PHASES)}")
        
        db = DynamoDBClient()
        
        # Check if user-job exists
        user_job = db.get_user_job(userid, jobid)
        if not user_job:
            return not_found(f"Job '{jobid}' not found")
        
        # Update phase
        updated = db.update_user_job(userid, jobid, {'jobphase': phase})
        
        return api_response(200, {
            'message': 'Phase updated successfully',
            'userJob': updated
        })
        
    except json.JSONDecodeError:
        return bad_request("Invalid JSON in request body")
    except Exception as e:
        print(f"Error updating job phase: {e}")
        return internal_error("Failed to update job phase")
