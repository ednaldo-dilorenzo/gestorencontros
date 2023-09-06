from app.extensoes import db
from app.model import EquipeEncontro, EquipeEncontroCasal


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


def buscar_equipe_casal_coordena(
    id_coordenador: int, id_encontro: int
) -> EquipeEncontro:
    return (
        db.session.query(EquipeEncontro)
        .filter(
            EquipeEncontro.id_coordenador == id_coordenador,
            EquipeEncontro.id_encontro == id_encontro,
        )
        .first()
    )


def adicionar_equipe_encontro_casal(equipe_econtro_casal: EquipeEncontroCasal):
    db.session.add(equipe_econtro_casal)


def remover_equipe_encontro_casal(equipe_econtro_casal: EquipeEncontroCasal):
    db.session.delete(equipe_econtro_casal)


def buscar_equipe_encontro_casal(
    id_equipe: int, id_encontro: int, id_casal: int
) -> EquipeEncontroCasal:
    return (
        db.session.query(EquipeEncontroCasal)
        .filter(
            EquipeEncontroCasal.id_casal == id_casal,
            EquipeEncontroCasal.id_encontro == id_encontro,
            EquipeEncontroCasal.id_equipe == id_equipe,
        )
        .first()
    )
