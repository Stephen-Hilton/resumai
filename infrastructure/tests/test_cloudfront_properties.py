"""
Property-based tests for CloudFront Function URL rewriting.

Tests:
- Property 28: CloudFront URL Rewriting
- Property 29: CloudFront Global Asset Passthrough
- Property 30: CloudFront Override CSS Rewriting

Feature: skillsnap-mvp
Validates: Requirements 11.2, 11.3, 11.4
"""
import pytest
from hypothesis import given, strategies as st, settings, assume
import re


def cloudfront_handler(host: str, uri: str) -> str:
    """
    Python implementation of the CloudFront Function for testing.
    This mirrors the JavaScript function in cloudfront_stack.py.
    """
    host = host.split(":")[0].lower()
    
    username = "www"
    parts = host.split(".")
    if len(parts) >= 3:
        username = parts[0]
    
    if uri == "":
        uri = "/"
    
    # Global assets: DO NOT rewrite
    if (uri.startswith("/assets/") or
        uri.startswith("/_global/") or
        uri == "/favicon.ico" or
        uri == "/robots.txt" or
        uri == "/sitemap.xml"):
        return uri
    
    # User root -> user homepage
    if uri == "/":
        return f"/{username}/index.html"
    
    # Normalize trailing slash
    if len(uri) > 1 and uri.endswith("/"):
        uri = uri[:-1]
    
    segs = [s for s in uri.split("/") if s]
    
    # "/company/job" -> "/username/company/job/index.html"
    if len(segs) == 2:
        return f"/{username}/{segs[0]}/{segs[1]}/index.html"
    
    # Anything deeper: prefix username
    return f"/{username}{uri}"


# Strategy for valid usernames (subdomains)
username_strategy = st.from_regex(r'^[a-z][a-z0-9]{2,20}$', fullmatch=True)

# Strategy for company names (URL-safe)
company_strategy = st.from_regex(r'^[a-z][a-z0-9\-]{1,30}$', fullmatch=True)

# Strategy for job title safe strings
jobtitle_strategy = st.from_regex(r'^[a-z][a-z0-9\-]{1,50}$', fullmatch=True)

# Strategy for global asset paths
asset_path_strategy = st.one_of(
    st.just("/assets/resume-base.css"),
    st.just("/assets/cover-base.css"),
    st.just("/_global/fonts/roboto.woff2"),
    st.just("/favicon.ico"),
    st.just("/robots.txt"),
    st.just("/sitemap.xml"),
    st.from_regex(r'^/assets/[a-z0-9\-/]+\.(css|js|png|jpg|svg|woff2?)$', fullmatch=True),
    st.from_regex(r'^/_global/[a-z0-9\-/]+\.(css|js|png|jpg|svg|woff2?)$', fullmatch=True),
)


class TestCloudFrontURLRewriting:
    """Tests for CloudFront URL rewriting functionality."""

    @given(
        username=username_strategy,
        company=company_strategy,
        jobtitle=jobtitle_strategy
    )
    @settings(max_examples=100)
    def test_property_28_url_rewriting(self, username: str, company: str, jobtitle: str):
        """
        Property 28: CloudFront URL Rewriting
        
        For any request to {username}.skillsnap.me/{company}/{jobtitlesafe},
        the CloudFront function SHALL rewrite the path to
        /{username}/{company}/{jobtitlesafe}/index.html in S3.
        
        Feature: skillsnap-mvp, Property 28: CloudFront URL Rewriting
        """
        host = f"{username}.skillsnap.me"
        uri = f"/{company}/{jobtitle}"
        
        result = cloudfront_handler(host, uri)
        expected = f"/{username}/{company}/{jobtitle}/index.html"
        
        assert result == expected, f"Expected {expected}, got {result}"

    @given(username=username_strategy)
    @settings(max_examples=100)
    def test_property_28_root_url_rewriting(self, username: str):
        """
        Property 28: CloudFront URL Rewriting (root path)
        
        For any request to {username}.skillsnap.me/,
        the CloudFront function SHALL rewrite to /{username}/index.html.
        
        Feature: skillsnap-mvp, Property 28: CloudFront URL Rewriting
        """
        host = f"{username}.skillsnap.me"
        uri = "/"
        
        result = cloudfront_handler(host, uri)
        expected = f"/{username}/index.html"
        
        assert result == expected, f"Expected {expected}, got {result}"

    @given(
        username=username_strategy,
        company=company_strategy,
        jobtitle=jobtitle_strategy
    )
    @settings(max_examples=100)
    def test_property_28_trailing_slash_normalization(self, username: str, company: str, jobtitle: str):
        """
        Property 28: CloudFront URL Rewriting (trailing slash)
        
        URLs with trailing slashes should be normalized.
        
        Feature: skillsnap-mvp, Property 28: CloudFront URL Rewriting
        """
        host = f"{username}.skillsnap.me"
        uri_with_slash = f"/{company}/{jobtitle}/"
        uri_without_slash = f"/{company}/{jobtitle}"
        
        result_with = cloudfront_handler(host, uri_with_slash)
        result_without = cloudfront_handler(host, uri_without_slash)
        
        # Both should produce the same result
        assert result_with == result_without, \
            f"Trailing slash should be normalized: {result_with} vs {result_without}"


