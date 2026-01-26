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
from shared.validation import VALID_SUBCOMPONENTS

# Default generation types for each subcomponent
DEFAULT_GEN_TYPES = {
    'contact': 'manual',  # Contact info should default to manual (verbatim)
    'summary': 'ai',
    'skills': 'ai',
    'highlights': 'ai',
    'experience': 'ai',
    'education': 'ai',
    'awards': 'ai',
    'keynotes': 'ai',
    'coverletter': 'ai',
}


def handler(event, context):
    """
    Get all preferences for the authenticated user.
    Returns defaults for any preferences not explicitly set.
    """
    try:
        # Get user ID from Cognito authorizer
        claims = event.get('requestContext', {}).get('authorizer', {}).get('claims', {})
        userid = claims.get('custom:userid') or claims.get('sub')
        
        if not userid:
            return bad_request("User ID not found in token")
        
        db = DynamoDBClient()
        stored_prefs = db.get_user_prefs(userid)
        
        # Build full preferences with defaults for missing values
        prefs = {}
        
        # Generation type preferences
        for component in VALID_SUBCOMPONENTS:
            pref_name = f"default_gen_{component}"
            prefs[pref_name] = stored_prefs.get(pref_name, DEFAULT_GEN_TYPES.get(component, 'ai'))
        
        # Boolean preferences (with defaults)
        prefs['show_year_education'] = stored_prefs.get('show_year_education', 'false') == 'true'
        prefs['show_year_awards'] = stored_prefs.get('show_year_awards', 'false') == 'true'
        prefs['show_year_keynotes'] = stored_prefs.get('show_year_keynotes', 'false') == 'true'
        prefs['combine_awards_keynotes'] = stored_prefs.get('combine_awards_keynotes', 'true') == 'true'
        
        # Integer preferences (with defaults)
        cutoff_year = stored_prefs.get('cutoff_year')
        prefs['cutoff_year'] = int(cutoff_year) if cutoff_year else None
        
        return api_response(200, {'preferences': prefs})
        
    except Exception as e:
        print(f"Error getting preferences: {e}")
        return internal_error("Failed to get preferences")
