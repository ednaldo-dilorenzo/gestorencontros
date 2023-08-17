from app.extensoes import db
from app.model import Casal, Pessoa
from sqlalchemy import or_


def criar_pessoa(pessoa: Pessoa):
    db.session.add(pessoa)


def criar_casal(casal: Casal):
    db.session.add(casal)


def buscar_casais(id_paroquia: int, page: int = 1, per_page: int = 10):
    return (
        db.session.query(Casal)
        .filter(Casal.id_paroquia == id_paroquia)
        .order_by(Casal.id)
        .paginate(page=page, per_page=per_page)
    )


def buscar_por_filtro(filtro: str, id_paroquia: int, page: int = 1, per_page: int = 10):
    busca = "%{}%".format(filtro)
    result = (
        db.session.query(Casal)
        .filter(Casal.id_paroquia == id_paroquia, Casal.extenso.like(busca))
        .order_by(Casal.id)
        .paginate(page=page, per_page=per_page)
    )
    return result


def buscar_casal_por_id(id_casal: int, id_paroquia: int) -> Casal:
    return (
        db.session.query(Casal)
        .filter(Casal.id_paroquia == id_paroquia, Casal.id == id_casal)
        .first()
    )


def buscar_por_filtro_nao_inscrito(
    filtro: str, id_paroquia: int, id_encontro: int
) -> list:
    busca = "%{}%".format(filtro)
    return (
        db.session.query(Casal)
        .filter(
            Casal.id_paroquia == id_paroquia,
            Casal.extenso.like(busca),
            or_(Casal.id_inscrito != id_encontro, Casal.id_inscrito == None),
        )
        .order_by(Casal.id)
        .all()
    )
