from flask import Blueprint, render_template, request
import app.modulos.usuario.service as usuario_service
from app.model import Usuario
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email
from flask_wtf import FlaskForm


usuario_bp = Blueprint("usuario", __name__, url_prefix="/usuarios")


@usuario_bp.route("/")
def index():
    dados = usuario_service.buscar_por_paroquia(1)
    return render_template("usuario/index.html", page=dados)


class UsuarioForm(FlaskForm):
    id = StringField("id")
    username = StringField("username", validators=[DataRequired()])
    senha = PasswordField("senha")
    nome = StringField("nome", validators=[DataRequired()])
    ativo = BooleanField("ativo", default=False)

    def retorna_usuario(self):
        resultado = Usuario()
        resultado.username = self.username.data
        resultado.senha = self.senha.data
        resultado.nome = self.nome.data
        resultado.ativo = self.ativo.data
        resultado.id_paroquia = 1
        return resultado


@usuario_bp.route("/registrar", methods=["GET", "POST"])
def registrar():
    usuario_form = UsuarioForm()

    if request.method == "GET":
        return render_template("usuario/registrar.html", form=usuario_form)

    if not usuario_form.validate_on_submit():
        return "Falha na validação", 400

    novo_usuario = usuario_form.retorna_usuario()
    usuario_service.salvar(novo_usuario)

    return "ok", 201


@usuario_bp.route("/<int:id_usuario>", methods=["GET", "POST"])
def editar(id_usuario):
    usuario_form = UsuarioForm()
    usuario_atual = usuario_service.buscar_por_id_e_paroquia(id_usuario, 1)

    if not usuario_atual:
        return "Usuário não encontrado", 404

    if request.method == "GET":
        usuario_form.id.data = usuario_atual.id
        usuario_form.ativo.data = usuario_atual.ativo
        usuario_form.nome.data = usuario_atual.nome
        usuario_form.username.data = usuario_atual.username
        return render_template("usuario/registrar.html", form=usuario_form)

    if not usuario_form.validate_on_submit():
        return "Falha na validação do form", 400

    usuario_alterado = usuario_form.retorna_usuario()
    usuario_service.editar(usuario_atual, usuario_alterado)

    return "ok", 200
