from flask import Blueprint, render_template, request
import modulos.encontro.service as encontroService
from modulos.encontro.dao import Encontro
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

encontro_bp = Blueprint("encontro", __name__, url_prefix="/encontros")


class EncontroForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired()])


@encontro_bp.route("/")
def index():
    encontros = encontroService.buscar_encontros(1)
    return render_template("encontro/index.html", encontros=encontros)


@encontro_bp.route("/register", methods=["GET", "POST"])
def register():
    encontroForm = EncontroForm()
    if request.method == "GET":
        return render_template("encontro/register.html", form=encontroForm)
    
    if not encontroForm.validate_on_submit():
        return "Falha na validação do formulário", 400

    encontro = Encontro(1, encontroForm.nome.data, 1)
    encontroService.criar_encontro(encontro)
    return "200", 200


@encontro_bp.route("/teams")
def teams():
    return render_template("encontro/teams.html")
