from flask import Blueprint, render_template, request
import app.modulos.movimento.service as movimento_service
from app.model import Movimento, Equipe, Encontro, Circulo
from wtforms import StringField, IntegerField, DateField
from wtforms.validators import DataRequired, Optional
from flask_wtf import FlaskForm

movimento_bp = Blueprint("movimento", __name__, url_prefix="/movimentos")


class MovimentoForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired()])
    id = StringField("id")


class EquipeForm(FlaskForm):
    id = StringField("id")
    nome = StringField("Nome", validators=[DataRequired()])
    descricao = StringField("Descrição", validators=[DataRequired()])

    def retorna_equipe(self):
        resultado = Equipe()
        resultado.id = self.id.data
        resultado.nome = self.nome.data
        resultado.descricao = self.descricao.data
        return resultado


class EncontroForm(FlaskForm):
    id = StringField("id")
    nome = StringField("Nome", validators=[DataRequired()])
    tema = StringField("Tema", validators=[DataRequired()])
    ano = IntegerField("Ano", validators=[DataRequired()])
    data_inicio = DateField("Data", validators=[Optional()])
    data_termino = DateField("Data fim", validators=[Optional()])

    def retorna_encontro(self):
        resultado = Encontro()
        resultado.id = self.id.data
        resultado.nome = self.nome.data
        resultado.tema = self.tema.data
        resultado.ano = self.ano.data
        resultado.data_inicio = self.data_inicio.data
        resultado.data_termino = self.data_termino.data
        return resultado


@movimento_bp.route("/")
def index():
    movimentos = movimento_service.buscar_encontros(1)
    return render_template("movimento/index.html", movimentos=movimentos)


@movimento_bp.route("/register", methods=["GET", "POST"])
def register():
    movimento_form = MovimentoForm()
    if request.method == "GET":
        return render_template("movimento/register.html", form=movimento_form)

    if not movimento_form.validate_on_submit():
        return "Falha na validação do formulário", 400

    movimento = Movimento()
    movimento.nome = movimento_form.nome.data
    movimento.id_paroquia = 1
    movimento_service.criar_encontro(movimento)
    return "200", 200


@movimento_bp.route("/<int:id>/edit", methods=["GET", "POST"])
def edit(id):
    movimento = movimento_service.buscar_movimento_por_id(id, 1)

    if not movimento:
        return "Encontro não encontrado", 404

    movimento_form = MovimentoForm()

    if request.method == "GET":
        movimento_form.id.data = movimento.id
        movimento_form.nome.data = movimento.nome
        return render_template("movimento/register.html", form=movimento_form)

    if not movimento_form.validate_on_submit():
        return "Falha na validação do formulário", 400

    novo_movimento = Movimento()
    novo_movimento.nome = movimento_form.nome.data
    movimento_service.atualizar_movimento(movimento, novo_movimento)
    return "200", 200


@movimento_bp.route("/<int:id_movimento>/equipes")
def equipes(id_movimento):
    equipes = movimento_service.buscar_equipes_por_movimento(id_movimento)
    return render_template(
        "movimento/equipe.html", items=equipes, id_movimento=id_movimento
    )


@movimento_bp.route("/<int:id_movimento>/equipes/nova", methods=["GET", "POST"])
def nova_equipe(id_movimento):
    equipe_form = EquipeForm()

    if request.method == "GET":
        return render_template(
            "movimento/equipe_registro.html",
            form=equipe_form,
            id_movimento=id_movimento,
        )

    if not equipe_form.validate_on_submit():
        return "Falha na validação dos dados", 400

    nova_equipe = equipe_form.retorna_equipe()
    nova_equipe.id_movimento = id_movimento
    movimento_service.criar_equipe(nova_equipe)

    return "created", 201


@movimento_bp.route(
    "/<int:id_movimento>/equipes/<int:id_equipe>", methods=["GET", "POST"]
)
def editar_equipe(id_movimento, id_equipe):
    equipe_atual = movimento_service.buscar_equipe_por_id_e_movimento(
        id_equipe, id_movimento
    )

    if not equipe_atual:
        return "Equipe não encontrada", 404

    equipe_form = EquipeForm()

    if request.method == "GET":
        equipe_form.id.data = equipe_atual.id
        equipe_form.nome.data = equipe_atual.nome
        equipe_form.descricao.data = equipe_atual.descricao
        return render_template(
            "movimento/equipe_registro.html",
            form=equipe_form,
            id_movimento=id_movimento,
        )

    if not equipe_form.validate_on_submit():
        return "Falha na validação dos dados", 400

    nova_equipe = equipe_form.retorna_equipe()
    movimento_service.atualizar_equipe(equipe_atual, nova_equipe)

    return "updated", 200


@movimento_bp.route("/<int:_id>/encontros")
def encontros(_id):
    movimento = movimento_service.buscar_movimento_por_id(_id, 1)
    encontros = movimento_service.buscar_encontros_por_movimento(_id)
    return render_template(
        "movimento/encontro.html", encontros=encontros, movimento=movimento
    )


