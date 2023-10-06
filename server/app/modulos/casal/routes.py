from http import HTTPStatus
from flask import Blueprint, request, url_for, render_template
from flask_login import login_required, current_user
from app.modulos.casal.handler import listar_casais, novo_casal, editar_casal
import app.modulos.casal.service as casal_service
import app.modulos.encontro.service as encontro_service
from app.model import EquipeEncontroCasal
from app.util.security import permission


casal_bp = Blueprint("casal", __name__, url_prefix="/casais")


@casal_bp.route("", strict_slashes=False)
@login_required
@permission(["DIRIGENTE"])
def index():
    return listar_casais(
        novo_link=url_for("casal.register"), edit_link=url_for("casal.index")
    )


@casal_bp.route("/novo", methods=["GET", "POST"])
@login_required
@permission(["DIRIGENTE"])
def register():
    return novo_casal(back_link=url_for("casal.index"))


@casal_bp.route("/<hashid:id>", methods=["GET", "POST", "PATCH"])
@login_required
@permission(["DIRIGENTE"])
def editar(id):
    return editar_casal(id, back_link=url_for("casal.index"))


@casal_bp.route("/busca")
@login_required
@permission(["DIRIGENTE"])
def buscar_por_filtro():
    filtro = request.args.get("filtro")
    inscrito = request.args.get(
        "inscrito", default=False, type=lambda v: v.lower() == "true"
    )
    circulo = request.args.get("circulo")
    encontro = request.args.get("encontro", type=int)
    equipe = request.args.get("equipe", type=int)

    casais = casal_service.buscar_por_filtro_test(
        filtro=filtro,
        id_paroquia=current_user.id_paroquia,
        id_encontro=encontro,
        inscrito=inscrito,
        id_circulo=circulo,
        id_equipe=equipe,
    )

    return [
        {"id": casal.id, "nome": f"{casal.esposo.apelido}/{casal.esposa.apelido}"}
        for casal in casais
    ]


@casal_bp.route("/<hashid:id_casal>/equipe", methods=["POST", "DELETE"])
@login_required
@permission(["DIRIGENTE"])
def adicionar_equipe(id_casal):
    id_encontro = request.form.get("id_encontro", type=int)
    id_equipe = request.form.get("id_equipe", type=int)

    if not id_encontro or not id_equipe:
        return "Encontro ou equipe não fornecida", HTTPStatus.BAD_REQUEST

    if request.method == "POST":
        equipe_encontro_casal = EquipeEncontroCasal()
        equipe_encontro_casal.id_casal = id_casal
        equipe_encontro_casal.id_encontro = id_encontro
        equipe_encontro_casal.id_equipe = id_equipe

        encontro_service.adicionar_equipe_encontro_casal(equipe_encontro_casal)

        return "ok", HTTPStatus.CREATED

    equipe_encontro_casal = encontro_service.buscar_equipe_encontro_casal(
        id_equipe, id_encontro, id_casal
    )

    if not equipe_encontro_casal:
        return "Equipe não encontrada para o casal", HTTPStatus.NOT_FOUND

    encontro_service.remover_equipe_econtro_casal(equipe_encontro_casal)

    return "ok", HTTPStatus.OK


@casal_bp.route("/<hashid:id_casal>/detalhes")
@login_required
@permission(["DIRIGENTE"])
def detalhes_casal(id_casal):
    casal = casal_service.buscar_por_id(id_paroquia=1, id_casal=id_casal)
    return render_template("casal/detalhes_casal.html", casal=casal)
