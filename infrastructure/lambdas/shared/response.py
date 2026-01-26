"""
API Response utilities for Lambda functions.

Requirements: 14.4
"""
import json
from typing import Any, Optional


def api_response(
    status_code: int,
    body: Any,
    headers: Optional[dict] = None
) -> dict:
    """
    Create a standardized API Gateway response.
    
    Args:
        status_code: HTTP status code
        body: Response body (will be JSON serialized)
        headers: Optional additional headers
        
    Returns:
        API Gateway response dict
    """
    default_headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type,Authorization,X-Amz-Date,X-Api-Key,X-Amz-Security-Token",
        "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS",
    }
    
    if headers:
        default_headers.update(headers)
    
    return {
        "statusCode": status_code,
        "headers": default_headers,
        "body": json.dumps(body) if not isinstance(body, str) else body,
    }


def error_response(
    status_code: int,
    error: str,
    message: str,
    details: Optional[list] = None
) -> dict:
    """
    Create a standardized error response.
    
    Args:
        status_code: HTTP status code
        error: Error type (e.g., "ValidationError", "NotFound")
        message: Human-readable error message
        details: Optional list of detailed error information
        
    Returns:
        API Gateway error response dict
    """
    body = {
        "error": error,
        "message": message,
    }
    
    if details:
        body["details"] = details
    
    return api_response(status_code, body)


# Common error responses
def unauthorized(message: str = "Authentication required") -> dict:
    """Return 401 Unauthorized response."""
    return error_response(401, "Unauthorized", message)


def forbidden(message: str = "Access denied") -> dict:
    """Return 403 Forbidden response."""
    return error_response(403, "Forbidden", message)


def not_found(message: str = "Resource not found") -> dict:
    """Return 404 Not Found response."""
    return error_response(404, "NotFound", message)


def bad_request(message: str, details: Optional[list] = None) -> dict:
    """Return 400 Bad Request response."""
    return error_response(400, "ValidationError", message, details)


def conflict(message: str) -> dict:
    """Return 409 Conflict response."""
    return error_response(409, "Conflict", message)


def rate_limited(message: str = "Too many requests") -> dict:
    """Return 429 Rate Limited response."""
    return error_response(429, "RateLimited", message)


def internal_error(message: str = "An error occurred") -> dict:
    """Return 500 Internal Server Error response."""
    return error_response(500, "InternalError", message)
