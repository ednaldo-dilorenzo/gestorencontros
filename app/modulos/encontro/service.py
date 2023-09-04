from app.model import EquipeEncontro
from app.util.error_handler import BusinessException
from app.modulos.encontro import dao as encontro_dao
from app.extensoes import transactional


@transactional
def atualizar_equipe_encontro(
    equipe_encontro_atual: EquipeEncontro, equipe_encontro_alterado: EquipeEncontro
):
    if equipe_encontro_alterado.id_coordenador is not None:
        equipe_casal_coordenador = encontro_dao.buscar_equipe_casal_coordena(
            equipe_encontro_alterado.id_coordenador,
            equipe_encontro_alterado.id_encontro,
        )

        if (
            equipe_casal_coordenador
            and equipe_casal_coordenador.id_equipe != equipe_encontro_alterado.id_equipe
        ):
            raise BusinessException(
                "Tentativa de colocar casal para coordenar mais de uma equipe"
            )

    equipe_encontro_atual.id_coordenador = equipe_encontro_alterado.id_coordenador


def buscar_equipe_encontro_por_encontro(id_encontro: int, id_equipe: int):
    return encontro_dao.buscar_equipe_encontro_por_encontro(id_encontro, id_equipe)
