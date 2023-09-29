from os import environ, path
from dotenv import load_dotenv
from app.util.file_handler import FileSystemFileHandler, AWSFileHandler


# Get the folder of the top-level directory of this project
dot_env_path = environ.get("DOTENV_PATH", None)
BASEDIR = dot_env_path if dot_env_path else path.abspath(path.dirname(__file__))

load_dotenv(path.join(BASEDIR, ".env"))

ENVIRONMENT = environ.get("ENVIRONMENT", "development")


class Config(object):
    SECRET_KEY = environ.get("SECRET_KEY", "secret-key")
    DATABASE_HOST = environ.get("DATABASE_HOST", "127.0.0.1")
    DATABASE_USERNAME = environ.get("DATABASE_USERNAME", "master")
    DATABASE_PASSWORD = environ.get("DATABASE_PASSWORD", "secret")
    DATABASE_PORT = environ.get("DATABASE_PORT", "5432")

    UPLOAD_FOLDER = environ.get("UPLOAD_FOLDER")

    SQLALCHEMY_DATABASE_URI = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/encontros"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True


class DevelopmentConfig(Config):
    FLASK_ENV = "development"

    def __init__(self):
        self.file_handler = FileSystemFileHandler(Config.UPLOAD_FOLDER)


class ProductionConfig(Config):
    FLASK_ENV = "production"

    def __init__(self):
        self.file_handler = AWSFileHandler("encontros-file-prod")


current_config = (
    ProductionConfig() if ENVIRONMENT == "production" else DevelopmentConfig()
)
