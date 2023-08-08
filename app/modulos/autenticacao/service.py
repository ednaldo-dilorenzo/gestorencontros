from werkzeug.security import check_password_hash
from app.modulos.autenticacao import dao as auth_dao
from app.modulos.autenticacao.model import Usuario


def valida_usuario(login: str, senha: str, paroquia: int = None) -> Usuario:
    usuario = None

    if paroquia:
        usuario = auth_dao.buscar_usuario_pelo_login_e_paroquia(login, paroquia)
    else:
        usuario = auth_dao.buscar_admin_pelo_login(login)

    return usuario if usuario and check_password_hash(usuario.senha, senha) else None


def buscar_por_id(id: int) -> Usuario:
    return auth_dao.buscar_usuario_por_id(id)


def buscar_todos_alunos() -> list:
    return auth_dao.buscar_todos()


def salvar_aluno(usuario: Usuario) -> bool:
    aluno = None

    if aluno:
        raise KeyError("Aluno já cadastrado")

    usuario.papel = "ALUNO"
    return auth_dao.salvar(usuario)


def atualizar_aluno(id: int, usuario: Usuario) -> bool:
    usuario.papel = "ALUNO"
    return auth_dao.atualizar(id, usuario)
