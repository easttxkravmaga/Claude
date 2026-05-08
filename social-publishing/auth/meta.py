"""Meta short-lived → long-lived Page token exchange.

Three-step flow:
  1. Exchange short-lived user token for long-lived user token (~60 days)
  2. List Pages the user manages, pick the ETKM Page, capture the Page Access
     Token (this token never expires)
  3. Get Instagram Business Account ID linked to the Page

Result: one OAuthCredential row with provider='meta', the Page token, page_id,
ig_account_id, and expires_at = NULL (Page tokens are perpetual).
"""

from datetime import datetime

import requests
from sqlalchemy import select

from db import SessionLocal
from models import OAuthCredential, Provider, RefreshStatus
from security import encrypt


_GRAPH = "https://graph.facebook.com/v19.0"
_TIMEOUT = 30


class MetaError(Exception):
    pass


def _get_long_lived_user_token(app_id: str, app_secret: str, short_token: str) -> str:
    resp = requests.get(
        f"{_GRAPH}/oauth/access_token",
        params={
            "grant_type": "fb_exchange_token",
            "client_id": app_id,
            "client_secret": app_secret,
            "fb_exchange_token": short_token,
        },
        timeout=_TIMEOUT,
    )
    if resp.status_code != 200:
        raise MetaError(_friendly_error(resp))
    payload = resp.json()
    token = payload.get("access_token")
    if not token:
        raise MetaError("Long-lived user token exchange returned no access_token")
    return token


def _list_pages(long_user_token: str) -> list[dict]:
    resp = requests.get(
        f"{_GRAPH}/me/accounts",
        params={"access_token": long_user_token, "fields": "id,name,access_token,tasks"},
        timeout=_TIMEOUT,
    )
    if resp.status_code != 200:
        raise MetaError(_friendly_error(resp))
    return resp.json().get("data", [])


def _get_ig_account_id(page_id: str, page_token: str) -> str | None:
    resp = requests.get(
        f"{_GRAPH}/{page_id}",
        params={"access_token": page_token, "fields": "instagram_business_account"},
        timeout=_TIMEOUT,
    )
    if resp.status_code != 200:
        raise MetaError(_friendly_error(resp))
    data = resp.json().get("instagram_business_account") or {}
    return data.get("id")


def _friendly_error(resp: requests.Response) -> str:
    try:
        body = resp.json()
        err = body.get("error", {})
        code = err.get("code")
        message = err.get("message", resp.text)
        if code == 190:
            return (
                "The short-lived token has expired or is invalid. "
                "Generate a new one in Graph API Explorer and try again."
            )
        if code == 10 or "permission" in message.lower():
            return (
                "App is missing required permissions. Re-generate the token "
                "with: pages_show_list, pages_read_engagement, pages_manage_posts, "
                "instagram_basic, instagram_content_publish, business_management."
            )
        return f"Meta error code={code}: {message}"
    except ValueError:
        return f"Meta error {resp.status_code}: {resp.text[:500]}"


def exchange(
    app_id: str,
    app_secret: str,
    short_lived_token: str,
    label: str = "ETKM Meta",
) -> OAuthCredential:
    """Run the full 3-step exchange and persist the resulting credential."""

    long_user_token = _get_long_lived_user_token(app_id, app_secret, short_lived_token)

    pages = _list_pages(long_user_token)
    if not pages:
        raise MetaError(
            "Generated token does not manage any Facebook Page. "
            "Confirm the user is an admin of the ETKM Page."
        )

    # ETKM only manages one Page; if multiples ever exist, the first is fine
    # and Nathan can re-run after picking a specific one.
    page = pages[0]
    page_id = page["id"]
    page_token = page["access_token"]
    page_name = page.get("name", "")

    ig_account_id = _get_ig_account_id(page_id, page_token)
    if not ig_account_id:
        raise MetaError(
            f"Facebook Page '{page_name}' is not linked to an Instagram "
            "Business Account. Connect them in Meta Business Suite first."
        )

    with SessionLocal() as session:
        existing = session.scalar(
            select(OAuthCredential).where(
                OAuthCredential.provider == Provider.meta,
                OAuthCredential.label == label,
            )
        )
        if existing is None:
            cred = OAuthCredential(
                provider=Provider.meta,
                label=label,
                client_id=app_id,
                client_secret_enc=encrypt(app_secret),
                access_token_enc=encrypt(page_token),
                refresh_token_enc=None,
                expires_at=None,
                page_id=page_id,
                ig_account_id=ig_account_id,
                last_refresh_at=datetime.utcnow(),
                last_refresh_status=RefreshStatus.success,
            )
            session.add(cred)
        else:
            existing.client_id = app_id
            existing.client_secret_enc = encrypt(app_secret)
            existing.access_token_enc = encrypt(page_token)
            existing.refresh_token_enc = None
            existing.expires_at = None
            existing.page_id = page_id
            existing.ig_account_id = ig_account_id
            existing.last_refresh_at = datetime.utcnow()
            existing.last_refresh_status = RefreshStatus.success
            existing.last_refresh_error = None
            cred = existing
        session.commit()
        session.refresh(cred)
        return cred


def refresh(cred: OAuthCredential) -> None:
    """Meta long-lived Page tokens never expire. No-op refresh.

    If a token is invalidated (password change, app revoke, security event),
    the next publish attempt fails with code=190 and the post-publisher writes
    the error to the post row. Manual re-authorization required.
    """
    cred.last_refresh_at = datetime.utcnow()
    cred.last_refresh_status = RefreshStatus.success
    cred.last_refresh_error = None
