from flask import Flask
from app.modulos import auth_bp, casal_bp, movimento_bp, usuario_bp, foto_bp
from app.extensoes import db, login_manager, migrate
import logging


def create_app(config_filename: str = ""):
    """
    Creates the app.

    Args:
        config_filename (str, optional): _description_. Defaults to ''.

    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_filename)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "authentication.login"
    login_manager.login_message = "Por favor realize o login para executar esta ação."

    app.register_blueprint(auth_bp)
    app.register_blueprint(casal_bp)
    app.register_blueprint(movimento_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(foto_bp)
    

    return app


def configure_logging():
    """Configures application logging level."""
    logging.basicConfig(format="[%(asctime)s] %(levelname)s %(name)s: %(message)s")
    logging.getLogger().setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
