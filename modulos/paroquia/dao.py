class Paroquia:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome


paroquias = {
    Paroquia(1, "Nossa Senhora das Neves"),
    Paroquia(2, "Nossa Senhora de Fátima"),
}


def buscar_todas_paroquias():
    return paroquias
