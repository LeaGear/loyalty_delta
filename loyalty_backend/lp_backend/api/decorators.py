import hmac

from functools import wraps
from django.conf import settings

from lp_backend.api.responses import fail

def api_key_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        key = request.headers.get("X-API-KEY", "")
        if not settings.BOT_API_KEY or not hmac.compare_digest(key, settings.BOT_API_KEY):
            return fail(detail="Forbidden", status_code=403)
        return view_func(request, *args, **kwargs)
    return wrapper