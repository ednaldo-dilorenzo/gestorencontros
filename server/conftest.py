import pytest
from sqlalchemy import delete
from werkzeug.security import generate_password_hash

from app import create_app, db
from app.model import Usuario, Paroquia


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
    paroquia.nome = "Teste"
    db.session.add(paroquia)

    usuario = Usuario()
    usuario.id = 1
    usuario.ativo = True
    usuario.nome = "Teste"
    usuario.papel = "DIRIGENTE"
    usuario.senha = generate_password_hash("123456")
    usuario.username = "teste@teste.com"
    usuario.id_paroquia = paroquia.id
    db.session.add(usuario)

    db.session.commit()

    yield app_with_db

    db.session.execute(delete(Usuario))
    db.session.execute(delete(Paroquia))
    db.session.commit()
