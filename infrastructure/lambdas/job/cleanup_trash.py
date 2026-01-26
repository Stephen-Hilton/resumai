"""
Job Cleanup Trash Lambda Handler

Removes jobs that have been in the Trash phase for more than 7 days.
Triggered daily by EventBridge scheduled rule.

Requirements: Automated cleanup
"""
import os
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from shared.dynamodb import DynamoDBClient

# Number of days before trash items are permanently deleted
TRASH_RETENTION_DAYS = 7


def handler(event, context):
    """
    Scan for jobs in Trash phase older than TRASH_RETENTION_DAYS and delete them.
    """
    db = DynamoDBClient()
    cutoff_date = datetime.utcnow() - timedelta(days=TRASH_RETENTION_DAYS)
    cutoff_iso = cutoff_date.isoformat()
    
    deleted_count = 0
    errors = []
    
    try:
        # Scan user_job table for items in Trash phase
        # Note: In production with large datasets, consider using a GSI on jobphase
        response = db.user_job_table.scan(
            FilterExpression='jobphase = :phase',
            ExpressionAttributeValues={':phase': 'Trash'}
        )
        
        items = response.get('Items', [])
        
        # Handle pagination
        while 'LastEvaluatedKey' in response:
            response = db.user_job_table.scan(
                FilterExpression='jobphase = :phase',
                ExpressionAttributeValues={':phase': 'Trash'},
                ExclusiveStartKey=response['LastEvaluatedKey']
            )
            items.extend(response.get('Items', []))
        
        print(f"Found {len(items)} jobs in Trash phase")
        
        for item in items:
            userid = item.get('userid')
            jobid = item.get('jobid')
            updated_at = item.get('updatedAt', '')
            
            # Check if the job has been in trash long enough
            if updated_at and updated_at < cutoff_iso:
                try:
                    # Delete user-job record
                    db.delete_user_job(userid, jobid)
                    
                    # Delete job record
                    db.delete_job(jobid)
                    
                    deleted_count += 1
                    print(f"Deleted job {jobid} for user {userid} (in trash since {updated_at})")
                    
                except Exception as e:
                    error_msg = f"Failed to delete job {jobid}: {str(e)}"
                    print(error_msg)
                    errors.append(error_msg)
        
        result = {
            'statusCode': 200,
            'body': {
                'message': f'Trash cleanup complete',
                'scanned': len(items),
                'deleted': deleted_count,
                'errors': len(errors),
                'cutoffDate': cutoff_iso
            }
        }
        
        print(f"Cleanup complete: {deleted_count} jobs deleted, {len(errors)} errors")
        return result
        
    except Exception as e:
        print(f"Error during trash cleanup: {e}")
        return {
            'statusCode': 500,
            'body': {
                'message': 'Trash cleanup failed',
                'error': str(e)
            }
        }
