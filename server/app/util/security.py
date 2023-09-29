from functools import wraps
from flask_login import current_user


def permission(roles):
    def decorator(fn):
        @wraps(fn)
        def inner(*args, **kwargs):
            role = current_user.papel

            if role in roles:
                return fn(*args, **kwargs)

            return "Acesso negado", 403

        return inner

    return decorator
