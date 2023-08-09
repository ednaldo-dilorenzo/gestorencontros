import app.modulos.casal.dao as casal_dao


def buscar_todos(paroquia: int):
    return casal_dao.buscar_casais(paroquia)


def buscar_por_filtro(filtro: str, id_paroquia: int):
    resultado = casal_dao.buscar_por_filtro(filtro, id_paroquia)
    return resultado


def salvar(casal):
    casal_dao.criar_pessoa(casal.esposo)
    casal_dao.criar_pessoa(casal.esposa)
    casal_dao.criar_casal(casal)
