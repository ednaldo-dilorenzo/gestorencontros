from app.modulos.equipe import dao as equipe_dao


def buscar_equipes_por_encontro(id_encontro: int) -> list:
    return equipe_dao.buscar_equipes_por_encontro(id_encontro)
