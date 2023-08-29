import app.modulos.casal.dao as casal_dao
from app.model import Casal
from app.extensoes import transactional
from typing import Optional


def buscar_todos(
    paroquia: int,
    page: int = 1,
    per_page: int = 10,
    id_inscrito: Optional[int] = None,
):
    return casal_dao.buscar_casais(paroquia, page, per_page, id_inscrito)


def buscar_por_filtro(filtro: str, id_paroquia: int, id_inscrito: Optional[int]=None):
    resultado = casal_dao.buscar_por_filtro(filtro.lower(), id_paroquia, id_inscrito=id_inscrito)
    return resultado


def buscar_por_id(id_casal: int, id_paroquia: int) -> Casal:
    return casal_dao.buscar_casal_por_id(id_casal, id_paroquia)


@transactional
def salvar(casal):
    casal.esposo = casal_dao.criar_pessoa(casal.esposo)
    casal.esposa = casal_dao.criar_pessoa(casal.esposa)
    casal.extenso = f"{casal.esposo.nome} {casal.esposo.apelido} {casal.esposa.nome} {casal.esposa.apelido}".lower()
    casal = casal_dao.criar_casal(casal)
    return casal


@transactional
def atualizar_casal(casal, casal_atualizado):
    atualizar_pessoa(casal.esposo, casal_atualizado.esposo)
    atualizar_pessoa(casal.esposa, casal_atualizado.esposa)
    casal.id_circulo = casal_atualizado.id_circulo
    casal.extenso = f"{casal.esposo.nome} {casal.esposa.nome}".lower()


def atualizar_pessoa(pessoa, pessoa_atualizada):
    if pessoa_atualizada.nome:
        pessoa.nome = pessoa_atualizada.nome
    if pessoa_atualizada.email:
        pessoa.email = pessoa_atualizada.email
    if pessoa_atualizada.telefone:
        pessoa.telefone = pessoa_atualizada.telefone


def buscar_casais_inscritos_sem_circulo(id_encontro: int) -> list:
    return casal_dao.buscar_casais_inscritos_sem_circulo(id_encontro)


def buscar_casais_inscritos_no_circulo(id_encontro, id_circulo) -> list:
    return casal_dao.buscar_casais_inscritos_no_circulo(id_encontro, id_circulo)


def buscar_por_filtro_nao_inscrito(
    filtro: str, id_paroquia: int, id_encontro: int
) -> list:
    return casal_dao.buscar_por_filtro_nao_inscrito(filtro, id_paroquia, id_encontro)


def buscar_por_filtro_test(
    filtro: str,
    id_paroquia: int,
    id_encontro: Optional[int] = None,
    inscrito: Optional[bool] = True,
    id_circulo: Optional[int] = None,
) -> list:
    return casal_dao.buscar_por_filtro_test(
        filtro, id_paroquia, id_encontro, inscrito, id_circulo
    )
