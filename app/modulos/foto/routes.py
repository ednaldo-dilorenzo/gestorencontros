from flask import Blueprint, send_file
from app.util.file_handler import retornar_foto_pessoa
from flask_login import login_required
from flask import request


foto_bp = Blueprint("foto", __name__, url_prefix="/foto")


@foto_bp.route("/")
@login_required
def foto():
    id_pessoa = request.args.get("id_pessoa", type=int)
    tipo = request.args.get("tipo")
    return send_file(
        retornar_foto_pessoa(id_pessoa, tipo and tipo == "f"), download_name="foto.jpg"
    )