@movimento_bp.route("/<int:_id>/encontros/register", methods=["GET", "POST"])
def novo_encontro(_id):
    movimento = movimento_service.buscar_movimento_por_id(_id, 1)
    encontro_form = EncontroForm()

    if request.method == "GET":
        return render_template(
            "movimento/encontro_registro.html", form=encontro_form, movimento=movimento
        )

    if not encontro_form.validate_on_submit():
        return "Falha na validação do formulário", 400

    novo_encontro = encontro_form.retorna_encontro()
    novo_encontro.id_movimento = _id

    movimento_service.criar_encontro(novo_encontro)

    return "200", 201


@movimento_bp.route(
    "/<int:id_movimento>/encontros/<int:id_encontro>/edit", methods=["GET", "POST"]
)
def editar_encontro(id_movimento, id_encontro):
    movimento = movimento_service.buscar_movimento_por_id(id_movimento, 1)
    encontro = movimento_service.buscar_encontro_por_id(id_movimento, id_encontro)

    if not encontro:
        return "Evento não encontrado", 404

    encontro_form = EncontroForm()

    if request.method == "GET":
        encontro_form.id.data = encontro.id
        encontro_form.nome.data = encontro.nome
        encontro_form.tema.data = encontro.tema
        encontro_form.ano.data = encontro.ano
        encontro_form.data_inicio.data = encontro.data_inicio.date()
        encontro_form.data_termino.data = encontro.data_termino.date()
        return render_template(
            "movimento/encontro_registro.html", form=encontro_form, movimento=movimento
        )

    if not encontro_form.validate_on_submit():
        return "Falha na validação do formulário", 400

    encontro_alterado = encontro_form.retorna_encontro()

    movimento_service.atualizar_encontro(encontro, encontro_alterado)

    return "ok", 200


@movimento_bp.route("/<int:id_movimento>/encontros/<int:id_encontro>/circulos")
def circulos(id_movimento, id_encontro):
    circulos = movimento_service.buscar_circulos_por_encontro(id_encontro)
    return render_template(
        "movimento/circulo.html",
        items=circulos,
        id_movimento=id_movimento,
        id_encontro=id_encontro,
    )


class CirculoForm(FlaskForm):
    id = StringField("id")
    nome = StringField("Nome")
    cor = StringField("Cor", validators=[DataRequired()])
    id_coordenador = IntegerField("id_coordenador", validators=[Optional()])
    coordenador = StringField("coordenador")

    def retorna_circulo(self):
        resultado = Circulo()
        resultado.id = self.id.data
        resultado.nome = self.nome.data
        resultado.cor = self.cor.data
        resultado.id_coordenador = self.id_coordenador.data
        return resultado


@movimento_bp.route(
    "/<int:id_movimento>/encontros/<int:id_encontro>/novo", methods=["GET", "POST"]
)
def novo_circulo(id_movimento, id_encontro):
    circulo_form = CirculoForm()

    if request.method == "GET":
        return render_template(
            "movimento/circulo_registro.html",
            form=circulo_form,
            id_movimento=id_movimento,
            id_encontro=id_encontro,
        )

    if not circulo_form.validate_on_submit():
        return "Falha na validação do formulário", 400

    novo_circulo = circulo_form.retorna_circulo()
    novo_circulo.id_movimento = id_movimento
    novo_circulo.id_encontro = id_encontro
    novo_circulo.id_paroquia = 1

    movimento_service.criar_circulo(novo_circulo)

    return "200", 201


@movimento_bp.route(
    "/<int:id_movimento>/encontros/<int:id_encontro>/circulos/<int:id_circulo>",
    methods=["GET", "POST"],
)
def editar_circulo(id_movimento, id_encontro, id_circulo):
    circulo_atual = movimento_service.buscar_circulo_por_id_e_encontro(
        id_circulo, id_encontro
    )

    circulo_form = CirculoForm()

    if request.method == "GET":
        circulo_form.id.data = circulo_atual.id
        circulo_form.nome.data = circulo_atual.nome
        circulo_form.cor.data = circulo_atual.cor
        circulo_form.id_coordenador = circulo_atual.id_coordenador
        circulo_form.coordenador = (
            f"{circulo_atual.coordenador.esposo.nome}/{circulo_atual.coordenador.esposa.nome}"
        )
        return render_template(
            "movimento/circulo_registro.html",
            form=circulo_form,
            id_movimento=id_movimento,
            id_encontro=id_encontro,
        )

    if not circulo_form.validate_on_submit():
        return "Falha na validação do formulário", 400

    novo_circulo = circulo_form.retorna_circulo()
    novo_circulo.id_movimento = id_movimento
    novo_circulo.id_encontro = id_encontro
    novo_circulo.id_paroquia = 1

    movimento_service.atualizar_circulo(circulo_atual, novo_circulo)

    return "ok", 200
