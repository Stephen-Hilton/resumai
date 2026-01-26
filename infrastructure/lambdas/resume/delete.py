"""
Resume Delete Lambda Handler

Deletes a resume for the authenticated user.

Requirements: 4.5
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from shared.response import api_response, bad_request, not_found, internal_error
from shared.dynamodb import DynamoDBClient


def handler(event, context):
    """
    Delete a resume.
    
    Path parameters:
    - resumename: Name of the resume to delete
    """
    try:
        # Get user ID from Cognito authorizer
        claims = event.get('requestContext', {}).get('authorizer', {}).get('claims', {})
        userid = claims.get('custom:userid') or claims.get('sub')
        
        if not userid:
            return bad_request("User ID not found in token")
        
        # Get resume name from path
        path_params = event.get('pathParameters', {}) or {}
        resumename = path_params.get('resumename')
        
        if not resumename:
            return bad_request("resumename is required")
        
        # URL decode the resume name
        from urllib.parse import unquote
        resumename = unquote(resumename)
        
        # Check if resume exists
        db = DynamoDBClient()
        existing = db.get_resume(userid, resumename)
        
        if not existing:
            return not_found(f"Resume '{resumename}' not found")
        
        # Delete resume
        db.delete_resume(userid, resumename)
        
        return api_response(200, {
            'message': f"Resume '{resumename}' deleted successfully"
        })
        
    except Exception as e:
        print(f"Error deleting resume: {e}")
        return internal_error("Failed to delete resume")
