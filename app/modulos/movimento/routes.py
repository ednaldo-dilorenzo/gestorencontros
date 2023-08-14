from flask import Blueprint, render_template, request
import app.modulos.movimento.service as movimento_service
from app.model import Movimento, Equipe
from app.modulos.movimento.dao import Evento
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

movimento_bp = Blueprint("movimento", __name__, url_prefix="/movimentos")


class MovimentoForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired()])
    id = StringField("id")


class EquipeForm(FlaskForm):
    id = StringField("id")
    nome = StringField("Nome", validators=[DataRequired()])
    descricao = StringField("Descrição", validators=[DataRequired()])

    def retorna_equipe(self):
        resultado = Equipe()
        resultado.id = self.id.data
        resultado.nome = self.nome.data
        resultado.descricao = self.descricao.data
        return resultado


class EventoForm(FlaskForm):
    id = StringField("id")
    nome = StringField("Nome")
    tema = StringField("Tema")
    ano = IntegerField("Ano")


@movimento_bp.route("/")
def index():
    movimentos = movimento_service.buscar_encontros(1)
    return render_template("movimento/index.html", movimentos=movimentos)


@movimento_bp.route("/register", methods=["GET", "POST"])
def register():
    movimento_form = MovimentoForm()
    if request.method == "GET":
        return render_template("movimento/register.html", form=movimento_form)

    if not movimento_form.validate_on_submit():
        return "Falha na validação do formulário", 400

    movimento = Movimento()
    movimento.nome = movimento_form.nome.data
    movimento.id_paroquia = 1
    movimento_service.criar_encontro(movimento)
    return "200", 200


@movimento_bp.route("/<int:id>/edit", methods=["GET", "POST"])
def edit(id):
    movimento = movimento_service.buscar_encontro_por_id(id, 1)

    if not movimento:
        return "Encontro não encontrado", 404

    movimento_form = MovimentoForm()

    if request.method == "GET":
        movimento_form.id.data = movimento.id
        movimento_form.nome.data = movimento.nome
        return render_template("movimento/register.html", form=movimento_form)

    if not movimento_form.validate_on_submit():
        return "Falha na validação do formulário", 400

    novo_movimento = Movimento()
    novo_movimento.nome = movimento_form.nome.data
    movimento_service.atualizar_encontro(novo_movimento, movimento)
    return "200", 200


@movimento_bp.route("/<int:id_movimento>/equipes")
def equipes(id_movimento):
    equipes = movimento_service.buscar_equipes_por_movimento(id_movimento)
    return render_template(
        "movimento/equipe.html", items=equipes, id_movimento=id_movimento
    )


@movimento_bp.route("/<int:id_movimento>/equipes/nova", methods=["GET", "POST"])
def nova_equipe(id_movimento):
    equipe_form = EquipeForm()

    if request.method == "GET":
        return render_template(
            "movimento/equipe_registro.html",
            form=equipe_form,
            id_movimento=id_movimento,
        )

    if not equipe_form.validate_on_submit():
        return "Falha na validação dos dados", 400

    nova_equipe = equipe_form.retorna_equipe()
    nova_equipe.id_movimento = id_movimento
    movimento_service.criar_equipe(nova_equipe)

    return "created", 201


@movimento_bp.route(
    "/<int:id_movimento>/equipes/<int:id_equipe>", methods=["GET", "POST"]
)
def editar_equipe(id_movimento, id_equipe):
    equipe_atual = movimento_service.buscar_equipe_por_id_e_movimento(
        id_equipe, id_movimento
    )

    if not equipe_atual:
        return "Equipe não encontrada", 404

    equipe_form = EquipeForm()

    if request.method == "GET":
        equipe_form.id.data = equipe_atual.id
        equipe_form.nome.data = equipe_atual.nome
        equipe_form.descricao.data = equipe_atual.descricao
        return render_template(
            "movimento/equipe_registro.html",
            form=equipe_form,
            id_movimento=id_movimento,
        )

    if not equipe_form.validate_on_submit():
        return "Falha na validação dos dados", 400

    nova_equipe = equipe_form.retorna_equipe()
    movimento_service.atualizar_equipe(equipe_atual, nova_equipe)

    return "updated", 200


@movimento_bp.route("/<int:_id>/encontros")
def encontros(_id):
    encontro = movimento_service.buscar_encontro_por_id(_id, 1)
    eventos = movimento_service.buscar_eventos_por_encontro(_id)
    return render_template("movimento/events.html", eventos=eventos, encontro=encontro)


@movimento_bp.route("/<int:_id>/eventos/register", methods=["GET", "POST"])
def register_event(_id):
    encontro = movimento_service.buscar_encontro_por_id(_id, 1)
    evento_form = EventoForm()

    if request.method == "GET":
        return render_template(
            "movimento/regevent.html", form=evento_form, encontro=encontro
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


@movimento_bp.route("/<int:_id>/eventos/edit/<int:id_evento>", methods=["GET", "POST"])
def edit_event(_id, id_evento):
    encontro = movimento_service.buscar_encontro_por_id(_id, 1)
    evento = movimento_service.buscar_evento_por_id(id_evento)

    if not evento:
        return "Evento não encontrado", 404

    evento_form = EventoForm()

    if request.method == "GET":
        return render_template(
            "movimento/regevent.html", form=evento_form, encontro=encontro
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
