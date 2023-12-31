import app.modulos.usuario.dao as usuario_dao
from app.extensoes import transactional
from app.model import Usuario
from app.util.constants import Roles
from werkzeug.security import generate_password_hash


def buscar_por_paroquia(id_paroquia: int, page: int = 1, per_page: int = 10):
    return usuario_dao.buscar_por_paroquia(id_paroquia, page, per_page)


def buscar_todos(page: int = 1, per_page: int = 10):
    return usuario_dao.buscar_todos(page, per_page)


def buscar_por_id_e_paroquia(id_usuario: int, id_paroquia: int) -> Usuario:
    return usuario_dao.buscar_por_id_e_paroquia(id_usuario, id_paroquia)


def buscar_por_id(id_usuario: int) -> Usuario:
    return usuario_dao.buscar_por_id(id_usuario)


@transactional
def salvar(usuario: Usuario):
    usuario.papel = Roles.ROLE_DIRIGENTE
    usuario.senha = generate_password_hash(usuario.senha)
    usuario_dao.criar_usuario(usuario)


@transactional
def editar(usuario_atual: Usuario, usuario_alterado: Usuario):
    usuario_atual.ativo = usuario_alterado.ativo
    usuario_atual.nome = usuario_alterado.nome
    usuario_atual.username = usuario_alterado.username
    usuario_atual.id_paroquia = usuario_alterado.id_paroquia
    if usuario_alterado.senha:
        usuario_atual.senha = generate_password_hash(usuario_alterado.senha)


@transactional
def mudar_senha(id_usuario: int, nova_senha):
    usuario = usuario_dao.buscar_por_id(id_usuario)

    if not usuario:
        raise KeyError("Usuário não encontrado")

    usuario.senha = generate_password_hash(nova_senha)
