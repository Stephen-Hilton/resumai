"""
Job Create Manual Lambda Handler

Creates a new job from manual entry.

Requirements: 5.3, 5.4, 5.5, 13.3
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

from shared.response import api_response, bad_request, internal_error
from shared.dynamodb import DynamoDBClient
from shared.validation import make_safe_url_segment, VALID_SUBCOMPONENTS


def get_default_generation_types(db: DynamoDBClient, userid: str) -> dict:
    """Get user's default generation types for all subcomponents."""
    prefs = db.get_user_prefs(userid)
    # Default generation types (contact defaults to manual, others to ai)
    defaults = {
        'contact': 'manual',
        'summary': 'ai',
        'skills': 'ai',
        'highlights': 'ai',
        'experience': 'ai',
        'education': 'ai',
        'awards': 'ai',
        'keynotes': 'ai',
        'coverletter': 'ai',
    }
    result = {}
    for component in VALID_SUBCOMPONENTS:
        pref_name = f"default_gen_{component}"
        result[component] = prefs.get(pref_name, defaults.get(component, 'ai'))
    return result


def handler(event, context):
    """
    Create a job from manual entry.
    
    Request body:
    {
        "jobcompany": "string",
        "jobtitle": "string",
        "jobdesc": "string",
        "joblocation": "string" (optional),
        "jobsalary": "string" (optional),
        "jobposteddate": "string" (optional, defaults to today),
        "joburl": "string" (optional),
        "jobtags": ["string"] (optional),
        "resumeid": "string" (resume name to use)
    }
    """
    try:
        # Get user ID from Cognito authorizer
        claims = event.get('requestContext', {}).get('authorizer', {}).get('claims', {})
        userid = claims.get('custom:userid') or claims.get('sub')
        
        if not userid:
            return bad_request("User ID not found in token")
        
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        
        # Required fields
        jobcompany = body.get('jobcompany')
        jobtitle = body.get('jobtitle')
        jobdesc = body.get('jobdesc')
        resumeid = body.get('resumeid')
        
        if not jobcompany:
            return bad_request("jobcompany is required")
        if not jobtitle:
            return bad_request("jobtitle is required")
        if not jobdesc:
            return bad_request("jobdesc is required")
        if not resumeid:
            return bad_request("resumeid is required")
        
        db = DynamoDBClient()
        
        # Verify resume exists
        resume = db.get_resume(userid, resumeid)
        if not resume:
            return bad_request(f"Resume '{resumeid}' not found")
        
        # Generate job ID
        jobid = str(uuid7.uuid7())
        
        # Create safe URL segment for job title
        jobtitlesafe = make_safe_url_segment(jobtitle)
        
        # Create JOB record
        job_data = {
            'jobid': jobid,
            'postedts': datetime.utcnow().isoformat(),
            'jobcompany': jobcompany,
            'jobtitle': jobtitle,
            'jobtitlesafe': jobtitlesafe,
            'jobdesc': jobdesc,
            'joblocation': body.get('joblocation', ''),
            'jobsalary': body.get('jobsalary', ''),
            'jobposteddate': body.get('jobposteddate', datetime.utcnow().strftime('%Y-%m-%d')),
            'joburl': body.get('joburl', ''),
            'jobcompanylogo': body.get('jobcompanylogo', ''),
            'jobtags': body.get('jobtags', []),
        }
        
        created_job = db.create_job(job_data)
        
        # Get user's default generation types
        gen_types = get_default_generation_types(db, userid)
        
        # Determine initial phase based on data completeness
        # For manual entry, all required data is present, so start as "Queued"
        initial_phase = 'Queued' if jobcompany and jobtitle and jobdesc else 'Search'
        
        # Create USER_JOB record
        user_job_data = {
            'userid': userid,
            'jobid': jobid,
            'resumeid': resumeid,
            'jobphase': initial_phase,
            
            # Subcomponent data (empty initially)
            'datacontact': '',
            'datasummary': '',
            'dataskills': '',
            'datahighlights': '',
            'dataexperience': '',
            'dataeducation': '',
            'dataawards': '',
            'datakeynotes': '',
            'datacoverletter': '',
            
            # Generation states (all start as "ready")
            'statecontact': 'ready',
            'statesummary': 'ready',
            'stateskills': 'ready',
            'statehighlights': 'ready',
            'stateexperience': 'ready',
            'stateeducation': 'ready',
            'stateawards': 'ready',
            'statekeynotes': 'ready',
            'statecoverletter': 'ready',
            
            # Generation types (from user preferences)
            'typecontact': gen_types['contact'],
            'typesummary': gen_types['summary'],
            'typeskills': gen_types['skills'],
            'typehighlights': gen_types['highlights'],
            'typeexperience': gen_types['experience'],
            'typeeducation': gen_types['education'],
            'typeawards': gen_types['awards'],
            'typekeynotes': gen_types['keynotes'],
            'typecoverletter': gen_types['coverletter'],
            
            # Final file locations (empty initially)
            's3locresumehtml': '',
            's3locresumepdf': '',
            's3loccoverletterhtml': '',
            's3loccoverletterpdf': '',
        }
        
        created_user_job = db.create_user_job(user_job_data)
        
        return api_response(201, {
            'message': 'Job created successfully',
            'job': created_job,
            'userJob': created_user_job
        })
        
    except json.JSONDecodeError:
        return bad_request("Invalid JSON in request body")
    except Exception as e:
        print(f"Error creating job: {e}")
        return internal_error("Failed to create job")
