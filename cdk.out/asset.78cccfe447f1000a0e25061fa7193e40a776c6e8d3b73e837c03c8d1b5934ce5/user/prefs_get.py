"""
User Preferences Get Lambda Handler

Gets all preferences for the authenticated user.

Requirements: 13.1
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from shared.response import api_response, bad_request, internal_error
from shared.dynamodb import DynamoDBClient


def handler(event, context):
    """
    Get all preferences for the authenticated user.
    """
    try:
        # Get user ID from Cognito authorizer
        claims = event.get('requestContext', {}).get('authorizer', {}).get('claims', {})
        userid = claims.get('custom:userid') or claims.get('sub')
        
        if not userid:
            return bad_request("User ID not found in token")
        
        db = DynamoDBClient()
        prefs = db.get_user_prefs(userid)
        
        return api_response(200, {'preferences': prefs})
        
    except Exception as e:
        print(f"Error getting preferences: {e}")
        return internal_error("Failed to get preferences")
