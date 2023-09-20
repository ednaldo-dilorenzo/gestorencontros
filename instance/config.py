import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "secret-key")
DATABASE_HOST = os.getenv("DATABASE_HOST", "127.0.0.1")
DATABASE_USERNAME = os.getenv("DATABASE_USERNAME", "master")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "secret")
DATABASE_PORT = os.getenv("DATABASE_PORT", "5432")

# Get the folder of the top-level directory of this project
BASEDIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = "/home/edsf/Imagens"

SQLALCHEMY_DATABASE_URI = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/encontros"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True