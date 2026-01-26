"""
Property-based tests for API responses.

Tests:
- Property 39: API Status Code Accuracy

Feature: skillsnap-mvp
Validates: Requirements 14.4, 14.5
"""
import pytest
from hypothesis import given, strategies as st, settings
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lambdas'))

from shared.response import (
    api_response, error_response, unauthorized, forbidden,
    not_found, bad_request, conflict, rate_limited, internal_error
)


class TestAPIStatusCodeAccuracy:
    """Tests for API status code accuracy."""

    @given(data=st.dictionaries(st.text(min_size=1, max_size=20), st.text(min_size=0, max_size=100), min_size=0, max_size=5))
    @settings(max_examples=100)
    def test_property_39_success_200(self, data: dict):
        """
        Property 39: API Status Code Accuracy
        
        For any successful API response, the HTTP status code SHALL be 200.
        
        Feature: skillsnap-mvp, Property 39: API Status Code Accuracy
        """
        response = api_response(200, data)
        
        assert response['statusCode'] == 200
        assert 'body' in response
        body = json.loads(response['body'])
        assert body == data

    @given(data=st.dictionaries(st.text(min_size=1, max_size=20), st.text(min_size=0, max_size=100), min_size=0, max_size=5))
    @settings(max_examples=100)
    def test_property_39_created_201(self, data: dict):
        """
        Property 39: API Status Code Accuracy
        
        For any resource creation response, the HTTP status code SHALL be 201.
        
        Feature: skillsnap-mvp, Property 39: API Status Code Accuracy
        """
        response = api_response(201, data)
        
        assert response['statusCode'] == 201
        body = json.loads(response['body'])
        assert body == data

    @given(message=st.text(min_size=1, max_size=100))
    @settings(max_examples=100)
    def test_property_39_bad_request_400(self, message: str):
        """
        Property 39: API Status Code Accuracy
        
        For any validation error, the HTTP status code SHALL be 400.
        
        Feature: skillsnap-mvp, Property 39: API Status Code Accuracy
        """
        response = bad_request(message)
        
        assert response['statusCode'] == 400
        body = json.loads(response['body'])
        assert body['error'] == 'ValidationError'
        assert body['message'] == message

    @given(message=st.text(min_size=1, max_size=100))
    @settings(max_examples=100)
    def test_property_39_unauthorized_401(self, message: str):
        """
        Property 39: API Status Code Accuracy
        
        For any unauthorized request, the HTTP status code SHALL be 401.
        
        Feature: skillsnap-mvp, Property 39: API Status Code Accuracy
        """
        response = unauthorized(message)
        
        assert response['statusCode'] == 401
        body = json.loads(response['body'])
        assert body['error'] == 'Unauthorized'
        assert body['message'] == message

    @given(message=st.text(min_size=1, max_size=100))
    @settings(max_examples=100)
    def test_property_39_forbidden_403(self, message: str):
        """
        Property 39: API Status Code Accuracy
        
        For any forbidden request, the HTTP status code SHALL be 403.
        
        Feature: skillsnap-mvp, Property 39: API Status Code Accuracy
        """
        response = forbidden(message)
        
        assert response['statusCode'] == 403
        body = json.loads(response['body'])
        assert body['error'] == 'Forbidden'
        assert body['message'] == message

    @given(message=st.text(min_size=1, max_size=100))
    @settings(max_examples=100)
    def test_property_39_not_found_404(self, message: str):
        """
        Property 39: API Status Code Accuracy
        
        For any resource not found, the HTTP status code SHALL be 404.
        
        Feature: skillsnap-mvp, Property 39: API Status Code Accuracy
        """
        response = not_found(message)
        
        assert response['statusCode'] == 404
        body = json.loads(response['body'])
        assert body['error'] == 'NotFound'
        assert body['message'] == message

    @given(message=st.text(min_size=1, max_size=100))
    @settings(max_examples=100)
    def test_property_39_conflict_409(self, message: str):
        """
        Property 39: API Status Code Accuracy
        
        For any conflict (e.g., duplicate resource), the HTTP status code SHALL be 409.
        
        Feature: skillsnap-mvp, Property 39: API Status Code Accuracy
        """
        response = conflict(message)
        
        assert response['statusCode'] == 409
        body = json.loads(response['body'])
        assert body['error'] == 'Conflict'
        assert body['message'] == message

    @given(message=st.text(min_size=1, max_size=100))
    @settings(max_examples=100)
    def test_property_39_rate_limited_429(self, message: str):
        """
        Property 39: API Status Code Accuracy
        
        For any rate limited request, the HTTP status code SHALL be 429.
        
        Feature: skillsnap-mvp, Property 39: API Status Code Accuracy
        """
        response = rate_limited(message)
        
        assert response['statusCode'] == 429
        body = json.loads(response['body'])
        assert body['error'] == 'RateLimited'
        assert body['message'] == message

    @given(message=st.text(min_size=1, max_size=100))
    @settings(max_examples=100)
    def test_property_39_internal_error_500(self, message: str):
        """
        Property 39: API Status Code Accuracy
        
        For any server error, the HTTP status code SHALL be 500.
        
        Feature: skillsnap-mvp, Property 39: API Status Code Accuracy
        """
        response = internal_error(message)
        
        assert response['statusCode'] == 500
        body = json.loads(response['body'])
        assert body['error'] == 'InternalError'
        assert body['message'] == message


