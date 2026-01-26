"""
User Preferences Update Lambda Handler

Updates preferences for the authenticated user.

Requirements: 13.2, 13.4
"""
import json
import os
import sys
import re

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from shared.response import api_response, bad_request, internal_error
from shared.dynamodb import DynamoDBClient
from shared.validation import VALID_SUBCOMPONENTS, VALID_GENERATION_TYPES

# Valid boolean preferences
VALID_BOOLEAN_PREFS = [
    'show_year_education',
    'show_year_awards', 
    'show_year_keynotes',
    'combine_awards_keynotes',
]

# Valid integer preferences
VALID_INTEGER_PREFS = [
    'cutoff_year',
]


def validate_pref_name(prefname: str) -> tuple:
    """
    Validate preference name.
    Returns (is_valid, error_message).
    """
    # Check if it's a generation type preference
    match = re.match(r'^default_gen_(\w+)$', prefname)
    if match:
        component = match.group(1)
        if component not in VALID_SUBCOMPONENTS:
            return False, f"Invalid subcomponent: {component}. Must be one of: {', '.join(VALID_SUBCOMPONENTS)}"
        return True, None
    
    # Check if it's a valid boolean preference
    if prefname in VALID_BOOLEAN_PREFS:
        return True, None
    
    # Check if it's a valid integer preference
    if prefname in VALID_INTEGER_PREFS:
        return True, None
    
    return False, f"Invalid preference name: {prefname}"


def handler(event, context):
    """
    Update user preferences.
    
    Request body:
    {
        "preferences": {
            "prefname": "prefvalue",
            ...
        }
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
        preferences = body.get('preferences', {})
        
        if not preferences:
            return bad_request("preferences object is required")
        
        if not isinstance(preferences, dict):
            return bad_request("preferences must be an object")
        
        db = DynamoDBClient()
        errors = []
        updated = {}
        
        for prefname, prefvalue in preferences.items():
            # Validate preference name
            is_valid, error = validate_pref_name(prefname)
            if not is_valid:
                errors.append(error)
                continue
            
            # Validate generation type values
            if prefname.startswith('default_gen_'):
                if prefvalue not in VALID_GENERATION_TYPES:
                    errors.append(f"Invalid value for {prefname}. Must be one of: {', '.join(VALID_GENERATION_TYPES)}")
                    continue
            
            # Convert boolean values to string for storage
            if prefname in VALID_BOOLEAN_PREFS:
                prefvalue = 'true' if prefvalue else 'false'
            
            # Convert integer values to string for storage
            if prefname in VALID_INTEGER_PREFS:
                if prefvalue is None:
                    # Skip None values (no cutoff)
                    db.delete_user_pref(userid, prefname)
                    updated[prefname] = None
                    continue
                prefvalue = str(prefvalue)
            
            # Set preference
            db.set_user_pref(userid, prefname, prefvalue)
            updated[prefname] = prefvalue
        
        if errors:
            return bad_request("Some preferences could not be updated", errors)
        
        return api_response(200, {
            'message': 'Preferences updated successfully',
            'updated': updated
        })
        
    except json.JSONDecodeError:
        return bad_request("Invalid JSON in request body")
    except Exception as e:
        print(f"Error updating preferences: {e}")
        return internal_error("Failed to update preferences")
