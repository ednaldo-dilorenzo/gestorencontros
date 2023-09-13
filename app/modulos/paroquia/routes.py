from flask import Blueprint
from flask_login import login_required
from app.util.security import permission
from app.util.constants import Roles
from app.modulos.paroquia import service as paroquia_service


paroquia_bp = Blueprint("paroquia", __name__, url_prefix="/paroquias")


@paroquia_bp.route("/")
@login_required
@permission([Roles.ROLE_ADMIN])
def buscar_todas():
    paroquias = paroquia_service.buscar_paroquias()

    return [{"id": paroquia.id, "nome": paroquia.nome} for paroquia in paroquias]
