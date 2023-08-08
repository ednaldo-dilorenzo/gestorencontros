from app.extensoes import db
from app.model.paroquia import Paroquia


def buscar_todas_paroquias():
    return db.session.query(Paroquia).all()
