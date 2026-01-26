"""
Resume Update Lambda Handler

Updates a resume for the authenticated user.

Requirements: 4.2
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from shared.response import api_response, bad_request, not_found, internal_error
from shared.dynamodb import DynamoDBClient
from shared.validation import validate_resume_json


def handler(event, context):
    """
    Update a resume.
    
    Path parameters:
    - resumename: Name of the resume to update
    
    Request body:
    {
        "resumejson": { ... updated resume JSON ... }
    }
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
        
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        resumejson = body.get('resumejson')
        
        if not resumejson:
            return bad_request("resumejson is required")
        
        # Validate resume JSON
        is_valid, errors = validate_resume_json(resumejson)
        if not is_valid:
            return bad_request("Invalid resume JSON", errors)
        
        # Check if resume exists
        db = DynamoDBClient()
        existing = db.get_resume(userid, resumename)
        
        if not existing:
            return not_found(f"Resume '{resumename}' not found")
        
        # Update resume
        updated = db.update_resume(userid, resumename, resumejson)
        
        return api_response(200, {
            'message': 'Resume updated successfully',
            'resume': updated
        })
        
    except json.JSONDecodeError:
        return bad_request("Invalid JSON in request body")
    except Exception as e:
        print(f"Error updating resume: {e}")
        return internal_error("Failed to update resume")
