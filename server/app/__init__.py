from flask import Flask
from app.modulos import (
    auth_bp,
    casal_bp,
    movimento_bp,
    usuario_bp,
    foto_bp,
    encontro_bp,
    paroquia_bp,
    dashboard_bp,
)
from app.extensoes import db, login_manager, migrate
from app.config import current_config
from app.util.filters import calculate_age
import logging


def create_app():
    """
    Creates the app.

    Args:
        config_filename (str, optional): _description_. Defaults to ''.

    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(current_config)
    app.add_template_filter(calculate_age)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "authentication.login"
    login_manager.login_message = "Por favor realize o login para executar esta ação."
    
    @app.url_value_preprocessor
    def pull_lang_code(endpoint, values):
        print(endpoint)
        print(values)
        

    app.register_blueprint(auth_bp)
    app.register_blueprint(casal_bp)
    app.register_blueprint(movimento_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(foto_bp)
    app.register_blueprint(encontro_bp)
    app.register_blueprint(paroquia_bp)
    app.register_blueprint(dashboard_bp)

    return app


def configure_logging():
    """Configures application logging level."""
    logging.basicConfig(format="[%(asctime)s] %(levelname)s %(name)s: %(message)s")
    logging.getLogger().setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