class TestAPIResponseStructure:
    """Tests for API response structure."""

    @given(
        status_code=st.sampled_from([200, 201, 400, 401, 403, 404, 409, 429, 500]),
        data=st.dictionaries(st.text(min_size=1, max_size=20), st.text(min_size=0, max_size=100), min_size=0, max_size=5)
    )
    @settings(max_examples=100)
    def test_response_has_required_fields(self, status_code: int, data: dict):
        """
        Tests that all API responses have required fields.
        
        Feature: skillsnap-mvp, Property 39: API Status Code Accuracy
        """
        response = api_response(status_code, data)
        
        # Required fields
        assert 'statusCode' in response
        assert 'headers' in response
        assert 'body' in response
        
        # Headers should include CORS
        assert 'Access-Control-Allow-Origin' in response['headers']
        assert 'Content-Type' in response['headers']

    @given(
        error_type=st.sampled_from(['ValidationError', 'NotFound', 'Unauthorized', 'Conflict']),
        message=st.text(min_size=1, max_size=100),
        details=st.lists(st.text(min_size=1, max_size=50), min_size=0, max_size=5)
    )
    @settings(max_examples=100)
    def test_error_response_structure(self, error_type: str, message: str, details: list):
        """
        Tests that error responses have correct structure.
        
        Feature: skillsnap-mvp, Property 39: API Status Code Accuracy
        """
        response = error_response(400, error_type, message, details if details else None)
        
        body = json.loads(response['body'])
        
        assert 'error' in body
        assert 'message' in body
        assert body['error'] == error_type
        assert body['message'] == message
        
        if details:
            assert 'details' in body
            assert body['details'] == details


class TestAPIStatusCodeMapping:
    """Tests for correct status code to error type mapping."""

    def test_status_code_error_mapping(self):
        """
        Tests that status codes map to correct error types.
        
        Feature: skillsnap-mvp, Property 39: API Status Code Accuracy
        """
        mappings = [
            (bad_request("test"), 400, "ValidationError"),
            (unauthorized("test"), 401, "Unauthorized"),
            (forbidden("test"), 403, "Forbidden"),
            (not_found("test"), 404, "NotFound"),
            (conflict("test"), 409, "Conflict"),
            (rate_limited("test"), 429, "RateLimited"),
            (internal_error("test"), 500, "InternalError"),
        ]
        
        for response, expected_code, expected_error in mappings:
            assert response['statusCode'] == expected_code
            body = json.loads(response['body'])
            assert body['error'] == expected_error
