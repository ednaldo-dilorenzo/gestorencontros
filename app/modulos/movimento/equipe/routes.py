from flask import Blueprint, render_template, url_for, request
import app.modulos.movimento.service as movimento_service
from flask_login import login_required
from app.model import Equipe
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm


equipe_bp = Blueprint("equipe", __name__, url_prefix="/<int:id_movimento>/equipes")


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


@equipe_bp.route("/")
@login_required
def index(id_movimento):
    equipes_movimento = movimento_service.buscar_equipes_por_movimento(id_movimento)
    return render_template(
        "movimento/equipe/index.html",
        items=equipes_movimento,
        id_movimento=id_movimento,
        back_link=url_for("movimento.index"),
    )


@equipe_bp.route("/nova", methods=["GET", "POST"])
@login_required
def nova_equipe(id_movimento):
    equipe_form = EquipeForm()

    if request.method == "GET":
        return render_template(
            "movimento/equipe/registro.html",
            form=equipe_form,
            id_movimento=id_movimento,
        )

    if not equipe_form.validate_on_submit():
        return "Falha na validação dos dados", 400

    nova_equipe = equipe_form.retorna_equipe()
    nova_equipe.id_movimento = id_movimento
    movimento_service.criar_equipe(nova_equipe)

    return "created", 201


@equipe_bp.route("/<int:id_equipe>", methods=["GET", "POST"])
@login_required
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
            "movimento/equipe/registro.html",
            form=equipe_form,
            id_movimento=id_movimento,
        )

    if not equipe_form.validate_on_submit():
        return "Falha na validação dos dados", 400

    nova_equipe = equipe_form.retorna_equipe()
    movimento_service.atualizar_equipe(equipe_atual, nova_equipe)

    return "updated", 200
