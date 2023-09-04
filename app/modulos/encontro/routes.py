from flask import Blueprint, request
from app.model import EquipeEncontro
from app.modulos.encontro import service as encontro_service
from app.util.error_handler import BusinessException

encontro_bp = Blueprint("encontro", __name__, url_prefix="/encontros")


@encontro_bp.route("/<int:id_encontro>/equipes/<int:id_equipe>", methods=["PATCH"])
def definir_coordenador(id_encontro, id_equipe):
    equipe_encontro = encontro_service.buscar_equipe_encontro_por_encontro(
        id_encontro, id_equipe
    )

    equipe_encontro_alterado = EquipeEncontro()
    equipe_encontro_alterado.id_encontro = equipe_encontro.id_encontro
    equipe_encontro_alterado.id_equipe = equipe_encontro.id_equipe
    equipe_encontro_alterado.id_coordenador = request.form.get("id_coordenador", type=int)

    try:
        encontro_service.atualizar_equipe_encontro(
            equipe_encontro, equipe_encontro_alterado
        )
    except BusinessException as bex:
        return str(bex), 422

    return "ok", 200
