from app.extensoes import db
from flask_login import UserMixin


class Paroquia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, unique=True, nullable=False)


class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    senha = db.Column(db.String, nullable=False)
    nome = db.Column(db.String, nullable=False)
    papel = db.Column(db.String, nullable=False)


class Pessoa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    email = db.Column(db.String)
    telefone = db.Column(db.String, nullable=False)
    id_paroquia = db.Column(db.Integer, db.ForeignKey("paroquia.id"))


class Casal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_esposo = db.Column(db.Integer, db.ForeignKey("pessoa.id"))
    id_esposa = db.Column(db.Integer, db.ForeignKey("pessoa.id"))
    esposa = db.relationship("Pessoa", backref="esposa", uselist=False, foreign_keys=[id_esposa])
    id_paroquia = db.Column(db.Integer, db.ForeignKey("paroquia.id"))
    esposo = db.relationship("Pessoa", backref="esposo", uselist=False, foreign_keys=[id_esposo])
    extenso = db.Column(db.String)
    #away_ref = db.relationship("Pessoa", backref="fixture", uselist=False, foreign_keys=[away_id])