from app.model import Encontro, EquipeEncontro
import app.modulos.movimento.dao as encontro_dao
import app.modulos.movimento.equipe.dao as equipe_dao
from app.extensoes import transactional


def buscar_encontros(paroquia: int):
    return encontro_dao.buscar_por_paroquia(paroquia)


@transactional
def criar_movimento(movimento):
    encontro_dao.salvar(movimento)

@transactional
def atualizar_movimento(movimento_atual, movimento_alterado):
    movimento_atual.nome = movimento_alterado.nome


@transactional
def criar_encontro(encontro: Encontro):
    equipes_movimento = equipe_dao.buscar_equipes_por_movimento(encontro.id_movimento)

    novo_encontro = encontro_dao.salvar_encontro(encontro)

    for equipe in equipes_movimento:
        equipe_encontro = EquipeEncontro()
        equipe_encontro.id_encontro = novo_encontro.id
        equipe_encontro.id_equipe = equipe.id
        equipe_dao.adicionar_equipe_encontro(equipe_encontro)


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


def buscar_circulo_por_id_e_encontro(id_circulo: int, id_encontro: int):
    return encontro_dao.buscar_circulo_por_id_e_encontro(id_circulo, id_encontro)


@transactional
def atualizar_circulo(circulo_atual, circulo_alterado):
    circulo_atual.nome = circulo_alterado.nome
    circulo_atual.cor = circulo_alterado.cor
    circulo_atual.id_coordenador = circulo_alterado.id_coordenador


def buscar_casais_inscritos_sem_circulo(id_encontro: int) -> list:
    pass
