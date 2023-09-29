from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def transactional(fn):
    """
    Decorator para colocar funções de serviço em uma transação.

    Args:
        fn (function): Função a ser chamada de forma atômica.

    Returns:
        _type_: Retorna o resultado da função caso exista o mesmo.
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        result = fn(*args, **kwargs)
        db.session.commit()
        return result

    return wrapper
