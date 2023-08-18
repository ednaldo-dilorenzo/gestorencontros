from flask import Blueprint, render_template, request
from flask_wtf import FlaskForm
from flask_login import login_required
from wtforms import StringField, EmailField, IntegerField, DateField
from wtforms.validators import DataRequired, Optional
import app.modulos.casal.service as casal_service
from app.model import Casal, Pessoa


casal_bp = Blueprint("casal", __name__, url_prefix="/casais")


class CasalForm(FlaskForm):
    id = StringField("id")
    id_esposo = IntegerField("id_esposo")
    nome_esposo = StringField("nome_esposo", validators=[DataRequired()])
    apelido_esposo = StringField("apelido_esposo", validators=[DataRequired()])
    email_esposo = EmailField("email_esposo", validators=[DataRequired()])
    nascimento_esposo = DateField("nascimento_esposo", validators=[Optional()])
    telefone_esposo = StringField("telefone_esposo", validators=[DataRequired()])
    id_esposa = IntegerField("id_esposa")
    nome_esposa = StringField("nome_esposa", validators=[DataRequired()])
    apelido_esposa = StringField("apelido_esposa", validators=[DataRequired()])
    email_esposa = EmailField("email_esposa", validators=[DataRequired()])
    nascimento_esposa = DateField("nascimento_esposa", validators=[Optional()])
    telefone_esposa = StringField("telefone_esposa", validators=[DataRequired()])
    endereco = StringField("endereco")
    complemento = StringField("complemento")
    cidade = StringField("cidade")
    estado = StringField("estado")
    cep = StringField("cep")

    def retorna_casal(self) -> Casal:
        casal = Casal()
        casal.id = self.id.data if self.id.data else None
        casal.id_paroquia = 1
        casal.esposo = Pessoa()
        casal.esposo.id = self.id_esposo.data if self.id_esposo.data else None
        casal.esposo.id_paroquia = 1
        casal.esposo.nome = self.nome_esposo.data
        casal.esposo.apelido = self.apelido_esposo.data
        casal.esposo.email = self.email_esposo.data
        casal.esposo.telefone = self.telefone_esposo.data
        casal.esposo.nascimento = self.nascimento_esposo.data
        casal.esposa = Pessoa()
        casal.esposa.id = self.id_esposa.data if self.id_esposa.data else None
        casal.esposa.id_paroquia = 1
        casal.esposa.nome = self.nome_esposa.data
        casal.esposa.apelido = self.apelido_esposa.data
        casal.esposa.email = self.email_esposa.data
        casal.esposa.telefone = self.telefone_esposa.data
        casal.esposa.nascimento = self.nascimento_esposa.data

        return casal


@casal_bp.route("/")
@login_required
def index():
    filtro = request.args.get("filtro", None)
    page = int(page) if (page := request.args.get("page", None)) else 1
    per_page = int(per_page) if (per_page := request.args.get("per_page", None)) else 10
    casais = (
        casal_service.buscar_por_filtro(filtro, 1)
        if filtro
        else casal_service.buscar_todos(1, page, per_page)
    )

    return render_template("casal/index.html", page=casais, filtro=filtro)


@casal_bp.route("/register", methods=["GET", "POST"])
@login_required
def register():
    casal_form = CasalForm()
    page = int(page) if (page := request.args.get("page", None)) else 1
    per_page = int(per_page) if (per_page := request.args.get("per_page", None)) else 10
    if request.method == "GET":
        return render_template(
            "casal/register.html", form=casal_form, page=page, per_page=per_page
        )

    if not casal_form.validate_on_submit():
        return "Falha na validação", 400

    novo_casal = casal_form.retorna_casal()

    casal_service.salvar(novo_casal)

    return "ok", 201


@casal_bp.route("/<int:id>/editar", methods=["GET", "POST"])
@login_required
def editar(id):
    casal = casal_service.buscar_por_id(id, 1)

    if not casal:
        return "Casal não encontrado", 404

    page = request.args.get("page", None)
    page = int(page) if page and page.isdigit() else 1
    per_page = request.args.get("per_page", None)
    per_page = int(per_page) if per_page and per_page.isdigit() else 10

    casal_form = CasalForm()

    if request.method == "GET":
        casal_form.id.data = casal.id
        casal_form.nome_esposo.data = casal.esposo.nome
        casal_form.apelido_esposo.data = casal.esposo.apelido
        casal_form.nascimento_esposo.data = casal.esposo.nascimento
        casal_form.nome_esposa.data = casal.esposa.nome
        casal_form.apelido_esposa.data = casal.esposa.apelido
        casal_form.email_esposo.data = casal.esposo.email
        casal_form.email_esposa.data = casal.esposa.email
        casal_form.telefone_esposo.data = casal.esposo.telefone
        casal_form.telefone_esposa.data = casal.esposa.telefone
        casal_form.nascimento_esposa.data = casal.esposa.nascimento

        return render_template(
            "casal/register.html", form=casal_form, page=page, per_page=per_page
        )

    if not casal_form.validate_on_submit():
        return "Falha na validação do formulário", 400

    casal_atualizado = casal_form.retorna_casal()

    casal_service.atualizar_casal(casal, casal_atualizado)

    return "Casal atualizado com sucesso", 200


@casal_bp.route("/busca")
def buscar_por_filtro():
    filtro = request.args.get("filtro")
    encontro = request.args.get("encontro")
    resultado = []
    if encontro and encontro.isdigit():
        casais = casal_service.buscar_por_filtro_nao_inscrito(filtro, 1, int(encontro))
        resultado = [
            {"id": casal.id, "nome": f"{casal.esposo.apelido}/{casal.esposa.apelido}"}
            for casal in casais
        ]

    return resultado
