import app.modulos.casal.dao as casal_dao
from app.model import Casal
from app.extensoes import transactional
from app.config import current_config, BASEDIR
from typing import Optional


def buscar_todos(
    paroquia: int,
    page: int = 1,
    per_page: int = 10,
    id_inscrito: Optional[int] = None,
):
    return casal_dao.buscar_casais(paroquia, page, per_page, id_inscrito)


def buscar_por_filtro(filtro: str, id_paroquia: int, id_inscrito: Optional[int] = None):
    resultado = casal_dao.buscar_por_filtro(
        filtro.lower(), id_paroquia, id_inscrito=id_inscrito
    )
    return resultado


def buscar_por_id(id_casal: int, id_paroquia: int) -> Casal:
    return casal_dao.buscar_casal_por_id(id_casal, id_paroquia)


@transactional
def salvar(casal, foto_esposo=None, foto_esposa=None):
    casal.esposo = casal_dao.criar_pessoa(casal.esposo)
    casal.esposa = casal_dao.criar_pessoa(casal.esposa)
    casal.extenso = f"{casal.esposo.nome} {casal.esposo.apelido} {casal.esposa.nome} {casal.esposa.apelido}".lower()
    casal = casal_dao.criar_casal(casal)
    if foto_esposo:
        current_config.file_handler.save(foto_esposo, f"{casal.esposo.id}_pessoa.jpg")
    if foto_esposa:
        current_config.file_handler.save(foto_esposa, f"{casal.esposa.id}_pessoa.jpg")
    return casal


@transactional
def atualizar_casal(casal, casal_atualizado, foto_esposo=None, foto_esposa=None):
    atualizar_pessoa(casal.esposo, casal_atualizado.esposo)
    atualizar_pessoa(casal.esposa, casal_atualizado.esposa)
    casal.id_circulo = casal_atualizado.id_circulo
    casal.extenso = f"{casal.esposo.nome} {casal.esposa.nome}".lower()
    if foto_esposo:
        current_config.file_handler.save(foto_esposo, f"{casal.esposo.id}_pessoa.jpg")
    if foto_esposa:
        current_config.file_handler.save(foto_esposa, f"{casal.esposa.id}_pessoa.jpg")


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
    id_equipe: Optional[int] = None,
) -> list:
    return casal_dao.buscar_por_filtro_test(
        filtro, id_paroquia, id_encontro, inscrito, id_circulo, id_equipe
    )


def buscar_casais_por_equipe_e_encontro(id_encontro: int, id_equipe: int) -> list:
    return casal_dao.buscar_casais_por_equipe_e_encontro(id_encontro, id_equipe)


def retornar_foto_pessoa(id_pessoa: int, feminino: bool = False):
    nome_arquivo = f"{id_pessoa}_pessoa.jpg"

    if not current_config.file_handler.file_exists(nome_arquivo):
        return open(
            f"{BASEDIR}/static/img/{'anonima.jpg' if feminino else 'anonimo.jpg'}", "rb"
        )

    return current_config.file_handler.read(nome_arquivo)
