"""
Resume List Lambda Handler

Lists all resumes for the authenticated user.

Requirements: 4.1
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from shared.response import api_response, bad_request, internal_error
from shared.dynamodb import DynamoDBClient


def handler(event, context):
    """
    List all resumes for the authenticated user.
    """
    try:
        # Get user ID from Cognito authorizer
        claims = event.get('requestContext', {}).get('authorizer', {}).get('claims', {})
        userid = claims.get('custom:userid') or claims.get('sub')
        
        if not userid:
            return bad_request("User ID not found in token")
        
        # List resumes
        db = DynamoDBClient()
        resumes = db.list_resumes(userid)
        
        # Return summary info (without full resumejson for list view)
        resume_list = []
        for resume in resumes:
            resume_list.append({
                'userid': resume['userid'],
                'resumename': resume['resumename'],
                'lastupdate': resume.get('lastupdate'),
                'contact_name': resume.get('resumejson', {}).get('contact', {}).get('name', ''),
            })
        
        return api_response(200, {
            'resumes': resume_list,
            'count': len(resume_list)
        })
        
    except Exception as e:
        print(f"Error listing resumes: {e}")
        return internal_error("Failed to list resumes")
