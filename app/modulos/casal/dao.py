class Pessoa:
    def __init__(self, id, nome, data_nascimento, email, paroquia):
        self.id = id
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.email = email
        self.paroquia = paroquia


class Casal:
    def __init__(self, id, esposo, esposa, paroquia):
        self.id = id
        self.esposo = esposo
        self.esposa = esposa
        self.paroquia = paroquia


pessoas = [
    Pessoa(1, "Ednaldo Dilorenzo de Souza Filho", "21/04/1982", "ed@test.com", 1),
    Pessoa(2, "Juliana de Castro Farias Dilorenzo", "26/09/1980", "ju@test.com", 1),
    Pessoa(3, "Rafael Moraes", "21/04/1982", "ra@test.com", 1),
    Pessoa(4, "Rafaela Moraes", "26/09/1980", "rafa@test.com", 1),
]


casais = [
    Casal(
        1,
        pessoas[0],
        pessoas[1],
        1,
    ),
    Casal(
        2,
        pessoas[2],
        pessoas[3],
        1,
    ),
]


def criar_pessoa(pessoa):
    pessoas.append(pessoa)


def criar_casal(casal):
    casais.append(casal)


def buscar_casais(id_paroquia: int):
    return list(filter(lambda casal: casal.paroquia == id_paroquia, casais))


def buscar_casal_por_id(id_casal: int):
    try:
        return next(filter(lambda casal: casal.id == id_casal, casais))
    except StopIteration:
        return None
