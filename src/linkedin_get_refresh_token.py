from dotenv import load_dotenv
import os
import secrets
import webbrowser
from urllib.parse import urlparse, parse_qs, urlencode
import requests


def _write_env_updates(updates: dict, env_path: str = '.env'):
    # Read existing .env (if any), update specified keys, and write back
    existing = {}
    lines = []
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()
        for ln in lines:
            if '=' in ln and not ln.strip().startswith('#'):
                k, v = ln.split('=', 1)
                existing[k.strip()] = v.strip()

    # Merge updates
    existing.update(updates)

    # Write back
    with open(env_path, 'w', encoding='utf-8') as f:
        for k, v in existing.items():
            f.write(f"{k}={v}\n")


def guide_and_persist(client_id: str = None, client_secret: str = None):
    """
    Guide a one-time interactive OAuth flow to obtain an access token and (if provided)
    a refresh token. Persist results to `.env` as LINKEDIN_ACCESS_TOKEN and
    LINKEDIN_REFRESH_TOKEN where available.

    Note: This is intended to be run once interactively on a machine where you can
    open the authorization URL and complete LinkedIn consent. After tokens are
    persisted, scheduled server runs can use the refresh token to obtain new
    access tokens without further interaction.
    """
    load_dotenv('.env')
    client_id = client_id or os.getenv('LINKEDIN_CLIENT_ID')
    client_secret = client_secret or os.getenv('LINKEDIN_CLIENT_SECRET')
    redirect_uri = os.getenv('LINKEDIN_REDIRECT_URI', 'http://localhost:8000/')
    scope = os.getenv('LINKEDIN_SCOPE', 'r_liteprofile r_emailaddress')

    if not client_id or not client_secret:
        raise RuntimeError('Please set LINKEDIN_CLIENT_ID and LINKEDIN_CLIENT_SECRET in your environment or pass them in.')

    state = secrets.token_urlsafe(16)
    auth_base = 'https://www.linkedin.com/oauth/v2/authorization'
    params = {
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'state': state,
        'scope': scope,
    }
    auth_url = f"{auth_base}?{urlencode(params)}"

    print('\nOpen this URL in your browser and complete authorization:')
    print(auth_url)
    try:
        webbrowser.open(auth_url)
    except Exception:
        pass

    redirected = input('\nAfter authorizing, paste the full redirect URL here (must contain "code="): ').strip()
    if 'code=' not in redirected:
        raise RuntimeError('Redirected URL must contain code parameter.')

    parsed = urlparse(redirected)
    qs = parse_qs(parsed.query)
    code = qs.get('code', [None])[0]
    if not code:
        raise RuntimeError('No code found in provided URL.')

    token_endpoint = 'https://www.linkedin.com/oauth/v2/accessToken'
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret,
    }

    resp = requests.post(token_endpoint, data=data, headers={'Accept': 'application/json'})
    if resp.status_code != 200:
        raise RuntimeError(f'Failed to obtain tokens: {resp.status_code} {resp.text}')

    j = resp.json()
    access_token = j.get('access_token')
    refresh_token = j.get('refresh_token')
    expires_in = j.get('expires_in')

    updates = {}
    if access_token:
        updates['LINKEDIN_ACCESS_TOKEN'] = access_token
    if refresh_token:
        updates['LINKEDIN_REFRESH_TOKEN'] = refresh_token
    if expires_in:
        updates['LINKEDIN_ACCESS_EXPIRES_IN'] = str(expires_in)

    if not updates:
        raise RuntimeError(f'No tokens returned from LinkedIn: {j}')

    _write_env_updates(updates, env_path='.env')
    print('\nPersisted tokens to .env (LINKEDIN_ACCESS_TOKEN and/or LINKEDIN_REFRESH_TOKEN).')


if __name__ == '__main__':
    guide_and_persist()
