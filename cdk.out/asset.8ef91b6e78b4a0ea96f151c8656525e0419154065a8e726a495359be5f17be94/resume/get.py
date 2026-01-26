"""
Resume Get Lambda Handler

Gets a resume by name for the authenticated user.

Requirements: 4.1
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from shared.response import api_response, bad_request, not_found, internal_error
from shared.dynamodb import DynamoDBClient


def handler(event, context):
    """
    Get a resume by name.
    
    Path parameters:
    - resumename: Name of the resume to retrieve
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
        
        # Get resume
        db = DynamoDBClient()
        resume = db.get_resume(userid, resumename)
        
        if not resume:
            return not_found(f"Resume '{resumename}' not found")
        
        return api_response(200, {'resume': resume})
        
    except Exception as e:
        print(f"Error getting resume: {e}")
        return internal_error("Failed to get resume")
