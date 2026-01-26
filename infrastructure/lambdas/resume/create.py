"""
Resume Create Lambda Handler

Creates a new resume for the authenticated user.

Requirements: 4.1, 4.4
"""
import json
import os
import sys

# Add shared module to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from shared.response import api_response, bad_request, internal_error
from shared.dynamodb import DynamoDBClient
from shared.validation import validate_resume_json


def handler(event, context):
    """
    Create a new resume.
    
    Request body:
    {
        "resumename": "string",
        "resumejson": { ... resume JSON ... }
    }
    """
    try:
        # Get user ID from Cognito authorizer
        claims = event.get('requestContext', {}).get('authorizer', {}).get('claims', {})
        userid = claims.get('custom:userid') or claims.get('sub')
        
        if not userid:
            return bad_request("User ID not found in token")
        
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        
        resumename = body.get('resumename')
        resumejson = body.get('resumejson')
        
        if not resumename:
            return bad_request("resumename is required")
        
        if not resumejson:
            return bad_request("resumejson is required")
        
        # Validate resume JSON
        is_valid, errors = validate_resume_json(resumejson)
        if not is_valid:
            print(f"Validation errors: {errors}")
            print(f"Resume JSON contact: {resumejson.get('contact', {})}")
            return bad_request("Invalid resume JSON", errors)
        
        # Create resume
        db = DynamoDBClient()
        
        # Check if resume with same name exists
        existing = db.get_resume(userid, resumename)
        if existing:
            return bad_request(f"Resume '{resumename}' already exists")
        
        resume_data = {
            'userid': userid,
            'resumename': resumename,
            'resumejson': resumejson,
        }
        
        created = db.create_resume(resume_data)
        
        return api_response(201, {
            'message': 'Resume created successfully',
            'resume': created
        })
        
    except json.JSONDecodeError:
        return bad_request("Invalid JSON in request body")
    except Exception as e:
        print(f"Error creating resume: {e}")
        return internal_error("Failed to create resume")
