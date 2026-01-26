"""
Job Get Lambda Handler

Gets a job by ID for the authenticated user.

Requirements: 6.1
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from shared.response import api_response, bad_request, not_found, internal_error
from shared.dynamodb import DynamoDBClient


def handler(event, context):
    """
    Get a job by ID.
    
    Path parameters:
    - jobid: ID of the job to retrieve
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
        
        # Get user-job relationship
        user_job = db.get_user_job(userid, jobid)
        if not user_job:
            return not_found(f"Job '{jobid}' not found")
        
        # Get job details
        job = db.get_job(jobid)
        if not job:
            return not_found(f"Job '{jobid}' not found")
        
        # Combine job and user-job data
        result = {**job, **user_job}
        
        return api_response(200, {'job': result})
        
    except Exception as e:
        print(f"Error getting job: {e}")
        return internal_error("Failed to get job")
