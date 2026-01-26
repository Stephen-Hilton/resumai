"""
Job Expiration Lambda Handler

Scheduled Lambda that expires jobs older than 30 days.

Requirements: 12.7
"""
import os
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from shared.dynamodb import DynamoDBClient
from shared.validation import VALID_PHASES

# Phases that should not be expired
TERMINAL_PHASES = {'Accepted', 'Skipped', 'Expired'}

# Days after which a job expires
EXPIRATION_DAYS = 30


def handler(event, context):
    """
    Expire jobs older than 30 days that are not in terminal phases.
    
    This Lambda is triggered by EventBridge schedule (daily).
    """
    try:
        db = DynamoDBClient()
        
        # Calculate expiration cutoff date
        cutoff_date = (datetime.utcnow() - timedelta(days=EXPIRATION_DAYS)).strftime('%Y-%m-%d')
        
        # Get all jobs (this would need pagination in production)
        # For MVP, we scan the JOB table
        import boto3
        dynamodb = boto3.resource('dynamodb')
        job_table = dynamodb.Table(os.environ.get('JOB_TABLE', 'skillsnap-job'))
        user_job_table = dynamodb.Table(os.environ.get('USER_JOB_TABLE', 'skillsnap-user-job'))
        
        # Scan for old jobs
        response = job_table.scan(
            FilterExpression='jobposteddate < :cutoff',
            ExpressionAttributeValues={':cutoff': cutoff_date}
        )
        
        expired_count = 0
        
        for job in response.get('Items', []):
            jobid = job['jobid']
            
            # Find all user-job records for this job
            user_jobs_response = user_job_table.scan(
                FilterExpression='jobid = :jobid',
                ExpressionAttributeValues={':jobid': jobid}
            )
            
            for user_job in user_jobs_response.get('Items', []):
                current_phase = user_job.get('jobphase', 'Search')
                
                # Only expire if not in terminal phase
                if current_phase not in TERMINAL_PHASES:
                    userid = user_job['userid']
                    db.update_user_job(userid, jobid, {'jobphase': 'Expired'})
                    expired_count += 1
                    print(f"Expired job {jobid} for user {userid}")
        
        return {
            'statusCode': 200,
            'body': {
                'message': f'Expired {expired_count} jobs',
                'cutoffDate': cutoff_date
            }
        }
        
    except Exception as e:
        print(f"Error expiring jobs: {e}")
        return {
            'statusCode': 500,
            'body': {'error': str(e)}
        }
