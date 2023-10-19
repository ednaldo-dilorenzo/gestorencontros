from http import HTTPStatus
from flask import url_for


def test_get_login(app_with_db):
    response = app_with_db.get(url_for("authentication.login"))
    assert response.status_code == HTTPStatus.OK.value


def test_post_login_form_not_valid(app_with_data):
    response = app_with_data.post(
        url_for("authentication.login"), data={"username": "testando", "senha": "123"}
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST.value


def test_post_login_wrong_password(app_with_data):
    response = app_with_data.post(
        url_for("authentication.login"),
        data={"login": "teste@teste.com", "senha": "12345689", "paroquia": 1},
        follow_redirects=True,
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED.value


def test_post_login_ok(app_with_data):
    response = app_with_data.post(
        url_for("authentication.login"),
        data={"login": "teste@teste.com", "senha": "123456", "paroquia": 1},
        follow_redirects=True,
    )
    assert response.status_code == HTTPStatus.OK.value
