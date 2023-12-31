from app.extensoes import db
from flask_login import UserMixin
from flask_hashids import HashidMixin


class Paroquia(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String, unique=True, nullable=False)


class Usuario(db.Model, UserMixin, HashidMixin):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False)
    senha = db.Column(db.String, nullable=False)
    nome = db.Column(db.String, nullable=False)
    papel = db.Column(db.String, nullable=False)
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    id_paroquia = db.Column(db.BigInteger, db.ForeignKey("paroquia.id"))
    paroquia = db.relationship(
        "Paroquia", backref="paroquia", uselist=False, foreign_keys=[id_paroquia]
    )


class Pessoa(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    nome = db.Column(db.String, nullable=False)
    email = db.Column(db.String)
    telefone = db.Column(db.String, nullable=False)
    nascimento = db.Column(db.Date)
    apelido = db.Column(db.String, nullable=False)
    id_paroquia = db.Column(db.Integer, db.ForeignKey("paroquia.id"))


class Casal(db.Model, HashidMixin):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    id_esposo = db.Column(db.Integer, db.ForeignKey("pessoa.id"))
    id_esposa = db.Column(db.Integer, db.ForeignKey("pessoa.id"))
    esposa = db.relationship(
        "Pessoa", backref="esposa", uselist=False, foreign_keys=[id_esposa]
    )
    id_paroquia = db.Column(db.Integer, db.ForeignKey("paroquia.id"))
    esposo = db.relationship(
        "Pessoa", backref="esposo", uselist=False, foreign_keys=[id_esposo]
    )
    extenso = db.Column(db.String)
    id_inscrito = db.Column(db.Integer, db.ForeignKey("encontro.id"))
    id_circulo = db.Column(db.Integer, db.ForeignKey("circulo.id"))
    observacoes = db.Column(db.String(250))


class Movimento(db.Model, HashidMixin):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    nome = db.Column(db.String, nullable=False)
    id_paroquia = db.Column(db.Integer, db.ForeignKey("paroquia.id"), nullable=False)


class Equipe(db.Model, HashidMixin):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    nome = db.Column(db.String, nullable=False)
    descricao = db.Column(db.String, nullable=False)
    id_movimento = db.Column(db.Integer, db.ForeignKey("movimento.id"), nullable=False)


class Encontro(db.Model, HashidMixin):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    nome = db.Column(db.String, nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    tema = db.Column(db.String, nullable=False)
    data_inicio = db.Column(db.Date, nullable=False)
    data_termino = db.Column(db.Date, nullable=False)
    id_movimento = db.Column(db.Integer, db.ForeignKey("movimento.id"), nullable=False)


class Circulo(db.Model, HashidMixin):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    nome = db.Column(db.String)
    cor = db.Column(db.String, nullable=False)
    id_coordenador = db.Column(db.Integer, db.ForeignKey("casal.id"))
    coordenador = db.relationship(
        "Casal", backref="coordenador", uselist=False, foreign_keys=[id_coordenador]
    )
    id_encontro = db.Column(db.Integer, db.ForeignKey("encontro.id"))
    id_paroquia = db.Column(db.Integer, db.ForeignKey("paroquia.id"))


class EquipeEncontro(db.Model):
    id_equipe = db.Column(db.BigInteger, db.ForeignKey("equipe.id"), primary_key=True)
    id_encontro = db.Column(
        db.BigInteger, db.ForeignKey("encontro.id"), primary_key=True
    )
    id_coordenador = db.Column(db.BigInteger, db.ForeignKey("casal.id"))
    equipe = db.relationship(
        "Equipe", backref="equipe", uselist=False, foreign_keys=[id_equipe]
    )
    coordenador = db.relationship(
        "Casal",
        uselist=False,
        foreign_keys=[id_coordenador],
    )


class EquipeEncontroCasal(db.Model):
    id_equipe = db.Column(db.BigInteger, db.ForeignKey("equipe.id"), primary_key=True)
    equipe = db.relationship("Equipe", uselist=False, foreign_keys=[id_equipe])
    id_encontro = db.Column(
        db.BigInteger, db.ForeignKey("encontro.id"), primary_key=True
    )
    id_casal = db.Column(db.BigInteger, db.ForeignKey("casal.id"), primary_key=True)
    casal = db.relationship("Casal", uselist=False, foreign_keys=[id_casal])
    coordenador = db.Column(db.Boolean, nullable=False, default=False)
    aceito = db.Column(db.Boolean, nullable=False, default=True)