class TestCloudFrontGlobalAssets:
    """Tests for CloudFront global asset passthrough."""

    @given(asset_path=asset_path_strategy, username=username_strategy)
    @settings(max_examples=100)
    def test_property_29_global_asset_passthrough(self, asset_path: str, username: str):
        """
        Property 29: CloudFront Global Asset Passthrough
        
        For any request path starting with /assets/, /_global/,
        or matching /favicon.ico, /robots.txt, /sitemap.xml,
        the CloudFront function SHALL NOT modify the path.
        
        Feature: skillsnap-mvp, Property 29: CloudFront Global Asset Passthrough
        """
        host = f"{username}.skillsnap.me"
        
        result = cloudfront_handler(host, asset_path)
        
        # Asset paths should NOT be modified
        assert result == asset_path, \
            f"Global asset path should not be modified: expected {asset_path}, got {result}"

    def test_property_29_specific_assets(self):
        """
        Property 29: CloudFront Global Asset Passthrough (specific files)
        
        Tests specific global asset paths that must pass through unchanged.
        
        Feature: skillsnap-mvp, Property 29: CloudFront Global Asset Passthrough
        """
        test_cases = [
            "/assets/resume-base.css",
            "/assets/cover-base.css",
            "/assets/js/main.js",
            "/assets/images/logo.png",
            "/_global/fonts/roboto.woff2",
            "/favicon.ico",
            "/robots.txt",
            "/sitemap.xml",
        ]
        
        for asset_path in test_cases:
            result = cloudfront_handler("john.skillsnap.me", asset_path)
            assert result == asset_path, \
                f"Asset {asset_path} should pass through unchanged, got {result}"


class TestCloudFrontOverrideCSS:
    """Tests for CloudFront override CSS rewriting."""

    @given(
        username=username_strategy,
        company=company_strategy,
        jobtitle=jobtitle_strategy
    )
    @settings(max_examples=100)
    def test_property_30_override_css_rewriting(self, username: str, company: str, jobtitle: str):
        """
        Property 30: CloudFront Override CSS Rewriting
        
        For any request to {username}.skillsnap.me/{company}/{jobtitlesafe}/resume-override.css,
        the CloudFront function SHALL rewrite to
        /{username}/{company}/{jobtitlesafe}/resume-override.css in S3.
        
        Feature: skillsnap-mvp, Property 30: CloudFront Override CSS Rewriting
        """
        host = f"{username}.skillsnap.me"
        uri = f"/{company}/{jobtitle}/resume-override.css"
        
        result = cloudfront_handler(host, uri)
        expected = f"/{username}/{company}/{jobtitle}/resume-override.css"
        
        assert result == expected, f"Expected {expected}, got {result}"

    @given(
        username=username_strategy,
        company=company_strategy,
        jobtitle=jobtitle_strategy,
        filename=st.from_regex(r'^[a-z0-9\-]+\.(css|html|pdf)$', fullmatch=True)
    )
    @settings(max_examples=100)
    def test_property_30_deep_path_rewriting(self, username: str, company: str, jobtitle: str, filename: str):
        """
        Property 30: CloudFront Override CSS Rewriting (deep paths)
        
        For any deep path request, the CloudFront function SHALL prefix with username.
        
        Feature: skillsnap-mvp, Property 30: CloudFront Override CSS Rewriting
        """
        host = f"{username}.skillsnap.me"
        uri = f"/{company}/{jobtitle}/{filename}"
        
        result = cloudfront_handler(host, uri)
        expected = f"/{username}/{company}/{jobtitle}/{filename}"
        
        assert result == expected, f"Expected {expected}, got {result}"


class TestCloudFrontEdgeCases:
    """Tests for CloudFront edge cases."""

    def test_www_subdomain_handling(self):
        """
        Tests that www subdomain is handled correctly.
        """
        # www.skillsnap.me should use "www" as username
        result = cloudfront_handler("www.skillsnap.me", "/")
        assert result == "/www/index.html"
        
        result = cloudfront_handler("www.skillsnap.me", "/acme/engineer")
        assert result == "/www/acme/engineer/index.html"

    def test_no_subdomain_handling(self):
        """
        Tests that requests without subdomain default to "www".
        """
        # skillsnap.me (no subdomain) should default to "www"
        result = cloudfront_handler("skillsnap.me", "/")
        assert result == "/www/index.html"

    @given(username=username_strategy)
    @settings(max_examples=100)
    def test_empty_uri_handling(self, username: str):
        """
        Tests that empty URI is handled as root.
        """
        host = f"{username}.skillsnap.me"
        
        result = cloudfront_handler(host, "")
        expected = f"/{username}/index.html"
        
        assert result == expected

    @given(username=username_strategy, single_segment=company_strategy)
    @settings(max_examples=100)
    def test_single_segment_path(self, username: str, single_segment: str):
        """
        Tests single segment paths (not company/job format).
        """
        host = f"{username}.skillsnap.me"
        uri = f"/{single_segment}"
        
        result = cloudfront_handler(host, uri)
        expected = f"/{username}/{single_segment}"
        
        assert result == expected

    def test_port_stripping(self):
        """
        Tests that port numbers are stripped from host.
        """
        result = cloudfront_handler("john.skillsnap.me:443", "/acme/engineer")
        assert result == "/john/acme/engineer/index.html"
        
        result = cloudfront_handler("john.skillsnap.me:8080", "/")
        assert result == "/john/index.html"

    def test_case_insensitivity(self):
        """
        Tests that host is case-insensitive.
        """
        result1 = cloudfront_handler("JOHN.skillsnap.me", "/acme/engineer")
        result2 = cloudfront_handler("john.skillsnap.me", "/acme/engineer")
        result3 = cloudfront_handler("John.Skillsnap.Me", "/acme/engineer")
        
        assert result1 == result2 == result3 == "/john/acme/engineer/index.html"
