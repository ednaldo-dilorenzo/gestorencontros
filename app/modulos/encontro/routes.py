from http import HTTPStatus
from flask import Blueprint, request
from app.model import EquipeEncontroCasal
from app.modulos.encontro import service as encontro_service
from app.modulos.equipe import service as equipe_service
from app.util.error_handler import BusinessException

encontro_bp = Blueprint("encontro", __name__, url_prefix="/encontros")


@encontro_bp.route("/<int:id_encontro>/equipes/<int:id_equipe>", methods=["PATCH"])
def definir_coordenador(id_encontro, id_equipe):
    id_coordenador = request.form.get("id_coordenador", type=int)

    if not id_coordenador:
        encontro_service.remover_coordenador_da_equipe(id_encontro, id_equipe)
        return "ok", HTTPStatus.OK

    equipe_encontro_casal_atual = encontro_service.buscar_equipe_encontro_casal(
        id_encontro=id_encontro, id_equipe=id_equipe, id_casal=id_coordenador
    )
    equipe_encontro_alterado = EquipeEncontroCasal()
    equipe_encontro_alterado.id_encontro = id_encontro
    equipe_encontro_alterado.id_equipe = id_equipe
    equipe_encontro_alterado.id_casal = id_coordenador
    equipe_encontro_alterado.coordenador = True

    if not equipe_encontro_casal_atual:
        encontro_service.adicionar_equipe_encontro_casal(equipe_encontro_alterado)
    else:
        try:
            encontro_service.atualizar_equipe_encontro(equipe_encontro_casal_atual, equipe_encontro_alterado)
        except BusinessException as bex:
            return str(bex), HTTPStatus.UNPROCESSABLE_ENTITY

    return "ok", HTTPStatus.OK


@encontro_bp.route("/<int:id_encontro>/equipes/<int:id_equipe>", methods=["GET"])
def buscar_casais_equipe(id_encontro, id_equipe):
    equipe_encontros = (
        equipe_service.buscar_equipe_encontro_casal_por_encontro_e_equipe(
            id_encontro, id_equipe
        )
    )

    return [
        {
            "id": equipe_encontro.casal.id,
            "nome": f"{equipe_encontro.casal.esposo.apelido}/{equipe_encontro.casal.esposa.apelido}",
            "coordenador": equipe_encontro.coordenador,
            "aceito": equipe_encontro.aceito,
        }
        for equipe_encontro in equipe_encontros
    ]
