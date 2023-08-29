from app.extensoes import db
from app.model import Casal, Pessoa
from sqlalchemy import or_
from typing import Optional


def criar_pessoa(pessoa: Pessoa) -> Pessoa:
    db.session.add(pessoa)
    return pessoa


def criar_casal(casal: Casal) -> Casal:
    db.session.add(casal)
    return casal


def buscar_casais(
    id_paroquia: int,
    page: int = 1,
    per_page: int = 10,
    id_inscrito: Optional[int] = None,
):
    resultado = db.session.query(Casal).filter(Casal.id_paroquia == id_paroquia)

    if id_inscrito:
        resultado = resultado.filter(Casal.id_inscrito == id_inscrito)

    return resultado.order_by(Casal.id).paginate(page=page, per_page=per_page)


def buscar_por_filtro(
    filtro: str,
    id_paroquia: int,
    page: int = 1,
    per_page: int = 10,
    id_inscrito: Optional[int] = None,
):
    busca = "%{}%".format(filtro)
    resultado = db.session.query(Casal).filter(
        Casal.id_paroquia == id_paroquia, Casal.extenso.like(busca)
    )

    if id_inscrito:
        resultado = resultado.filter(Casal.id_inscrito == id_inscrito)

    return resultado.order_by(Casal.id).paginate(page=page, per_page=per_page)


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


def buscar_casais_inscritos_sem_circulo(id_encontro: int) -> list:
    return (
        db.session.query(Casal)
        .filter(Casal.id_inscrito == id_encontro, Casal.id_circulo == None)
        .all()
    )


def buscar_casais_inscritos_no_circulo(id_encontro: int, id_circulo: int) -> list:
    return (
        db.session.query(Casal)
        .filter(Casal.id_inscrito == id_encontro, Casal.id_circulo == id_circulo)
        .all()
    )


def buscar_por_filtro_test(
    filtro: str,
    id_paroquia: int,
    id_encontro: Optional[int] = None,
    inscrito: Optional[bool] = True,
    id_circulo: Optional[int] = None,
) -> list:
    resultado = db.session.query(Casal).filter(
        Casal.id_paroquia == id_paroquia,
    )

    if not filtro is None:
        if filtro:
            busca = "%{}%".format(filtro)
            resultado = resultado.filter(Casal.extenso.like(busca))
        else:
            return []

    if id_circulo:
        resultado = resultado.filter(Casal.id_circulo == id_circulo)

    if id_encontro:
        if inscrito:
            resultado = resultado.filter(Casal.id_inscrito == id_encontro)
        else:
            resultado = resultado.filter(
                or_(Casal.id_inscrito != id_encontro, Casal.id_inscrito == None)
            )

    return resultado.order_by(Casal.id).all()
