import app.modulos.movimento.dao as encontro_dao
from app.extensoes import transactional


def buscar_encontros(paroquia: int):
    return encontro_dao.buscar_por_paroquia(paroquia)


@transactional
def criar_encontro(encontro):
    encontro_dao.salvar(encontro)


def buscar_equipes_por_movimento(id_movimento: int) -> list:
    return encontro_dao.buscar_equipes_por_movimento(id_movimento)


def buscar_equipe_por_id_e_movimento(id: int, id_movimento: int):
    return encontro_dao.buscar_equipe_por_id_e_movimento(id, id_movimento)


@transactional
def criar_equipe(equipe):
    encontro_dao.salvar_equipe(equipe)


@transactional
def atualizar_equipe(equipe_atual, nova_equipe):
    equipe_atual.nome = nova_equipe.nome
    equipe_atual.descricao = nova_equipe.descricao

def criar_evento(evento):
    encontro_dao.salvar_evento(evento)


@transactional
def atualizar_encontro(encontro, encontro_atual):
    encontro_atual.nome = encontro.nome


def buscar_encontro_por_id(_id: int, paroquia: int):
    return encontro_dao.buscar_por_id(_id, paroquia)


def buscar_eventos_por_encontro(id_encontro):
    return encontro_dao.buscar_eventos_por_encontro(id_encontro)


def buscar_evento_por_id(id_evento):
    return encontro_dao.buscar_evento_por_id(id_evento)
