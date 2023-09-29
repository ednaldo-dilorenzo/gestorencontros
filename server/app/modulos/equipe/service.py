from app.modulos.equipe import dao as equipe_dao


def buscar_equipes_por_encontro(id_encontro: int) -> list:
    return equipe_dao.buscar_equipes_por_encontro(id_encontro)


def buscar_equipe_encontro_casal_por_encontro_e_equipe(
    id_encontro: int, id_equipe: int
) -> list:
    return equipe_dao.buscar_equipe_encontro_casal_por_encontro_e_equipe(
        id_encontro, id_equipe
    )
