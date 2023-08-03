class Encontro:
    def __init__(self, id, nome, paroquia):
        self.id = id
        self.nome = nome
        self.paroquia = paroquia


class Evento:
    def __init__(self, id, nome, ano, tema, data_inicio, data_fim, encontro, paroquia):
        self.id = id
        self.nome = nome
        self.ano = ano
        self.tema = tema
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.encontro = encontro
        self.paroquia = paroquia


encontros = [
    Encontro(1, "Encontro de Casais com Cristo", 1),
    Encontro(2, "Encontro de Jovens com Cristo", 1),
    Encontro(3, "Segue-me I", 1),
    Encontro(4, "Segue-me II", 1),
    Encontro(1, "Encontro de Casais com Cristo", 2),
    Encontro(2, "Encontro de Jovens com Cristo", 2),
]


eventos = [
    Evento(1, "XXXVI ECC Neves", 2016, "Tu és meu", "2016-09-24", "2016-09-26", 1, 1),
    Evento(
        2,
        "XXXVII ECC Neves",
        2018,
        "Minha família vossa é",
        "2018-09-24",
        "2018-09-26",
        1,
        1,
    ),
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


def buscar_por_id(_id: int, paroquia: int) -> Encontro:
    try:
        return next(
            filter(
                lambda encontro: encontro.paroquia == paroquia and encontro.id == _id,
                encontros,
            )
        )
    except StopIteration:
        return None


def salvar(encontro):
    encontros.append(encontro)


def salvar_evento(evento: Evento):
    eventos.append(evento)


def atualizar(valor):
    encontro_atual = next(
        filter(
            lambda encontro: encontro.paroquia == valor.paroquia
            and encontro.id == valor.id,
            encontros,
        )
    )

    encontro_atual.nome = valor.nome

    return encontro_atual


def buscar_eventos_por_encontro(id_encontro):
    try:
        return list(
            filter(
                lambda evento: evento.encontro == id_encontro,
                eventos,
            )
        )
    except StopIteration:
        return None
