from dotenv import load_dotenv
import os
import secrets
import webbrowser
from urllib.parse import urlparse, parse_qs, urlencode
import requests


def get_linkedin_access_token(client_id: str=None, client_secret: str=None) -> str:
    """
    Obtain an access token for LinkedIn API, using the provided client ID and secret,
    or falling back to environment variables if not provided.

    Args:
        client_id (str, optional): LinkedIn Client ID. Defaults to None.
        client_secret (str, optional): LinkedIn Client Secret. Defaults to None.

    Returns:
        str: Access token for LinkedIn API
    """
    load_dotenv('.env')
    # Allow an already-issued access token to be provided via env to avoid
    # any interactive flow.
    access_token_env = os.getenv('LINKEDIN_ACCESS_TOKEN')
    if access_token_env:
        return access_token_env

    client_id = client_id or os.getenv('LINKEDIN_CLIENT_ID')
    client_secret = client_secret or os.getenv('LINKEDIN_CLIENT_SECRET')
    redirect_uri = os.getenv('LINKEDIN_REDIRECT_URI', 'http://localhost:8000/')

    if not client_id or not client_secret:
        raise RuntimeError("LinkedIn client ID and secret must be set in environment variables, or set LINKEDIN_ACCESS_TOKEN.")

    # If a refresh token is available in the environment, exchange it for
    # a fresh access token so we can operate without a browser.
    refresh_token = os.getenv('LINKEDIN_REFRESH_TOKEN')
    token_endpoint = 'https://www.linkedin.com/oauth/v2/accessToken'
    if refresh_token:
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': client_id,
            'client_secret': client_secret,
        }
        resp = requests.post(token_endpoint, data=data, headers={'Accept': 'application/json'})
        if resp.status_code == 200:
            j = resp.json()
            access_token = j.get('access_token')
            if access_token:
                return access_token
        # fallthrough to interactive flow if refresh failed

    # As a last resort, fall back to interactive authorization code flow.
    # Note: this will open the browser which the user wanted to avoid,
    # but it remains as a fallback if no env tokens are available.
    state = secrets.token_urlsafe(16)
    auth_base = 'https://www.linkedin.com/oauth/v2/authorization'
    scope = os.getenv('LINKEDIN_SCOPE', 'r_liteprofile r_emailaddress')
    params = {
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'state': state,
        'scope': scope,
    }
    auth_url = f"{auth_base}?{urlencode(params)}"

    print('\nOpen this URL in your browser to authorize the application:')
    print(auth_url)
    try:
        webbrowser.open(auth_url)
    except Exception:
        pass

    redirected = input('\nAfter authorizing, paste the full redirect URL here (or paste "code=..." portion): ').strip()
    code = None
    if 'code=' in redirected:
        try:
            parsed = urlparse(redirected)
            qs = parse_qs(parsed.query)
            code = qs.get('code', [None])[0]
        except Exception:
            parts = redirected.split('code=')
            if len(parts) > 1:
                code = parts[1].split('&')[0]
    else:
        code = redirected

    if not code:
        raise RuntimeError('Authorization code not provided; cannot obtain access token.')

    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret,
    }

    resp = requests.post(token_endpoint, data=data, headers={'Accept': 'application/json'})
    if resp.status_code != 200:
        raise RuntimeError(f'Failed to obtain access token: {resp.status_code} {resp.text}')

    j = resp.json()
    access_token = j.get('access_token')
    if not access_token:
        raise RuntimeError(f'No access token in response: {j}')

    return access_token


def open_linkedin_page(url: str, access_token: str) -> dict:
    """
    Open a LinkedIn webpage using the provided access token, so that the 
    user is authenticated and the page is fully available.  

    Args:
        url (str): The URL of the LinkedIn page to open.
        access_token (str): The access token for LinkedIn API.

    Returns the HTML page content as a string.
    """
    load_dotenv('.env')
    if not access_token:
        raise RuntimeError('access_token is required')

    headers = {
        'Authorization': f'Bearer {access_token}',
        'User-Agent': 'resumai/1.0',
        'Accept': '*/*',
    }

    # Use GET to retrieve the page. LinkedIn may block programmatic browsing,
    # but for API endpoints the Bearer token will return data. For HTML pages,
    # LinkedIn typically requires a browser session; still attempt a fetch.
    resp = requests.get(url, headers=headers)

    result = {
        'status_code': resp.status_code,
        'headers': dict(resp.headers),
        'content': resp.text,
    }

    return result


