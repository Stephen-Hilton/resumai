"""
Generation Type Toggle Lambda Handler

Toggles the generation type for a subcomponent.

Requirements: 7.7
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from shared.response import api_response, bad_request, not_found, internal_error
from shared.dynamodb import DynamoDBClient
from shared.validation import validate_subcomponent, validate_generation_type, VALID_SUBCOMPONENTS, VALID_GENERATION_TYPES


def handler(event, context):
    """
    Toggle generation type for a subcomponent.
    
    Path parameters:
    - jobid: ID of the job
    - component: Name of the subcomponent
    
    Request body:
    {
        "type": "manual" | "ai"
    }
    """
    try:
        # Get user ID from Cognito authorizer
        claims = event.get('requestContext', {}).get('authorizer', {}).get('claims', {})
        userid = claims.get('custom:userid') or claims.get('sub')
        
        if not userid:
            return bad_request("User ID not found in token")
        
        # Get path parameters
        path_params = event.get('pathParameters', {}) or {}
        jobid = path_params.get('jobid')
        component = path_params.get('component')
        
        if not jobid:
            return bad_request("jobid is required")
        
        if not component:
            return bad_request("component is required")
        
        if not validate_subcomponent(component):
            return bad_request(f"Invalid component. Must be one of: {', '.join(VALID_SUBCOMPONENTS)}")
        
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        new_type = body.get('type')
        
        if not new_type:
            return bad_request("type is required")
        
        if not validate_generation_type(new_type):
            return bad_request(f"Invalid type. Must be one of: {', '.join(VALID_GENERATION_TYPES)}")
        
        db = DynamoDBClient()
        
        # Get user-job
        user_job = db.get_user_job(userid, jobid)
        if not user_job:
            return not_found(f"Job '{jobid}' not found")
        
        # Update generation type
        updated = db.update_user_job(userid, jobid, {f'type{component}': new_type})
        
        return api_response(200, {
            'message': f'Generation type for {component} updated to {new_type}',
            'component': component,
            'type': new_type
        })
        
    except json.JSONDecodeError:
        return bad_request("Invalid JSON in request body")
    except Exception as e:
        print(f"Error toggling type: {e}")
        return internal_error("Failed to toggle generation type")
