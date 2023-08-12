import app.modulos.encontro.dao as encontroDao
from app.extensoes import transactional


def buscar_encontros(paroquia: int):
    return encontroDao.buscar_por_paroquia(paroquia)


@transactional
def criar_encontro(encontro):
    encontroDao.salvar(encontro)


def criar_evento(evento):
    encontroDao.salvar_evento(evento)


@transactional
def atualizar_encontro(encontro, encontro_atual):
    encontro_atual.nome = encontro.nome


def buscar_encontro_por_id(_id: int, paroquia: int):
    return encontroDao.buscar_por_id(_id, paroquia)


def buscar_eventos_por_encontro(id_encontro):
    return encontroDao.buscar_eventos_por_encontro(id_encontro)


def buscar_evento_por_id(id_evento):
    return encontroDao.buscar_evento_por_id(id_evento)
