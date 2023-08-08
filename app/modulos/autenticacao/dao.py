from app.extensoes import db
from app.modulos.autenticacao.model import Usuario

# usuarios = [
#     Usuario(
#         1,
#         "master@root.com",
#         "pbkdf2:sha256:260000$ZY3WbE5SLhCOaHY8$d1d86ce45e3e54646e3d7e2a4fbcb5939e128ff6c7d5b688098b2f0760a55adb",
#         "Ednaldo",
#         "892382783972",
#         "ADMIN",
#         None,
#     ),
#     Usuario(
#         4,
#         "ast@test.com",
#         "pbkdf2:sha256:260000$1JXmVblo8se6jlJT$8db0fb61f3231541931b2a3137f75655d3a14e4d679b4391ca83a300765fe4e1",
#         "Atrogildo",
#         "89a878378411",
#         "DIRIGENTE",
#         1,
#     ),
#     Usuario(
#         2,
#         "ju@test.com",
#         "pbkdf2:sha256:260000$1JXmVblo8se6jlJT$8db0fb61f3231541931b2a3137f75655d3a14e4d679b4391ca83a300765fe4e1",
#         "Juliana",
#         "009289189281",
#         "DIRIGENTE",
#         1,
#     ),
#     Usuario(
#         3,
#         "be@test.com",
#         "pbkdf2:sha256:260000$1JXmVblo8se6jlJT$8db0fb61f3231541931b2a3137f75655d3a14e4d679b4391ca83a300765fe4e1",
#         "Bernardo",
#         "6565434453534",
#         "DIRIGENTE",
#         2,
#     ),
# ]


def buscar_admin_pelo_login(login: str) -> Usuario:
    usuario = db.session.query(Usuario).filter(Usuario.username == login).first()
    return usuario


def buscar_usuario_pelo_login_e_paroquia(login: str, paroquia: int) -> Usuario:
    usuario = db.execute(db.select(Usuario).where(Usuario.username == login)).first()
    return usuario


def buscar_usuario_por_id(id: int) -> Usuario:
    usuario = db.execute(db.select(Usuario).where(Usuario.id == id)).first()
    return usuario


def buscar_todos() -> list:
    return db.session.execute(db.select(Usuario).order_by(Usuario.username)).scalars()


def salvar(usuario: Usuario) -> Usuario:
    db.session.add(usuario)
    db.session.commit()
    return usuario


def atualizar(usuario_id: int, usuario: Usuario) -> Usuario:
    return None
