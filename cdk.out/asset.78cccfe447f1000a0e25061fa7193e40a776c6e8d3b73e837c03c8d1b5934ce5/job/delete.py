"""
Job Delete Lambda Handler

Deletes a job for the authenticated user.

Requirements: 5.4
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from shared.response import api_response, bad_request, not_found, internal_error
from shared.dynamodb import DynamoDBClient


def handler(event, context):
    """
    Delete a job.
    
    Path parameters:
    - jobid: ID of the job to delete
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
        
        # Check if user-job exists
        user_job = db.get_user_job(userid, jobid)
        if not user_job:
            return not_found(f"Job '{jobid}' not found")
        
        # Delete user-job relationship
        db.delete_user_job(userid, jobid)
        
        # Note: We don't delete the JOB record as other users might reference it
        # In a production system, you might want to check if any other users
        # reference this job and delete it if not
        
        return api_response(200, {
            'message': f"Job '{jobid}' deleted successfully"
        })
        
    except Exception as e:
        print(f"Error deleting job: {e}")
        return internal_error("Failed to delete job")
