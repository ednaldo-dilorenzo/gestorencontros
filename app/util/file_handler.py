import os
from werkzeug.utils import secure_filename


def salvar_imagem(arquivo=None, caminho_arquivo="", nome_arquivo="default.png"):
    if arquivo:
        nome = secure_filename(nome_arquivo)
        arquivo.save(os.path.join(caminho_arquivo, nome))


def pegar_caminho_uploads():
    return "/home/edsf/Imagens"
