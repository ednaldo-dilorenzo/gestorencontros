import operator
from .usuario import Usuario

usuarios = [
    Usuario(
        1,
        "master@root.com",
        "pbkdf2:sha256:260000$ZY3WbE5SLhCOaHY8$d1d86ce45e3e54646e3d7e2a4fbcb5939e128ff6c7d5b688098b2f0760a55adb",
        "Ednaldo",
        "892382783972",
        "ADMIN",
        None,
    ),
    Usuario(
        4,
        "ast@test.com",
        "pbkdf2:sha256:260000$1JXmVblo8se6jlJT$8db0fb61f3231541931b2a3137f75655d3a14e4d679b4391ca83a300765fe4e1",
        "Atrogildo",
        "89a878378411",
        "DIRIGENTE",
        1,
    ),
    Usuario(
        2,
        "ju@test.com",
        "pbkdf2:sha256:260000$1JXmVblo8se6jlJT$8db0fb61f3231541931b2a3137f75655d3a14e4d679b4391ca83a300765fe4e1",
        "Juliana",
        "009289189281",
        "DIRIGENTE",
        1,
    ),
    Usuario(
        3,
        "be@test.com",
        "pbkdf2:sha256:260000$1JXmVblo8se6jlJT$8db0fb61f3231541931b2a3137f75655d3a14e4d679b4391ca83a300765fe4e1",
        "Bernardo",
        "6565434453534",
        "DIRIGENTE",
        2,
    ),
]


def buscar_admin_pelo_login(login: str) -> Usuario:
    try:
        return next(
            filter(
                lambda usuario: usuario.username == login and usuario.papel == "ADMIN",
                usuarios,
            )
        )
    except StopIteration:
        return None


def buscar_usuario_pelo_login_e_paroquia(login: str, paroquia: int) -> Usuario:
    try:
        return next(
            filter(
                lambda usuario: usuario.username == login
                and usuario.paroquia == paroquia,
                usuarios,
            )
        )
    except StopIteration:
        return None


def buscar_usuario_por_id(id: int) -> Usuario:
    try:
        return next(filter(lambda usuario: usuario.id == id, usuarios))
    except StopIteration:
        return None


def buscar_todos() -> list:
    return sorted(usuarios, key=operator.attrgetter("id"))


def salvar(usuario: Usuario) -> Usuario:
    ultimo_usuario = max(usuarios, key=operator.attrgetter("id"))
    usuario.id = ultimo_usuario.id + 1
    usuarios.append(usuario)
    return usuario


def atualizar(usuario_id: int, usuario: Usuario) -> Usuario:
    index = next(i for i, x in enumerate(usuarios) if x.id == usuario_id)
    usuarios[index] = usuario
    return usuario
