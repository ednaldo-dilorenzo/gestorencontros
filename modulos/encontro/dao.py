class Encontro:
    
    def __init__(self, id, nome, paroquia):
        self.id = id
        self.nome = nome
        self.paroquia = paroquia


encontros = [
    Encontro(1, "Encontro de Casais com Cristo", 1),
    Encontro(2, "Encontro de Jovens com Cristo", 1),
    Encontro(3, "Segue-me I", 1),
    Encontro(4, "Segue-me II", 1),
    Encontro(1, "Encontro de Casais com Cristo", 2),
    Encontro(2, "Encontro de Jovens com Cristo", 2),
]


def buscar_por_paroquia(paroquia: int):
    try:
        return list(
            filter(
                lambda encontro: encontro.paroquia == paroquia,
                encontros,
            )
        )
    except StopIteration:
        return None
    
def salvar(encontro):
    encontros.append(encontro)
