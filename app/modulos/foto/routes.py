from flask import Blueprint, send_from_directory
from app.util.file_handler import pegar_caminho_uploads
from flask_login import login_required
from flask import current_app, request
import os


foto_bp = Blueprint("foto", __name__, url_prefix="/foto")


@foto_bp.route("/")
@login_required
def foto():
    id_pessoa = request.args.get("id_pessoa")
    tipo = request.args.get("tipo")
    if id_pessoa and os.path.exists(
        os.path.join(pegar_caminho_uploads(), f"{id_pessoa}_pessoa.jpg")
    ):
        return send_from_directory(pegar_caminho_uploads(), f"{id_pessoa}_pessoa.jpg")

    nome_arquivo = "anonima.jpg" if tipo and tipo == "f" else "anonimo.jpg"
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], nome_arquivo)
