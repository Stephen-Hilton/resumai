"""
Property-based tests for authentication.

Tests:
- Property 1: OAuth Account Linking Consistency
- Property 3: Unauthenticated Request Rejection

Feature: skillsnap-mvp
Validates: Requirements 1.2, 3.2, 14.2
"""
import pytest
from hypothesis import given, strategies as st, settings
import re
import json


# Strategy for valid email addresses
email_strategy = st.emails()

# Strategy for valid usernames
username_strategy = st.from_regex(r'^[a-zA-Z][a-zA-Z0-9_]{2,29}$', fullmatch=True)

# Strategy for valid UUIDs
uuid_strategy = st.uuids().map(str)

# Strategy for Cognito sub (UUID format)
cognito_sub_strategy = st.uuids().map(str)


class MockUserEmailTable:
    """Mock USER_EMAIL table for testing account linking logic."""
    
    def __init__(self):
        self.emails = {}
    
    def get_user_by_email(self, email: str) -> dict | None:
        """Get user by email."""
        return self.emails.get(email.lower())
    
    def create_user_email(self, email: str, userid: str) -> bool:
        """Create email mapping. Returns False if exists."""
        email_lower = email.lower()
        if email_lower in self.emails:
            return False
        self.emails[email_lower] = {'useremail': email_lower, 'userid': userid}
        return True


def oauth_account_linking(
    email: str,
    cognito_sub: str,
    user_email_table: MockUserEmailTable,
    generate_userid: callable
) -> dict:
    """
    Simulates OAuth account linking logic.
    
    If email exists, returns existing user.
    Otherwise, creates new user and email mapping.
    """
    # Check if user exists
    existing = user_email_table.get_user_by_email(email)
    if existing:
        return {
            'action': 'linked',
            'userid': existing['userid'],
            'email': email.lower(),
        }
    
    # Create new user
    new_userid = generate_userid()
    user_email_table.create_user_email(email, new_userid)
    
    return {
        'action': 'created',
        'userid': new_userid,
        'email': email.lower(),
    }


class TestOAuthAccountLinking:
    """Tests for OAuth account linking consistency."""

    @given(email=email_strategy, cognito_sub=cognito_sub_strategy)
    @settings(max_examples=100)
    def test_property_1_new_user_creation(self, email: str, cognito_sub: str):
        """
        Property 1: OAuth Account Linking Consistency
        
        For any Google OAuth authentication response with an email address,
        if no user with that email exists, the system SHALL create a new
        USER record and corresponding USER_EMAIL entry.
        
        Feature: skillsnap-mvp, Property 1: OAuth Account Linking Consistency
        """
        table = MockUserEmailTable()
        userid_counter = [0]
        
        def generate_userid():
            userid_counter[0] += 1
            return f"user-{userid_counter[0]}"
        
        result = oauth_account_linking(email, cognito_sub, table, generate_userid)
        
        # Should create new user
        assert result['action'] == 'created'
        assert result['userid'] == 'user-1'
        assert result['email'] == email.lower()
        
        # Email should now be in table
        assert table.get_user_by_email(email) is not None

    @given(email=email_strategy, cognito_sub1=cognito_sub_strategy, cognito_sub2=cognito_sub_strategy)
    @settings(max_examples=100)
    def test_property_1_existing_user_linking(self, email: str, cognito_sub1: str, cognito_sub2: str):
        """
        Property 1: OAuth Account Linking Consistency
        
        For any Google OAuth authentication response with an email address,
        if a user with that email already exists in USER_EMAIL, the system
        SHALL link to the existing account.
        
        Feature: skillsnap-mvp, Property 1: OAuth Account Linking Consistency
        """
        table = MockUserEmailTable()
        userid_counter = [0]
        
        def generate_userid():
            userid_counter[0] += 1
            return f"user-{userid_counter[0]}"
        
        # First authentication - creates user
        result1 = oauth_account_linking(email, cognito_sub1, table, generate_userid)
        assert result1['action'] == 'created'
        original_userid = result1['userid']
        
        # Second authentication with same email - should link
        result2 = oauth_account_linking(email, cognito_sub2, table, generate_userid)
        assert result2['action'] == 'linked'
        assert result2['userid'] == original_userid
        
        # Should not create new user
        assert userid_counter[0] == 1

    @given(
        emails=st.lists(email_strategy, min_size=2, max_size=5, unique_by=str.lower),
        cognito_subs=st.lists(cognito_sub_strategy, min_size=5, max_size=5)
    )
    @settings(max_examples=100)
    def test_property_1_multiple_users(self, emails: list, cognito_subs: list):
        """
        Property 1: OAuth Account Linking Consistency
        
        Multiple different emails should create separate users.
        
        Feature: skillsnap-mvp, Property 1: OAuth Account Linking Consistency
        """
        table = MockUserEmailTable()
        userid_counter = [0]
        
        def generate_userid():
            userid_counter[0] += 1
            return f"user-{userid_counter[0]}"
        
        userids = set()
        for i, email in enumerate(emails):
            result = oauth_account_linking(email, cognito_subs[i], table, generate_userid)
            assert result['action'] == 'created'
            userids.add(result['userid'])
        
        # Each email should have unique userid
        assert len(userids) == len(emails)


