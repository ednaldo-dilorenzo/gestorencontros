import modulos.encontro.dao as encontroDao


def buscar_encontros(paroquia: int):
    return encontroDao.buscar_por_paroquia(paroquia)


def criar_encontro(encontro):
    encontroDao.salvar(encontro)


def criar_evento(evento):
    encontroDao.salvar_evento(evento)


def atualizar_encontro(encontro):
    encontroDao.atualizar(encontro)


def buscar_encontro_por_id(_id: int, paroquia: int):
    return encontroDao.buscar_por_id(_id, paroquia)


def buscar_eventos_por_encontro(id_encontro):
    return encontroDao.buscar_eventos_por_encontro(id_encontro)
