"""
Generate All Lambda Handler

Queues generation for all 8 subcomponents.

Requirements: 7.8, 16.1, 16.2
"""
import json
import os
import sys
import boto3
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from shared.response import api_response, bad_request, not_found, internal_error
from shared.dynamodb import DynamoDBClient
from shared.validation import VALID_SUBCOMPONENTS

# SQS client
sqs = boto3.client('sqs')
QUEUE_URL = os.environ.get('GENERATION_QUEUE_URL', '')


def handler(event, context):
    """
    Queue generation for all 8 subcomponents.
    
    Path parameters:
    - jobid: ID of the job to generate for
    """
    try:
        # Get user ID from Cognito authorizer
        claims = event.get('requestContext', {}).get('authorizer', {}).get('claims', {})
        userid = claims.get('custom:userid') or claims.get('sub')
        
        if not userid:
            return bad_request("User ID not found in token")
        
        # Get job ID from path
        path_params = event.get('pathParameters', {}) or {}
        jobid = path_params.get('jobid')
        
        if not jobid:
            return bad_request("jobid is required")
        
        db = DynamoDBClient()
        
        # Get user-job
        user_job = db.get_user_job(userid, jobid)
        if not user_job:
            return not_found(f"Job '{jobid}' not found")
        
        resumeid = user_job.get('resumeid')
        if not resumeid:
            return bad_request("No resume associated with this job")
        
        # Queue messages for all 8 subcomponents
        timestamp = datetime.utcnow().isoformat()
        queued_count = 0
        
        for component in VALID_SUBCOMPONENTS:
            # Get generation type for this component
            gen_type = user_job.get(f'type{component}', 'ai')
            
            message = {
                'userid': userid,
                'jobid': jobid,
                'resumeid': resumeid,
                'component': component,
                'generationType': gen_type,
                'timestamp': timestamp
            }
            
            try:
                # Build SQS params - only include MessageGroupId for FIFO queues
                sqs_params = {
                    'QueueUrl': QUEUE_URL,
                    'MessageBody': json.dumps(message),
                }
                if '.fifo' in QUEUE_URL:
                    sqs_params['MessageGroupId'] = f"{userid}-{jobid}"
                
                sqs.send_message(**sqs_params)
                queued_count += 1
            except Exception as sqs_error:
                print(f"Error queuing {component}: {sqs_error}")
        
        # Update all generation states to "generating"
        updates = {f'state{comp}': 'generating' for comp in VALID_SUBCOMPONENTS}
        updates['jobphase'] = 'Generating'
        db.update_user_job(userid, jobid, updates)
        
        return api_response(202, {
            'message': f'Queued {queued_count} subcomponents for generation',
            'jobid': jobid,
            'status': 'generating'
        })
        
    except Exception as e:
        print(f"Error in generate all: {e}")
        return internal_error("Failed to queue generation")
