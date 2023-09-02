from app.model import EquipeEncontro
from app.extensoes import db
from sqlalchemy.orm import joinedload


def buscar_equipes_por_encontro(id_encontro: int) -> list:
    return (
        db.session.query(EquipeEncontro)
        .options(joinedload(EquipeEncontro.equipe))
        .options(joinedload(EquipeEncontro.coordenador))
        .filter(EquipeEncontro.id_encontro == id_encontro)
        .all()
    )
