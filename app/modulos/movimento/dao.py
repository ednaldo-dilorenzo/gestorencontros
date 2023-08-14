from app.extensoes import db
from app.model import Movimento, Equipe


class Encontro:
    def __init__(self, id, nome, paroquia):
        self.id = id
        self.nome = nome
        self.paroquia = paroquia


class Evento:
    def __init__(self, id, nome, ano, tema, data_inicio, data_fim, encontro, paroquia):
        self.id = id
        self.nome = nome
        self.ano = ano
        self.tema = tema
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.encontro = encontro
        self.paroquia = paroquia


encontros = [
    Encontro(1, "Encontro de Casais com Cristo", 1),
    Encontro(2, "Encontro de Jovens com Cristo", 1),
    Encontro(3, "Segue-me I", 1),
    Encontro(4, "Segue-me II", 1),
    Encontro(1, "Encontro de Casais com Cristo", 2),
    Encontro(2, "Encontro de Jovens com Cristo", 2),
]


eventos = [
    Evento(1, "XXXVI ECC Neves", 2016, "Tu és meu", "2016-09-24", "2016-09-26", 1, 1),
    Evento(
        2,
        "XXXVII ECC Neves",
        2018,
        "Minha família vossa é",
        "2018-09-24",
        "2018-09-26",
        1,
        1,
    ),
]


def buscar_por_paroquia(id_paroquia: int):
    return (
        db.session.query(Movimento)
        .filter(Movimento.id_paroquia == id_paroquia)
        .order_by(Movimento.id)
        .all()
    )


def buscar_por_id(_id: int, id_paroquia: int) -> Encontro:
    return (
        db.session.query(Movimento)
        .filter(Movimento.id_paroquia == id_paroquia, Movimento.id == _id)
        .first()
    )


def salvar(movimento):
    db.session.add(movimento)


def salvar_evento(evento: Evento):
    eventos.append(evento)


def atualizar(valor):
    encontro_atual = next(
        filter(
            lambda encontro: encontro.paroquia == valor.paroquia
            and encontro.id == valor.id,
            encontros,
        )
    )

    encontro_atual.nome = valor.nome

    return encontro_atual


def buscar_equipes_por_movimento(id_movimento: int) -> list:
    return (
        db.session.query(Equipe)
        .filter(Equipe.id_movimento == id_movimento)
        .order_by(Equipe.nome)
        .all()
    )


def buscar_equipe_por_id_e_movimento(_id: int, id_movimento: int) -> Equipe:
    return (
        db.session.query(Equipe)
        .filter(Equipe.id == _id, Equipe.id_movimento == id_movimento)
        .first()
    )


def salvar_equipe(equipe: Equipe):
    db.session.add(equipe)


def buscar_eventos_por_encontro(id_encontro):
    try:
        return list(
            filter(
                lambda evento: evento.encontro == id_encontro,
                eventos,
            )
        )
    except StopIteration:
        return None


def buscar_evento_por_id(_id: int) -> Encontro:
    try:
        return next(
            filter(
                lambda evento: evento.id == _id,
                eventos,
            )
        )
    except StopIteration:
        return None
