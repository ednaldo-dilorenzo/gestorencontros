from app.model import EquipeEncontroCasal
from app.util.error_handler import BusinessException
from app.modulos.encontro import dao as encontro_dao
from app.extensoes import transactional


@transactional
def atualizar_equipe_encontro(
    equipe_encontro_casal_atual: EquipeEncontroCasal,
    equipe_encontro_alterado: EquipeEncontroCasal,
):
    if equipe_encontro_alterado.coordenador is not None:
        if (
            not equipe_encontro_casal_atual.coordenador
            and equipe_encontro_alterado.coordenador
        ):
            equipe_casal_coordena = encontro_dao.buscar_equipe_casal_coordena(
                equipe_encontro_alterado.id_casal, equipe_encontro_alterado.id_encontro
            )

            if (
                equipe_casal_coordena
                and equipe_casal_coordena.id_equipe != equipe_encontro_alterado.id_equipe
            ):
                raise BusinessException(
                    "Tentativa de alocar casal para coordenar mais de uma equipe"
                )

            if coordenador_atual_da_equipe := encontro_dao.buscar_coordenador_da_equipe_no_encontro(
                equipe_encontro_casal_atual.id_encontro,
                equipe_encontro_casal_atual.id_equipe,
            ):
                coordenador_atual_da_equipe.coordenador = False

            equipe_encontro_casal_atual.coordenador = True
        elif (
            equipe_encontro_casal_atual.coordenador != equipe_encontro_alterado.coordenador
        ):
            equipe_encontro_casal_atual.coordenador = False

    if (
        equipe_encontro_alterado.aceito is not None
        and equipe_encontro_casal_atual.aceito != equipe_encontro_alterado.aceito
    ):
        equipe_encontro_casal_atual.aceito = equipe_encontro_alterado.aceito


@transactional
def remover_coordenador_da_equipe(id_encontro: int, id_equipe: int):
    if coordenador_atual_da_equipe := encontro_dao.buscar_coordenador_da_equipe_no_encontro(
        id_encontro, id_equipe
    ):
        coordenador_atual_da_equipe.coordenador = False


def buscar_equipe_encontro_por_encontro(id_encontro: int, id_equipe: int):
    return encontro_dao.buscar_equipe_encontro_por_encontro(id_encontro, id_equipe)


def buscar_equipe_encontro_casal(
    id_equipe: int, id_encontro: int, id_casal: int
) -> EquipeEncontroCasal:
    return encontro_dao.buscar_equipe_encontro_casal(id_equipe, id_encontro, id_casal)


@transactional
def adicionar_equipe_encontro_casal(equipe_encontro_casal: EquipeEncontroCasal):
    return encontro_dao.adicionar_equipe_encontro_casal(equipe_encontro_casal)


@transactional
def remover_equipe_econtro_casal(equipe_encontro_casal: EquipeEncontroCasal):
    return encontro_dao.remover_equipe_encontro_casal(equipe_encontro_casal)
