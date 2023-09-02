from app.model import EquipeEncontro
from app.modulos.encontro import dao as encontro_dao
from app.extensoes import transactional


@transactional
def atualizar_equipe_encontro(
    equipe_encontro_atual: EquipeEncontro, equipe_encontro_alterado: EquipeEncontro
):
    equipe_encontro_atual.id_coordenador = equipe_encontro_alterado.id_coordenador


def buscar_equipe_encontro_por_encontro(id_encontro: int, id_equipe: int):
    return encontro_dao.buscar_equipe_encontro_por_encontro(id_encontro, id_equipe)
