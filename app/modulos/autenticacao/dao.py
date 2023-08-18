from app.extensoes import db
from app.model import Usuario


def buscar_admin_pelo_login(login: str) -> Usuario:
    usuario = (
        db.session.query(Usuario)
        .filter(Usuario.username == login, Usuario.papel == "ADMIN")
        .first()
    )
    return usuario


def buscar_usuario_pelo_login_e_paroquia(login: str, paroquia: int) -> Usuario:
    usuario = db.execute(db.select(Usuario).where(Usuario.username == login)).first()
    return usuario


def buscar_usuario_por_id(id: int) -> Usuario:
    usuario = db.session.query(Usuario).filter(Usuario.id == id).first()
    return usuario


def buscar_todos() -> list:
    return db.session.execute(db.select(Usuario).order_by(Usuario.username)).scalars()


def salvar(usuario: Usuario) -> Usuario:
    db.session.add(usuario)
    db.session.commit()
    return usuario


def atualizar(usuario_id: int, usuario: Usuario) -> Usuario:
    return None
