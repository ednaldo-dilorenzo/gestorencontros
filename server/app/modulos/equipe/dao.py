from app.model import EquipeEncontro, EquipeEncontroCasal
from app.extensoes import db
from sqlalchemy.orm import joinedload


def buscar_equipes_por_encontro(id_encontro: int) -> list:
    return (
        db.session.query(EquipeEncontro)
        .options(joinedload(EquipeEncontro.equipe))
        .filter(EquipeEncontro.id_encontro == id_encontro)
        .all()
    )


def buscar_equipe_encontro_casal_por_encontro_e_equipe(
    id_encontro: int, id_equipe: int
) -> list:
    return (
        db.session.query(EquipeEncontroCasal)
        .options(joinedload(EquipeEncontroCasal.casal))
        .filter(
            EquipeEncontroCasal.id_encontro == id_encontro,
            EquipeEncontroCasal.id_equipe == id_equipe,
        )
        .order_by(EquipeEncontroCasal.coordenador.desc(), EquipeEncontroCasal.aceito.desc())
        .all()
    )
