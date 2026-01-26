"""
Job List Lambda Handler

Lists jobs for the authenticated user with optional phase filter.

Requirements: 3.6, 3.7, 3.8
"""
import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from shared.response import api_response, bad_request, internal_error
from shared.dynamodb import DynamoDBClient
from shared.validation import VALID_PHASES, ACTIVE_PHASES


def calculate_posting_age(jobposteddate: str) -> int:
    """Calculate days since job was posted."""
    try:
        posted = datetime.strptime(jobposteddate, '%Y-%m-%d')
        today = datetime.utcnow()
        delta = today - posted
        return delta.days
    except (ValueError, TypeError):
        return 0


def handler(event, context):
    """
    List jobs for the authenticated user.
    
    Query parameters:
    - phase: Filter by specific phase (optional)
    - filter: "active" for all active phases, "all" for all jobs (optional)
    """
    try:
        # Get user ID from Cognito authorizer
        claims = event.get('requestContext', {}).get('authorizer', {}).get('claims', {})
        userid = claims.get('custom:userid') or claims.get('sub')
        
        if not userid:
            return bad_request("User ID not found in token")
        
        # Get query parameters
        query_params = event.get('queryStringParameters', {}) or {}
        phase = query_params.get('phase')
        filter_type = query_params.get('filter', 'all')
        
        db = DynamoDBClient()
        
        # Get user jobs based on filter
        if phase:
            if phase not in VALID_PHASES:
                return bad_request(f"Invalid phase. Must be one of: {', '.join(VALID_PHASES)}")
            user_jobs = db.list_user_jobs(userid, phase)
        else:
            user_jobs = db.list_user_jobs(userid)
            
            # Apply filter
            if filter_type == 'active':
                user_jobs = [uj for uj in user_jobs if uj.get('jobphase') in ACTIVE_PHASES]
        
        # Enrich with job details and calculate posting age
        jobs = []
        for user_job in user_jobs:
            job = db.get_job(user_job['jobid'])
            if job:
                combined = {**job, **user_job}
                combined['postingAge'] = calculate_posting_age(job.get('jobposteddate', ''))
                jobs.append(combined)
        
        # Sort by creation date (newest first)
        jobs.sort(key=lambda x: x.get('createdAt', ''), reverse=True)
        
        # Calculate phase counts
        all_user_jobs = db.list_user_jobs(userid)
        phase_counts = {}
        for p in VALID_PHASES:
            phase_counts[p] = sum(1 for uj in all_user_jobs if uj.get('jobphase') == p)
        
        return api_response(200, {
            'jobs': jobs,
            'count': len(jobs),
            'phaseCounts': phase_counts,
            'totalCount': len(all_user_jobs)
        })
        
    except Exception as e:
        print(f"Error listing jobs: {e}")
        return internal_error("Failed to list jobs")
