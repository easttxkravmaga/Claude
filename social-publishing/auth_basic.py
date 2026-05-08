import hmac
import os
from functools import wraps

from flask import request, Response


_admin_user = os.environ.get("ADMIN_USER", "etkm")
_admin_pass = os.environ.get("ADMIN_PASS")


def _check(user: str, password: str) -> bool:
    if not _admin_pass:
        return False
    user_ok = hmac.compare_digest(user, _admin_user)
    pass_ok = hmac.compare_digest(password, _admin_pass)
    return user_ok and pass_ok


def require_basic_auth(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        auth = request.authorization
        if not auth or not _check(auth.username or "", auth.password or ""):
            return Response(
                "Authentication required.",
                401,
                {"WWW-Authenticate": 'Basic realm="ETKM Publishing"'},
            )
        return view(*args, **kwargs)
    return wrapped
