"""
DynamoDB utilities for Lambda functions.

Requirements: 15.1, 15.4, 15.5
"""
import os
import boto3
from boto3.dynamodb.conditions import Key, Attr
from typing import Any, Optional, Dict, List
from datetime import datetime


class DynamoDBClient:
    """Wrapper for DynamoDB operations with table name configuration."""
    
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        
        # Table names from environment or defaults
        self.user_table = self.dynamodb.Table(
            os.environ.get('USER_TABLE', 'skillsnap-user')
        )
        self.user_email_table = self.dynamodb.Table(
            os.environ.get('USER_EMAIL_TABLE', 'skillsnap-user-email')
        )
        self.user_username_table = self.dynamodb.Table(
            os.environ.get('USER_USERNAME_TABLE', 'skillsnap-user-username')
        )
        self.user_pref_table = self.dynamodb.Table(
            os.environ.get('USER_PREF_TABLE', 'skillsnap-user-pref')
        )
        self.job_table = self.dynamodb.Table(
            os.environ.get('JOB_TABLE', 'skillsnap-job')
        )
        self.user_job_table = self.dynamodb.Table(
            os.environ.get('USER_JOB_TABLE', 'skillsnap-user-job')
        )
        self.resume_table = self.dynamodb.Table(
            os.environ.get('RESUME_TABLE', 'skillsnap-resume')
        )
        self.resume_url_table = self.dynamodb.Table(
            os.environ.get('RESUME_URL_TABLE', 'skillsnap-resume-url')
        )
    
    # User operations
    def get_user(self, userid: str) -> Optional[Dict]:
        """Get user by userid."""
        response = self.user_table.get_item(Key={'userid': userid})
        return response.get('Item')
    
    def create_user(self, user_data: Dict) -> Dict:
        """Create a new user."""
        now = datetime.utcnow().isoformat()
        user_data['createdAt'] = now
        user_data['updatedAt'] = now
        self.user_table.put_item(Item=user_data)
        return user_data
    
    def update_user(self, userid: str, updates: Dict) -> Dict:
        """Update user fields."""
        updates['updatedAt'] = datetime.utcnow().isoformat()
        
        update_expr = "SET " + ", ".join(f"#{k} = :{k}" for k in updates.keys())
        expr_names = {f"#{k}": k for k in updates.keys()}
        expr_values = {f":{k}": v for k, v in updates.items()}
        
        response = self.user_table.update_item(
            Key={'userid': userid},
            UpdateExpression=update_expr,
            ExpressionAttributeNames=expr_names,
            ExpressionAttributeValues=expr_values,
            ReturnValues='ALL_NEW'
        )
        return response.get('Attributes', {})
    
    # User Email operations (uniqueness enforcement)
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email."""
        response = self.user_email_table.get_item(Key={'useremail': email.lower()})
        item = response.get('Item')
        if item:
            return self.get_user(item['userid'])
        return None
    
    def create_user_email(self, email: str, userid: str) -> bool:
        """Create user email mapping. Returns False if email exists."""
        try:
            self.user_email_table.put_item(
                Item={'useremail': email.lower(), 'userid': userid},
                ConditionExpression='attribute_not_exists(useremail)'
            )
            return True
        except self.dynamodb.meta.client.exceptions.ConditionalCheckFailedException:
            return False
    
    # User Username operations (uniqueness enforcement)
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Get user by username."""
        response = self.user_username_table.get_item(Key={'username': username.lower()})
        item = response.get('Item')
        if item:
            return self.get_user(item['userid'])
        return None
    
    def create_user_username(self, username: str, userid: str) -> bool:
        """Create username mapping. Returns False if username exists."""
        try:
            self.user_username_table.put_item(
                Item={'username': username.lower(), 'userid': userid},
                ConditionExpression='attribute_not_exists(username)'
            )
            return True
        except self.dynamodb.meta.client.exceptions.ConditionalCheckFailedException:
            return False
    
    # User Preferences operations
    def get_user_prefs(self, userid: str) -> Dict[str, str]:
        """Get all preferences for a user."""
        response = self.user_pref_table.query(
            KeyConditionExpression=Key('userid').eq(userid)
        )
        return {item['prefname']: item['prefvalue'] for item in response.get('Items', [])}
    
    def set_user_pref(self, userid: str, prefname: str, prefvalue: str) -> None:
        """Set a user preference."""
        self.user_pref_table.put_item(
            Item={'userid': userid, 'prefname': prefname, 'prefvalue': prefvalue}
        )
    
    def delete_user_pref(self, userid: str, prefname: str) -> None:
        """Delete a user preference."""
        self.user_pref_table.delete_item(
            Key={'userid': userid, 'prefname': prefname}
        )
    
    # Job operations
    def get_job(self, jobid: str) -> Optional[Dict]:
        """Get job by jobid."""
        response = self.job_table.get_item(Key={'jobid': jobid})
        return response.get('Item')
    
    def create_job(self, job_data: Dict) -> Dict:
        """Create a new job."""
        job_data['createdAt'] = datetime.utcnow().isoformat()
        self.job_table.put_item(Item=job_data)
        return job_data
    
    def update_job(self, jobid: str, updates: Dict) -> Dict:
        """Update job fields."""
        update_expr = "SET " + ", ".join(f"#{k} = :{k}" for k in updates.keys())
        expr_names = {f"#{k}": k for k in updates.keys()}
        expr_values = {f":{k}": v for k, v in updates.items()}
        
        response = self.job_table.update_item(
            Key={'jobid': jobid},
            UpdateExpression=update_expr,
            ExpressionAttributeNames=expr_names,
            ExpressionAttributeValues=expr_values,
            ReturnValues='ALL_NEW'
        )
        return response.get('Attributes', {})
    
    def delete_job(self, jobid: str) -> None:
        """Delete a job."""
        self.job_table.delete_item(Key={'jobid': jobid})
    
    # User-Job operations
    def get_user_job(self, userid: str, jobid: str) -> Optional[Dict]:
        """Get user-job relationship."""
        response = self.user_job_table.get_item(
            Key={'userid': userid, 'jobid': jobid}
        )
        return response.get('Item')
    
    def create_user_job(self, user_job_data: Dict) -> Dict:
        """Create a new user-job relationship."""
        now = datetime.utcnow().isoformat()
        user_job_data['createdAt'] = now
        user_job_data['updatedAt'] = now
        self.user_job_table.put_item(Item=user_job_data)
        return user_job_data
    
    def update_user_job(self, userid: str, jobid: str, updates: Dict) -> Dict:
        """Update user-job fields."""
        updates['updatedAt'] = datetime.utcnow().isoformat()
        
        update_expr = "SET " + ", ".join(f"#{k} = :{k}" for k in updates.keys())
        expr_names = {f"#{k}": k for k in updates.keys()}
        expr_values = {f":{k}": v for k, v in updates.items()}
        
        response = self.user_job_table.update_item(
            Key={'userid': userid, 'jobid': jobid},
            UpdateExpression=update_expr,
            ExpressionAttributeNames=expr_names,
            ExpressionAttributeValues=expr_values,
            ReturnValues='ALL_NEW'
        )
        return response.get('Attributes', {})
    
    def delete_user_job(self, userid: str, jobid: str) -> None:
        """Delete a user-job relationship."""
        self.user_job_table.delete_item(
            Key={'userid': userid, 'jobid': jobid}
        )
    
    def list_user_jobs(self, userid: str, phase: Optional[str] = None) -> List[Dict]:
        """List all jobs for a user, optionally filtered by phase."""
        if phase:
            response = self.user_job_table.query(
                IndexName='phase-index',
                KeyConditionExpression=Key('userid').eq(userid) & Key('jobphase').eq(phase)
            )
        else:
            response = self.user_job_table.query(
                KeyConditionExpression=Key('userid').eq(userid)
            )
        return response.get('Items', [])
    
    # Resume operations
    def get_resume(self, userid: str, resumename: str) -> Optional[Dict]:
        """Get resume by userid and resumename."""
        response = self.resume_table.get_item(
            Key={'userid': userid, 'resumename': resumename}
        )
        return response.get('Item')
    
    def create_resume(self, resume_data: Dict) -> Dict:
        """Create a new resume."""
        resume_data['lastupdate'] = datetime.utcnow().isoformat()
        self.resume_table.put_item(Item=resume_data)
        return resume_data
    
    def update_resume(self, userid: str, resumename: str, resumejson: Dict) -> Dict:
        """Update resume JSON."""
        response = self.resume_table.update_item(
            Key={'userid': userid, 'resumename': resumename},
            UpdateExpression='SET resumejson = :rj, lastupdate = :lu',
            ExpressionAttributeValues={
                ':rj': resumejson,
                ':lu': datetime.utcnow().isoformat()
            },
            ReturnValues='ALL_NEW'
        )
        return response.get('Attributes', {})
    
    def delete_resume(self, userid: str, resumename: str) -> None:
        """Delete a resume."""
        self.resume_table.delete_item(
            Key={'userid': userid, 'resumename': resumename}
        )
    
    def list_resumes(self, userid: str) -> List[Dict]:
        """List all resumes for a user."""
        response = self.resume_table.query(
            KeyConditionExpression=Key('userid').eq(userid)
        )
        return response.get('Items', [])
    
    # Resume URL operations
    def get_resume_url(self, resumeurl: str) -> Optional[Dict]:
        """Get resume URL record."""
        response = self.resume_url_table.get_item(Key={'resumeurl': resumeurl})
        return response.get('Item')
    
    def create_resume_url(self, resumeurl: str, userid: str, jobid: str) -> bool:
        """Create resume URL mapping. Returns False if URL exists."""
        try:
            self.resume_url_table.put_item(
                Item={
                    'resumeurl': resumeurl,
                    'userid': userid,
                    'jobid': jobid,
                    'createdAt': datetime.utcnow().isoformat()
                },
                ConditionExpression='attribute_not_exists(resumeurl)'
            )
            return True
        except self.dynamodb.meta.client.exceptions.ConditionalCheckFailedException:
            return False
    
    def delete_resume_url(self, resumeurl: str) -> None:
        """Delete a resume URL record."""
        self.resume_url_table.delete_item(Key={'resumeurl': resumeurl})
