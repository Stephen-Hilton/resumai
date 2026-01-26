"""
Generate Single Subcomponent Lambda Handler

Queues generation for a single subcomponent.

Requirements: 7.2, 7.3
"""
import json
import os
import sys
import boto3
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from shared.response import api_response, bad_request, not_found, internal_error
from shared.dynamodb import DynamoDBClient
from shared.validation import validate_subcomponent, VALID_SUBCOMPONENTS

# SQS client
sqs = boto3.client('sqs')
QUEUE_URL = os.environ.get('GENERATION_QUEUE_URL', '')


def handler(event, context):
    """
    Queue generation for a single subcomponent.
    
    Path parameters:
    - jobid: ID of the job
    - component: Name of the subcomponent to generate
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
        
        db = DynamoDBClient()
        
        # Get user-job
        user_job = db.get_user_job(userid, jobid)
        if not user_job:
            return not_found(f"Job '{jobid}' not found")
        
        # Check generation state
        current_state = user_job.get(f'state{component}', 'locked')
        if current_state == 'locked':
            return bad_request(f"Cannot generate {component}: state is locked")
        
        if current_state == 'generating':
            return bad_request(f"Generation already in progress for {component}")
        
        resumeid = user_job.get('resumeid')
        if not resumeid:
            return bad_request("No resume associated with this job")
        
        # Get generation type for this component
        gen_type = user_job.get(f'type{component}', 'ai')
        
        # Queue message
        message = {
            'userid': userid,
            'jobid': jobid,
            'resumeid': resumeid,
            'component': component,
            'generationType': gen_type,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps(message),
            MessageGroupId=f"{userid}-{jobid}" if '.fifo' in QUEUE_URL else None,
        )
        
        # Update generation state to "generating"
        db.update_user_job(userid, jobid, {f'state{component}': 'generating'})
        
        return api_response(202, {
            'message': f'Queued {component} for generation',
            'jobid': jobid,
            'component': component,
            'status': 'generating'
        })
        
    except Exception as e:
        print(f"Error in generate single: {e}")
        return internal_error("Failed to queue generation")
