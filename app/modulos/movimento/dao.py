from app.extensoes import db
from app.model import Movimento, Equipe, Encontro, Circulo


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


def salvar_encontro(encontro: Encontro) -> Encontro:
    db.session.add(encontro)
    db.session.flush()
    return encontro


def atualizar(valor):
    pass


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


def buscar_encontros_por_movimento(id_movimento):
    return (
        db.session.query(Encontro)
        .filter(Encontro.id_movimento == id_movimento)
        .order_by(Encontro.ano.desc())
        .all()
    )


def buscar_encontro_por_id(id_movimento: int, id_encontro: int) -> Encontro:
    return (
        db.session.query(Encontro)
        .filter(Encontro.id_movimento == id_movimento, Encontro.id == id_encontro)
        .first()
    )


def buscar_circulos_por_encontro(id_encontro: int) -> list:
    return db.session.query(Circulo).filter(Circulo.id_encontro == id_encontro).all()


def salvar_circulo(circulo: Circulo):
    db.session.add(circulo)


def buscar_circulo_por_id_e_encontro(id_circulo: int, id_encontro: int) -> Circulo:
    return (
        db.session.query(Circulo)
        .filter(Circulo.id_encontro == id_encontro, Circulo.id == id_circulo)
        .first()
    )