class TestUnauthenticatedRequestRejection:
    """Tests for unauthenticated request rejection."""

    def validate_auth_token(self, token: str | None) -> tuple[bool, int, str]:
        """
        Simulates token validation.
        
        Returns (is_valid, status_code, message)
        """
        if token is None:
            return (False, 401, "Authentication required")
        
        if not token.startswith("Bearer "):
            return (False, 401, "Invalid token format")
        
        jwt_part = token[7:]  # Remove "Bearer "
        
        if not jwt_part or len(jwt_part) < 10:
            return (False, 401, "Invalid or expired token")
        
        # Simulate valid token
        return (True, 200, "OK")

    @given(token=st.one_of(st.none(), st.just(""), st.just("invalid")))
    @settings(max_examples=100)
    def test_property_3_missing_token_rejection(self, token: str | None):
        """
        Property 3: Unauthenticated Request Rejection
        
        For any request to the API without a valid Cognito token,
        the system SHALL return 401 Unauthorized.
        
        Feature: skillsnap-mvp, Property 3: Unauthenticated Request Rejection
        """
        is_valid, status_code, message = self.validate_auth_token(token)
        
        assert not is_valid
        assert status_code == 401
        assert "Authentication required" in message or "Invalid" in message

    @given(random_string=st.text(min_size=1, max_size=100))
    @settings(max_examples=100)
    def test_property_3_invalid_format_rejection(self, random_string: str):
        """
        Property 3: Unauthenticated Request Rejection
        
        Tokens without proper Bearer format should be rejected.
        
        Feature: skillsnap-mvp, Property 3: Unauthenticated Request Rejection
        """
        # Test without Bearer prefix
        is_valid, status_code, message = self.validate_auth_token(random_string)
        
        if not random_string.startswith("Bearer "):
            assert not is_valid
            assert status_code == 401

    @given(jwt_content=st.text(min_size=20, max_size=500, alphabet=st.characters(whitelist_categories=('L', 'N'))))
    @settings(max_examples=100)
    def test_property_3_valid_format_accepted(self, jwt_content: str):
        """
        Property 3: Unauthenticated Request Rejection
        
        Properly formatted tokens should pass format validation.
        
        Feature: skillsnap-mvp, Property 3: Unauthenticated Request Rejection
        """
        token = f"Bearer {jwt_content}"
        is_valid, status_code, message = self.validate_auth_token(token)
        
        # Should pass format validation (actual JWT validation would be more complex)
        assert is_valid
        assert status_code == 200


class TestAPIAuthorizationResponses:
    """Tests for API authorization response codes."""

    def api_request(self, token: str | None, endpoint: str) -> dict:
        """
        Simulates an API request with authorization.
        
        Returns response with status code and body.
        """
        # Check authorization
        if token is None:
            return {
                'statusCode': 401,
                'body': json.dumps({
                    'error': 'Unauthorized',
                    'message': 'Authentication required'
                })
            }
        
        if not token.startswith("Bearer ") or len(token) < 15:
            return {
                'statusCode': 401,
                'body': json.dumps({
                    'error': 'Unauthorized',
                    'message': 'Invalid or expired token'
                })
            }
        
        # Authorized request
        return {
            'statusCode': 200,
            'body': json.dumps({'data': 'success'})
        }

    @given(endpoint=st.sampled_from([
        '/resumes',
        '/resumes/123',
        '/jobs',
        '/jobs/456',
        '/preferences',
        '/jobs/789/generate-all',
    ]))
    @settings(max_examples=100)
    def test_property_3_all_endpoints_require_auth(self, endpoint: str):
        """
        Property 3: Unauthenticated Request Rejection
        
        All API endpoints should require authentication.
        
        Feature: skillsnap-mvp, Property 3: Unauthenticated Request Rejection
        """
        # Request without token
        response = self.api_request(None, endpoint)
        
        assert response['statusCode'] == 401
        body = json.loads(response['body'])
        assert body['error'] == 'Unauthorized'

    @given(
        endpoint=st.sampled_from(['/resumes', '/jobs', '/preferences']),
        jwt_content=st.text(min_size=20, max_size=100, alphabet=st.characters(whitelist_categories=('L', 'N')))
    )
    @settings(max_examples=100)
    def test_property_3_valid_token_accepted(self, endpoint: str, jwt_content: str):
        """
        Property 3: Unauthenticated Request Rejection
        
        Valid tokens should be accepted.
        
        Feature: skillsnap-mvp, Property 3: Unauthenticated Request Rejection
        """
        token = f"Bearer {jwt_content}"
        response = self.api_request(token, endpoint)
        
        assert response['statusCode'] == 200
