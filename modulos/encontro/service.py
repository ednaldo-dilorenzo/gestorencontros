import modulos.encontro.dao as encontroDao


def buscar_encontros(paroquia: int):
    return encontroDao.buscar_por_paroquia(paroquia)

def criar_encontro(encontro):
    encontroDao.salvar(encontro)
