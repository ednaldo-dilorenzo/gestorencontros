from http import HTTPStatus
from flask_login import current_user
from app.model import Casal, Pessoa
import app.modulos.casal.service as casal_service
from app.util.file_handler import salvar_imagem
from flask import request, render_template, url_for, current_app
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    EmailField,
    IntegerField,
    DateField,
    HiddenField,
    FileField,
)
from wtforms.validators import DataRequired, Optional


class CasalForm(FlaskForm):
    id = HiddenField("id")
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
    id_circulo = IntegerField("id_circulo")
    id_inscrito = HiddenField("id_inscrito")
    foto_esposo = FileField()
    foto_esposa = FileField()

    def retorna_casal(self) -> Casal:
        casal = Casal()
        casal.id = self.id.data if self.id.data else None
        casal.id_paroquia = current_user.id_paroquia
        casal.esposo = Pessoa()
        casal.esposo.id = self.id_esposo.data if self.id_esposo.data else None
        casal.esposo.id_paroquia = current_user.id_paroquia
        casal.esposo.nome = self.nome_esposo.data
        casal.esposo.apelido = self.apelido_esposo.data
        casal.esposo.email = self.email_esposo.data
        casal.esposo.telefone = self.telefone_esposo.data
        casal.esposo.nascimento = self.nascimento_esposo.data
        casal.esposa = Pessoa()
        casal.esposa.id = self.id_esposa.data if self.id_esposa.data else None
        casal.esposa.id_paroquia = current_user.id_paroquia
        casal.esposa.nome = self.nome_esposa.data
        casal.esposa.apelido = self.apelido_esposa.data
        casal.esposa.email = self.email_esposa.data
        casal.esposa.telefone = self.telefone_esposa.data
        casal.esposa.nascimento = self.nascimento_esposa.data
        casal.id_circulo = self.id_circulo.data
        casal.id_inscrito = self.id_inscrito.data if self.id_inscrito.data else None

        return casal


def listar_casais(id_inscrito=None, back_link=None, novo_link=None, edit_link=None):
    filtro = request.args.get("filtro")
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    casais = (
        casal_service.buscar_por_filtro(
            filtro, current_user.id_paroquia, id_inscrito=id_inscrito
        )
        if filtro
        else casal_service.buscar_todos(
            current_user.id_paroquia, page, per_page, id_inscrito
        )
    )

    return render_template(
        "casal/index.html",
        page=casais,
        filtro=filtro,
        inscrito=id_inscrito,
        back_link=back_link,
        novo_link=novo_link,
        edit_link=edit_link,
    )


def novo_casal(id_inscrito=None, back_link=None):
    casal_form = CasalForm()
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    if request.method == "GET":
        casal_form.id_inscrito.data = id_inscrito
        return render_template(
            "casal/register.html",
            form=casal_form,
            page=page,
            per_page=per_page,
            inscrito=id_inscrito,
            back_link=back_link,
        )

    if not casal_form.validate_on_submit():
        return "Falha na validação", HTTPStatus.BAD_REQUEST

    novo_casal = casal_form.retorna_casal()
    novo_casal = casal_service.salvar(novo_casal)
    foto_esposo = casal_form.foto_esposo.data
    foto_esposa = casal_form.foto_esposa.data
    salvar_imagem(
        foto_esposo,
        f"{novo_casal.esposo.id}_pessoa.jpg",
    )
    salvar_imagem(
        foto_esposa,
        f"{novo_casal.esposa.id}_pessoa.jpg",
    )

    return "created", HTTPStatus.CREATED


def editar_casal(id, back_link):
    casal = casal_service.buscar_por_id(id, current_user.id_paroquia)

    if not casal:
        return "Casal não encontrado", HTTPStatus.NOT_FOUND

    casal_form = CasalForm()

    if request.method == "GET":
        casal_form.id.data = casal.id
        casal_form.id_esposo.data = casal.esposo.id
        casal_form.id_esposa.data = casal.esposa.id
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

        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        return render_template(
            "casal/register.html",
            form=casal_form,
            page=page,
            per_page=per_page,
            back_link=back_link,
        )

    if request.method == "POST":
        if not casal_form.validate_on_submit():
            return "Falha na validação do formulário", HTTPStatus.BAD_REQUEST

    casal_atualizado = casal_form.retorna_casal()
    casal_service.atualizar_casal(casal, casal_atualizado)
    foto_esposo = casal_form.foto_esposo.data
    foto_esposa = casal_form.foto_esposa.data
    salvar_imagem(
        foto_esposo,
        f"{casal.esposo.id}_pessoa.jpg",
    )
    salvar_imagem(
        foto_esposa,
        f"{casal.esposa.id}_pessoa.jpg",
    )

    return "ok", HTTPStatus.OK
