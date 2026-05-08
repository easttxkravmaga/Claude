"""LinkedIn OAuth — Authorization Code flow with offline_access scope.

Fixes the Manus build's bug where LinkedIn tokens died at 60 days because
no refresh_token was issued. Requesting offline_access produces a refresh
token good for 365 days, refreshable indefinitely.
"""

import os
import secrets
from datetime import datetime, timedelta
from urllib.parse import urlencode

import requests
from sqlalchemy import select

from db import SessionLocal
from models import OAuthCredential, Provider, RefreshStatus
from security import decrypt, encrypt


_AUTHORIZE_URL = "https://www.linkedin.com/oauth/v2/authorization"
_TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
_USERINFO_URL = "https://api.linkedin.com/v2/userinfo"

_SCOPES = "openid profile email w_member_social r_basicprofile offline_access"

_TIMEOUT = 30


class LinkedInError(Exception):
    pass


def _redirect_uri() -> str:
    uri = os.environ.get("LINKEDIN_REDIRECT_URI")
    if not uri:
        raise LinkedInError(
            "LINKEDIN_REDIRECT_URI env var is not set. "
            "Set it after Cloud Run deploy and update LinkedIn Developer Portal."
        )
    return uri


def build_authorize_url(client_id: str, state: str) -> str:
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": _redirect_uri(),
        "scope": _SCOPES,
        "state": state,
    }
    return f"{_AUTHORIZE_URL}?{urlencode(params)}"


def new_state() -> str:
    return secrets.token_urlsafe(32)


def exchange_code(code: str, client_id: str, client_secret: str) -> dict:
    resp = requests.post(
        _TOKEN_URL,
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": _redirect_uri(),
            "client_id": client_id,
            "client_secret": client_secret,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=_TIMEOUT,
    )
    if resp.status_code != 200:
        raise LinkedInError(f"Token exchange failed: {resp.status_code} {resp.text}")
    payload = resp.json()
    if "refresh_token" not in payload:
        raise LinkedInError(
            "Token exchange returned no refresh_token. "
            "The LinkedIn app is missing the offline_access scope. "
            "Add it under OAuth 2.0 settings and re-authorize."
        )
    return payload


def fetch_person_urn(access_token: str) -> str:
    resp = requests.get(
        _USERINFO_URL,
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=_TIMEOUT,
    )
    if resp.status_code != 200:
        raise LinkedInError(f"userinfo fetch failed: {resp.status_code} {resp.text}")
    data = resp.json()
    sub = data.get("sub")
    if not sub:
        raise LinkedInError("userinfo response missing 'sub' field")
    return f"urn:li:person:{sub}"


def store_credential(
    client_id: str,
    client_secret: str,
    token_payload: dict,
    person_urn: str,
    label: str = "ETKM LinkedIn",
) -> OAuthCredential:
    expires_in = int(token_payload.get("expires_in", 5184000))
    expires_at = datetime.utcnow() + timedelta(seconds=expires_in)

    with SessionLocal() as session:
        existing = session.scalar(
            select(OAuthCredential).where(
                OAuthCredential.provider == Provider.linkedin,
                OAuthCredential.label == label,
            )
        )
        if existing is None:
            cred = OAuthCredential(
                provider=Provider.linkedin,
                label=label,
                client_id=client_id,
                client_secret_enc=encrypt(client_secret),
                access_token_enc=encrypt(token_payload["access_token"]),
                refresh_token_enc=encrypt(token_payload["refresh_token"]),
                expires_at=expires_at,
                person_urn=person_urn,
                last_refresh_at=datetime.utcnow(),
                last_refresh_status=RefreshStatus.success,
            )
            session.add(cred)
        else:
            existing.client_id = client_id
            existing.client_secret_enc = encrypt(client_secret)
            existing.access_token_enc = encrypt(token_payload["access_token"])
            existing.refresh_token_enc = encrypt(token_payload["refresh_token"])
            existing.expires_at = expires_at
            existing.person_urn = person_urn
            existing.last_refresh_at = datetime.utcnow()
            existing.last_refresh_status = RefreshStatus.success
            existing.last_refresh_error = None
            cred = existing
        session.commit()
        session.refresh(cred)
        return cred


def refresh(cred: OAuthCredential) -> None:
    if not cred.refresh_token_enc:
        cred.last_refresh_status = RefreshStatus.failed
        cred.last_refresh_error = (
            "No refresh token available. "
            "Re-authorize with offline_access enabled."
        )
        cred.last_refresh_at = datetime.utcnow()
        return

    refresh_token = decrypt(cred.refresh_token_enc)
    client_secret = decrypt(cred.client_secret_enc)

    resp = requests.post(
        _TOKEN_URL,
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": cred.client_id,
            "client_secret": client_secret,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=_TIMEOUT,
    )
    if resp.status_code != 200:
        cred.last_refresh_status = RefreshStatus.failed
        cred.last_refresh_error = f"{resp.status_code} {resp.text[:500]}"
        cred.last_refresh_at = datetime.utcnow()
        return

    payload = resp.json()
    expires_in = int(payload.get("expires_in", 5184000))

    cred.access_token_enc = encrypt(payload["access_token"])
    if "refresh_token" in payload:
        cred.refresh_token_enc = encrypt(payload["refresh_token"])
    cred.expires_at = datetime.utcnow() + timedelta(seconds=expires_in)
    cred.last_refresh_at = datetime.utcnow()
    cred.last_refresh_status = RefreshStatus.success
    cred.last_refresh_error = None
