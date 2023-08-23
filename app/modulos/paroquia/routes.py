from flask import Blueprint, render_template


paroquia_bp = Blueprint("paroquia", __name__, url_prefix="/paroquias")


@paroquia_bp.route("/")
def index():
    return render_template("paroquia/index.html")
