from flask import Blueprint, render_template, request
import app.modulos.encontro.service as encontroService
from app.modulos.encontro.dao import Encontro, Evento
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

encontro_bp = Blueprint("encontro", __name__, url_prefix="/encontros")


class EncontroForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired()])
    id = StringField("id")


class EventoForm(FlaskForm):
    id = StringField("id")
    nome = StringField("Nome")
    tema = StringField("Tema")
    ano = IntegerField("Ano")


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


@encontro_bp.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    encontro = encontroService.buscar_encontro_por_id(id, 1)

    if not encontro:
        return "Encontro não encontrado", 404

    encontroForm = EncontroForm()
    encontroForm.id.data = encontro.id
    encontroForm.nome.data = encontro.nome

    if request.method == "GET":
        return render_template("encontro/register.html", form=encontroForm)

    novo_encontro = Encontro(encontroForm.id.data, encontroForm.nome.data, 1)
    encontroService.atualizar_encontro(novo_encontro)
    return "200", 200


@encontro_bp.route("/teams")
def teams():
    return render_template("encontro/teams.html")


@encontro_bp.route("/<int:_id>/eventos")
def events(_id):
    encontro = encontroService.buscar_encontro_por_id(_id, 1)
    eventos = encontroService.buscar_eventos_por_encontro(_id)
    return render_template("encontro/events.html", eventos=eventos, encontro=encontro)


@encontro_bp.route("/<int:_id>/eventos/register", methods=["GET", "POST"])
def register_event(_id):
    encontro = encontroService.buscar_encontro_por_id(_id, 1)
    evento_form = EventoForm()

    if request.method == "GET":
        return render_template(
            "encontro/regevent.html", form=evento_form, encontro=encontro
        )

    if not evento_form.validate_on_submit():
        return "Falha na validação do formulário", 400

    novo_evento = Evento(
        1,
        evento_form.nome.data,
        evento_form.ano.data,
        evento_form.tema.data,
        "incio",
        "fim",
        _id,
        1,
    )

    encontroService.criar_evento(novo_evento)

    return "200", 201


@encontro_bp.route("/<int:_id>/eventos/edit/<int:id_evento>", methods=["GET", "POST"])
def edit_event(_id, id_evento):
    encontro = encontroService.buscar_encontro_por_id(_id, 1)
    evento = encontroService.buscar_evento_por_id(id_evento)

    if not evento:
        return "Evento não encontrado", 404

    evento_form = EventoForm()

    if request.method == "GET":
        return render_template(
            "encontro/regevent.html", form=evento_form, encontro=encontro
        )

    if not evento_form.validate_on_submit():
        return "Falha na validação do formulário", 400

    novo_evento = Evento(
        1,
        evento_form.nome.data,
        evento_form.ano.data,
        evento_form.tema.data,
        "incio",
        "fim",
        _id,
        1,
    )

    encontroService.criar_evento(novo_evento)

    return "200", 201
