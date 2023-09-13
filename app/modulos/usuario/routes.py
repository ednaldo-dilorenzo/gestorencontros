from http import HTTPStatus
from flask import Blueprint, render_template, request
import app.modulos.usuario.service as usuario_service
from app.modulos.paroquia import service as paroquia_service
from app.model import Usuario
from wtforms import StringField, PasswordField, BooleanField, HiddenField, SelectField
from wtforms.validators import DataRequired, Optional
from flask_wtf import FlaskForm
from flask_login import login_required, current_user
from app.util.constants import Roles


usuario_bp = Blueprint("usuario", __name__, url_prefix="/usuarios")


@usuario_bp.route("", strict_slashes=False)
@login_required
def index():
    page = request.args.get("page", type=int)
    per_page = request.args.get("per_page", type=int)
    dados = (
        usuario_service.buscar_por_paroquia(
            current_user.id_paroquia, page=page, per_page=per_page
        )
        if current_user.papel == Roles.ROLE_DIRIGENTE
        else usuario_service.buscar_todos(page=page, per_page=per_page)
    )
    return render_template("usuario/index.html", page=dados)


class UsuarioForm(FlaskForm):
    id = HiddenField("id")
    username = StringField("Email", validators=[DataRequired()])
    nome = StringField("Nome", validators=[DataRequired()])
    senha = PasswordField("Senha")
    ativo = BooleanField("Ativo", default=False)
    id_paroquia = SelectField(
        "Paroquia",
        choices=(),
        validators=[Optional()],
        validate_choice=False,
        coerce=int,
    )

    def retorna_usuario(self):
        resultado = Usuario()
        resultado.username = self.username.data
        resultado.senha = self.senha.data
        resultado.nome = self.nome.data
        resultado.ativo = self.ativo.data
        return resultado


@usuario_bp.route("/registrar", methods=["GET", "POST"])
@login_required
def registrar():
    usuario_form = UsuarioForm()

    if request.method == "GET":
        if current_user.papel == Roles.ROLE_ADMIN:
            paroquias = [(-1, "Selecione...")] + [
                (paroquia.id, paroquia.nome)
                for paroquia in paroquia_service.buscar_paroquias()
            ]
            usuario_form.id_paroquia.choices = paroquias
        return render_template("usuario/registrar.html", form=usuario_form)

    if not usuario_form.validate_on_submit():
        return "Falha na validação", HTTPStatus.BAD_REQUEST

    novo_usuario = usuario_form.retorna_usuario()
    if current_user.papel == Roles.ROLE_ADMIN:
        novo_usuario.id_paroquia = (
            usuario_form.id_paroquia.data if usuario_form.id_paroquia.data > 0 else None
        )
    else:
        novo_usuario.id_paroquia = current_user.id_paroquia

    usuario_service.salvar(novo_usuario)

    return "ok", HTTPStatus.CREATED


@usuario_bp.route("/<int:id_usuario>", methods=["GET", "POST"])
@login_required
def editar(id_usuario):
    usuario_form = UsuarioForm()

    usuario_atual = (
        usuario_service.buscar_por_id_e_paroquia(id_usuario, current_user.id_paroquia)
        if current_user.papel == Roles.ROLE_DIRIGENTE
        else usuario_service.buscar_por_id(id_usuario)
    )

    if not usuario_atual:
        return "Usuário não encontrado", HTTPStatus.NOT_FOUND

    if request.method == "GET":
        usuario_form.id.data = usuario_atual.id
        usuario_form.ativo.data = usuario_atual.ativo
        usuario_form.nome.data = usuario_atual.nome
        usuario_form.username.data = usuario_atual.username
        if current_user.papel == Roles.ROLE_ADMIN:
            paroquias = [(-1, "Selecione...")] + [
                (paroquia.id, paroquia.nome)
                for paroquia in paroquia_service.buscar_paroquias()
            ]
            usuario_form.id_paroquia.choices = paroquias
            if usuario_atual.id_paroquia:
                usuario_form.id_paroquia.data = usuario_atual.id_paroquia

        return render_template("usuario/registrar.html", form=usuario_form)

    if not usuario_form.validate_on_submit():
        return "Falha na validação do form", HTTPStatus.BAD_REQUEST

    usuario_alterado = usuario_form.retorna_usuario()
    if current_user.papel == Roles.ROLE_ADMIN:
        usuario_alterado.id_paroquia = (
            usuario_form.id_paroquia.data if usuario_form.id_paroquia.data > 0 else None
        )
    else:
        usuario_alterado.id_paroquia = current_user.id_paroquia

    usuario_service.editar(usuario_atual, usuario_alterado)

    return "ok", HTTPStatus.OK
