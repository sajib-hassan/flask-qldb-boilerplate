from functools import wraps

from hash_chain.app.modules.auth.services import Auth
from hash_chain.app.util.exceptions import ApiForbidden


def token_required(f):
    """Execute function if request contains valid access token."""

    @wraps(f)
    def decorated(*args, **kwargs):
        token_payload = Auth.check_access_token(admin_only=False)
        if not token_payload.get("token"):
            raise ApiForbidden()

        # for name, val in token_payload.items():
        #     setattr(decorated, name, val)

        return f(*args, **kwargs)

    return decorated


def admin_token_required(f):
    """Execute function if request contains valid access token AND user is admin."""

    @wraps(f)
    def decorated(*args, **kwargs):
        token_payload = Auth.check_access_token(admin_only=True)
        if not token_payload.get("admin"):
            raise ApiForbidden()
        # for name, val in token_payload.items():
        #     setattr(decorated, name, val)
        return f(*args, **kwargs)

    return decorated
