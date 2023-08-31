from app.extensoes import db
from app.model import Equipe, EquipeEncontro


def buscar_equipes_por_movimento(id_movimento: int) -> list:
    return db.session.query(Equipe).filter(Equipe.id_movimento == id_movimento).all()


def adicionar_equipe_encontro(equipe_encontro: EquipeEncontro):
    db.session.add(equipe_encontro)
