from http import HTTPStatus
from flask import Blueprint, render_template, request, url_for
from flask_login import current_user
import app.modulos.movimento.service as movimento_service
from app.model import Movimento
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_login import login_required
from flask_wtf import FlaskForm
from app.modulos.movimento.equipe.routes import equipe_bp
from app.modulos.movimento.encontro.routes import encontro_bp

movimento_bp = Blueprint("movimento", __name__, url_prefix="/movimentos")
movimento_bp.register_blueprint(equipe_bp)
movimento_bp.register_blueprint(encontro_bp)


class MovimentoForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired()])
    id = StringField("id")


@movimento_bp.route("", strict_slashes=False)
@login_required
def index():
    movimentos = movimento_service.buscar_encontros(current_user.id_paroquia)
    return render_template("movimento/index.html", movimentos=movimentos)


@movimento_bp.route("/register", methods=["GET", "POST"])
@login_required
def register():
    movimento_form = MovimentoForm()
    if request.method == "GET":
        return render_template(
            "movimento/register.html",
            form=movimento_form,
            back_link=url_for("movimento.index"),
        )

    if not movimento_form.validate_on_submit():
        return "Falha na validação do formulário", HTTPStatus.BAD_REQUEST

    movimento = Movimento()
    movimento.nome = movimento_form.nome.data
    movimento.id_paroquia = current_user.id_paroquia
    movimento_service.criar_movimento(movimento)
    return "ok", HTTPStatus.OK


@movimento_bp.route("/<hashid:id_movimento>", methods=["GET", "POST"])
@login_required
def edit(id_movimento):
    movimento = movimento_service.buscar_movimento_por_id(id_movimento, current_user.id_paroquia)

    if not movimento:
        return "Encontro não encontrado", HTTPStatus.NOT_FOUND

    movimento_form = MovimentoForm()

    if request.method == "GET":
        movimento_form.id.data = movimento.id
        movimento_form.nome.data = movimento.nome
        return render_template(
            "movimento/register.html",
            form=movimento_form,
            back_link=url_for("movimento.index"),
        )

    if not movimento_form.validate_on_submit():
        return "Falha na validação do formulário", HTTPStatus.BAD_REQUEST

    novo_movimento = Movimento()
    novo_movimento.nome = movimento_form.nome.data
    movimento_service.atualizar_movimento(movimento, novo_movimento)
    return "ok", HTTPStatus.OK
