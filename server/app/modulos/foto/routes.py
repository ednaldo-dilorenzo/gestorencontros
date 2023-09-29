from flask import Blueprint, send_file
from flask_login import login_required
from flask import request
from app.modulos.casal.service import retornar_foto_pessoa


foto_bp = Blueprint("foto", __name__, url_prefix="/foto")


@foto_bp.route("/")
@login_required
def foto():
    id_pessoa = request.args.get("id_pessoa", type=int)
    tipo = request.args.get("tipo")
    return send_file(
        retornar_foto_pessoa(id_pessoa, tipo and tipo == "f"), download_name="foto.jpg"
    )
