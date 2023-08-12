from flask import Blueprint, render_template, request
import app.modulos.encontro.service as movimento_service
from app.model import Movimento
from app.modulos.encontro.dao import Encontro, Evento
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

encontro_bp = Blueprint("encontro", __name__, url_prefix="/encontros")


class MovimentoForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired()])
    id = StringField("id")


class EventoForm(FlaskForm):
    id = StringField("id")
    nome = StringField("Nome")
    tema = StringField("Tema")
    ano = IntegerField("Ano")


@encontro_bp.route("/")
def index():
    movimentos = movimento_service.buscar_encontros(1)
    return render_template("encontro/index.html", encontros=movimentos)


@encontro_bp.route("/register", methods=["GET", "POST"])
def register():
    movimento_form = MovimentoForm()
    if request.method == "GET":
        return render_template("encontro/register.html", form=movimento_form)

    if not movimento_form.validate_on_submit():
        return "Falha na validação do formulário", 400

    movimento = Movimento()
    movimento.nome = movimento_form.nome.data
    movimento.id_paroquia = 1
    movimento_service.criar_encontro(movimento)
    return "200", 200


@encontro_bp.route("/<int:id>/edit", methods=["GET", "POST"])
def edit(id):
    movimento = movimento_service.buscar_encontro_por_id(id, 1)

    if not movimento:
        return "Encontro não encontrado", 404

    movimento_form = MovimentoForm()

    if request.method == "GET":
        movimento_form.id.data = movimento.id
        movimento_form.nome.data = movimento.nome
        return render_template("encontro/register.html", form=movimento_form)

    novo_movimento = Movimento()
    novo_movimento.nome = movimento_form.nome.data
    movimento_service.atualizar_encontro(novo_movimento, movimento)
    return "200", 200


@encontro_bp.route("/teams")
def teams():
    return render_template("encontro/teams.html")


@encontro_bp.route("/<int:_id>/eventos")
def events(_id):
    encontro = movimento_service.buscar_encontro_por_id(_id, 1)
    eventos = movimento_service.buscar_eventos_por_encontro(_id)
    return render_template("encontro/events.html", eventos=eventos, encontro=encontro)


@encontro_bp.route("/<int:_id>/eventos/register", methods=["GET", "POST"])
def register_event(_id):
    encontro = movimento_service.buscar_encontro_por_id(_id, 1)
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

    movimento_service.criar_evento(novo_evento)

    return "200", 201


@encontro_bp.route("/<int:_id>/eventos/edit/<int:id_evento>", methods=["GET", "POST"])
def edit_event(_id, id_evento):
    encontro = movimento_service.buscar_encontro_por_id(_id, 1)
    evento = movimento_service.buscar_evento_por_id(id_evento)

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

    movimento_service.criar_evento(novo_evento)

    return "200", 201
