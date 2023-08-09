from app.extensoes import db
from app.model import Casal


def criar_pessoa(pessoa):
    pass


def criar_casal(casal):
    pass


def buscar_casais(id_paroquia: int):
    return db.session.query(Casal).filter(Casal.id_paroquia == id_paroquia).all()


def buscar_por_filtro(
    filtro: str, id_paroquia: int, page: int = 1, per_page: int = 10
):
    busca = "%{}%".format(filtro)
    result = (
        db.session.query(Casal)
        .filter(Casal.id_paroquia == id_paroquia, Casal.extenso.like(busca))
        .paginate(page=page, per_page=per_page)
    )
    return result


def buscar_casal_por_id(id_casal: int):
    return None
