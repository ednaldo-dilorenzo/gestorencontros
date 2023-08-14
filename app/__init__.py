from flask import Flask
from flask_login import LoginManager
from app.modulos import auth_bp, casal_bp, movimento_bp
from app.extensoes import db
import logging


login_manager = LoginManager()


def create_app(config_filename: str = ""):
    """
    Creates the app.

    Args:
        config_filename (str, optional): _description_. Defaults to ''.

    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_filename)
    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return None

    app.register_blueprint(auth_bp)
    app.register_blueprint(casal_bp)
    app.register_blueprint(movimento_bp)

    return app


def configure_logging():
    """Configures application logging level."""
    logging.basicConfig(format="[%(asctime)s] %(levelname)s %(name)s: %(message)s")
    logging.getLogger().setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
