import app.modulos.movimento.dao as encontro_dao
from app.extensoes import transactional


def buscar_encontros(paroquia: int):
    return encontro_dao.buscar_por_paroquia(paroquia)


@transactional
def atualizar_movimento(movimento_atual, movimento_alterado):
    movimento_atual.nome = movimento_alterado.nome


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


@transactional
def atualizar_encontro(encontro_atual, encontro_alterado):
    encontro_atual.nome = encontro_alterado.nome
    encontro_atual.tema = encontro_alterado.tema
    encontro_atual.ano = encontro_alterado.ano
    encontro_atual.data_inicio = encontro_alterado.data_inicio
    encontro_atual.data_termino = encontro_alterado.data_termino


def buscar_movimento_por_id(_id: int, paroquia: int):
    return encontro_dao.buscar_por_id(_id, paroquia)


def buscar_encontros_por_movimento(id_movimento):
    return encontro_dao.buscar_encontros_por_movimento(id_movimento)


def buscar_encontro_por_id(id_movimento, id_encontro):
    return encontro_dao.buscar_encontro_por_id(id_movimento, id_encontro)


def buscar_circulos_por_encontro(id_encontro: int) -> list:
    return encontro_dao.buscar_circulos_por_encontro(id_encontro)


@transactional
def criar_circulo(circulo):
    encontro_dao.salvar_circulo(circulo)