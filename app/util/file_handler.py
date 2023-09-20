import os
from instance import config
from werkzeug.utils import secure_filename
import os


def salvar_imagem(arquivo=None, nome_arquivo="default.png"):
    caminho_arquivo = config.UPLOAD_FOLDER
    if arquivo:
        nome = secure_filename(nome_arquivo)
        arquivo.save(os.path.join(caminho_arquivo, nome))


def salvar_foto_pessoa(id_pessoa: int):
    pass


def retornar_foto_pessoa(id_pessoa: int, feminino: bool = False):
    nome_arquivo = f"{id_pessoa}_pessoa.jpg"
    if not id_pessoa or not os.path.exists(
        os.path.join(config.UPLOAD_FOLDER, nome_arquivo)
    ):
        nome_arquivo = "anonima.jpg" if feminino else "anonimo.jpg"

    return open(f"{config.UPLOAD_FOLDER}/{nome_arquivo}", "rb")


def pegar_caminho_uploads():
    return config.UPLOAD_FOLDER
