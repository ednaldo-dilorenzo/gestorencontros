from flask import Blueprint, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField
import app.modulos.casal.service as casal_service


casal_bp = Blueprint("casal", __name__, url_prefix="/casais")


class CasalForm(FlaskForm):
    id = StringField("id")
    nome_esposo = StringField("nome_esposo")
    email_esposo = EmailField("email_esposo")
    nascimento_esposo = StringField("nascimento_esposo")
    telefone_esposo = StringField("telefone_esposo")
    nome_esposa = StringField("nome_esposa")
    email_esposa = EmailField("email_esposa")
    nascimento_esposa = StringField("nascimento_esposa")
    telefone_esposa = StringField("telefone_esposa")
    endereco = StringField("endereco")
    complemento = StringField("complemento")
    cidade = StringField("cidade")
    estado = StringField("estado")
    cep = StringField("cep")


@casal_bp.route("/")
def index():
    filtro = request.args.get("filtro", None)
    casais = (
        casal_service.buscar_por_filtro(filtro, 1)
        if filtro
        else casal_service.buscar_todos(1)
    )

    return render_template("casal/index.html", page=casais)


@casal_bp.route("/register", methods=["GET", "POST"])
def register():
    casal_form = CasalForm()
    if request.method == "GET":
        return render_template("casal/register.html", form=casal_form)

    if not casal_form.validate_on_submit():
        return "Falha na validação", 404

    novo_casal = None

    casal_service.salvar(novo_casal)

    return "ok", 201
