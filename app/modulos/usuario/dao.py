from app.extensoes import db
from app.model import Usuario


def buscar_por_paroquia(id_paroquia: int, page: int = 1, per_page: int = 10):
    return (
        db.session.query(Usuario)
        .filter(Usuario.id_paroquia == id_paroquia)
        .paginate(page=page, per_page=per_page)
    )


def criar_usuario(usuario):
    db.session.add(usuario)


def buscar_por_id_e_paroquia(id_usuario: int, id_paroquia: int) -> Usuario:
    return (
        db.session.query(Usuario)
        .filter(Usuario.id == id_usuario, Usuario.id_paroquia == id_paroquia)
        .first()
    )
