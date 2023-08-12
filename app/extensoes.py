from flask_sqlalchemy import SQLAlchemy
from functools import wraps

db = SQLAlchemy()


def transactional(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        result = fn(*args, **kwargs)
        db.session.commit()
        return result

    return wrapper
