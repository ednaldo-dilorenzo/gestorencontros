import pytest
from sqlalchemy import delete
from werkzeug.security import generate_password_hash 

from app import create_app, db
from app.model import Usuario, Paroquia
from faker import Faker

fake = Faker()


@pytest.fixture(scope="session")
def flask_app():
    app = create_app()

    client = app.test_client()

    ctx = app.test_request_context()
    ctx.push()

    yield client

    ctx.pop()


@pytest.fixture(scope="session")
def app_with_db(flask_app):
    db.create_all()

    yield flask_app

    db.session.commit()
    db.drop_all()


@pytest.fixture
def app_with_data(app_with_db):
    paroquia = Paroquia()
    paroquia.id = 1
    paroquia.nome = fake.name()
    db.session.add(paroquia)

    usuario = Usuario()
    usuario.id = 1
    usuario.ativo = True
    usuario.nome = fake.name()
    usuario.papel = fake.job()
    usuario.senha = generate_password_hash("123456")
    usuario.username = fake.email()
    usuario.id_paroquia = paroquia.id
    db.session.add(usuario)

    db.session.commit()

    yield app_with_db

    db.session.execute(delete(Usuario))
    db.session.execute(delete(Paroquia))
    db.session.commit()


@pytest.fixture
def test_user():
    usuario = db.session.query(Usuario).filter(Usuario.id == 1).first()
    db.session.expunge(usuario)
    return usuario
