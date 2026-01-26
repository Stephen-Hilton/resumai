"""
Post Confirmation Lambda Handler

Creates USER, USER_EMAIL, and USER_USERNAME records when a new user signs up.

Requirements: 1.2, 15.2, 15.3
"""
import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    import uuid7
except ImportError:
    import uuid
    class uuid7:
        @staticmethod
        def uuid7():
            return uuid.uuid4()

from shared.dynamodb import DynamoDBClient


def handler(event, context):
    """
    Cognito Post Confirmation trigger.
    
    Creates user records in DynamoDB when a new user confirms their account.
    """
    try:
        print(f"Post confirmation event: {json.dumps(event)}")
        
        # Only process confirmed signups
        trigger_source = event.get('triggerSource', '')
        if trigger_source not in ['PostConfirmation_ConfirmSignUp', 'PostConfirmation_ConfirmForgotPassword']:
            print(f"Skipping trigger source: {trigger_source}")
            return event
        
        # Get user attributes
        user_attributes = event.get('request', {}).get('userAttributes', {})
        cognito_sub = user_attributes.get('sub', '')
        email = user_attributes.get('email', '')
        username = event.get('userName', '')
        userhandle = user_attributes.get('preferred_username', '') or user_attributes.get('name', '') or username
        
        if not email:
            print("No email found in user attributes")
            return event
        
        db = DynamoDBClient()
        
        # Check if user already exists (for idempotency)
        existing_user = db.get_user_by_email(email)
        if existing_user:
            print(f"User already exists for email: {email}")
            return event
        
        # Generate new user ID
        userid = str(uuid7.uuid7())
        
        # Create USER record
        user_data = {
            'userid': userid,
            'userhandle': userhandle,
            'email': email,
            'username': username,
            'cognitoSub': cognito_sub,
            'gmailConnected': False,
        }
        
        db.create_user(user_data)
        print(f"Created user: {userid}")
        
        # Create USER_EMAIL record for uniqueness
        if not db.create_user_email(email, userid):
            print(f"Email already exists: {email}")
            # This shouldn't happen if we checked above, but handle it gracefully
        
        # Create USER_USERNAME record for uniqueness
        if username:
            if not db.create_user_username(username, userid):
                print(f"Username already exists: {username}")
                # Username collision - user can still use the account
        
        # Set default preferences
        default_prefs = {
            'default_gen_contact': 'manual',
            'default_gen_summary': 'ai',
            'default_gen_skills': 'ai',
            'default_gen_highlights': 'ai',
            'default_gen_experience': 'ai',
            'default_gen_education': 'manual',
            'default_gen_awards': 'manual',
            'default_gen_coverletter': 'ai',
        }
        
        for prefname, prefvalue in default_prefs.items():
            db.set_user_pref(userid, prefname, prefvalue)
        
        print(f"Set default preferences for user: {userid}")
        
        return event
        
    except Exception as e:
        print(f"Error in post confirmation: {e}")
        # Don't fail the signup, just log the error
        return event
