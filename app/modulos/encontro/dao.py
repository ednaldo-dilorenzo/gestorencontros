from app.extensoes import db
from app.model import EquipeEncontro


def buscar_equipe_encontro_por_encontro(
    id_encontro: int, id_equipe: int
) -> EquipeEncontro:
    return (
        db.session.query(EquipeEncontro)
        .filter(
            EquipeEncontro.id_encontro == id_encontro,
            EquipeEncontro.id_equipe == id_equipe,
        )
        .first()
    )


def buscar_equipe_casal_coordena(id_coordenador: int, id_encontro: int) -> EquipeEncontro:
    return (
        db.session.query(EquipeEncontro)
        .filter(
            EquipeEncontro.id_coordenador == id_coordenador,
            EquipeEncontro.id_encontro == id_encontro,
        )
        .first()
    )
