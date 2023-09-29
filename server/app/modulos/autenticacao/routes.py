from flask import Blueprint, redirect, url_for, request, render_template, flash
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from app.modulos.autenticacao import service as usuario_service
from app.modulos.paroquia import service as paroquia_service
from flask_wtf import FlaskForm
from flask_login import (
    current_user,
    login_user,
    logout_user,
    login_required,
)

auth_bp = Blueprint("authentication", __name__, url_prefix="/auth")


class LoginForm(FlaskForm):
    login = StringField("Usuário", validators=[DataRequired()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    paroquia = StringField("Paroquia")


@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("authentication.login"))


@auth_bp.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("root"))
    form = LoginForm()
    paroquias = paroquia_service.buscar_paroquias()
    if request.method == "GET" or not form.validate_on_submit():
        return render_template("login.html", form=form, paroquias=paroquias)

    if logged_user := usuario_service.valida_usuario(
        form.login.data, form.senha.data, form.paroquia.data
    ):
        login_user(logged_user)
        next_url = request.args.get("next")
        return redirect(url_for(next_url)) if next_url else redirect(url_for("root"))

    flash("Login ou senha inválida")
    return render_template("login.html", form=form, paroquias=paroquias)
