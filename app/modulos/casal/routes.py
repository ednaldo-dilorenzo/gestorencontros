from flask import Blueprint, render_template, request, url_for, current_app
from flask_login import login_required
from app.modulos.casal.handler import CasalForm, listar_casais, novo_casal, editar_casal
import app.modulos.casal.service as casal_service
from app.util.file_handler import salvar_imagem


casal_bp = Blueprint("casal", __name__, url_prefix="/casais")


@casal_bp.route("", strict_slashes=False)
@login_required
def index():
    return listar_casais(
        novo_link=url_for("casal.register"), edit_link=url_for("casal.index")
    )


@casal_bp.route("/novo", methods=["GET", "POST"])
@login_required
def register():
    return novo_casal(back_link=url_for("casal.index"))


@casal_bp.route("/<int:id>", methods=["GET", "POST", "PATCH"])
@login_required
def editar(id):
    return editar_casal(id, back_link=url_for("casal.index"))


@casal_bp.route("/busca")
def buscar_por_filtro():
    filtro = request.args.get("filtro")
    inscrito = request.args.get("inscrito", type=bool)
    circulo = request.args.get("circulo")
    encontro = request.args.get("encontro", type=int)

    casais = casal_service.buscar_por_filtro_test(
        filtro, 1, encontro, inscrito, circulo
    )

    return [
        {"id": casal.id, "nome": f"{casal.esposo.apelido}/{casal.esposa.apelido}"}
        for casal in casais
    ]
