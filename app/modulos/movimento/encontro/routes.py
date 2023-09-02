from flask import Blueprint, render_template, request, url_for
from flask_login import login_required
import app.modulos.movimento.service as movimento_service
from wtforms import StringField, IntegerField, DateField
from wtforms.validators import DataRequired, Optional
from flask_wtf import FlaskForm
from app.modulos.casal.handler import listar_casais, novo_casal, editar_casal
import app.modulos.casal.service as casal_service
import app.modulos.equipe.service as equipe_service
from app.model import Circulo, Encontro


encontro_bp = Blueprint(
    "encontro", __name__, url_prefix="/<int:id_movimento>/encontros"
)


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


@encontro_bp.route("/")
@login_required
def index(id_movimento):
    movimento = movimento_service.buscar_movimento_por_id(id_movimento, 1)
    encontros = movimento_service.buscar_encontros_por_movimento(id_movimento)
    return render_template(
        "movimento/encontro/index.html", encontros=encontros, movimento=movimento
    )


@encontro_bp.route("/novo", methods=["GET", "POST"])
@login_required
def novo(id_movimento):
    movimento = movimento_service.buscar_movimento_por_id(id_movimento, 1)
    encontro_form = EncontroForm()

    if request.method == "GET":
        return render_template(
            "movimento/encontro/registro.html", form=encontro_form, movimento=movimento
        )

    if not encontro_form.validate_on_submit():
        return "Falha na validação do formulário", 400

    novo_encontro = encontro_form.retorna_encontro()
    novo_encontro.id_movimento = id_movimento

    movimento_service.criar_encontro(novo_encontro)

    return "200", 201


@encontro_bp.route("/<int:id_encontro>", methods=["GET", "POST"])
@login_required
def editar(id_movimento, id_encontro):
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
        encontro_form.data_inicio.data = encontro.data_inicio
        encontro_form.data_termino.data = encontro.data_termino
        return render_template(
            "movimento/encontro/registro.html", form=encontro_form, movimento=movimento
        )

    if not encontro_form.validate_on_submit():
        return "Falha na validação do formulário", 400

    encontro_alterado = encontro_form.retorna_encontro()

    movimento_service.atualizar_encontro(encontro, encontro_alterado)

    return "ok", 200


@encontro_bp.route("/<int:id_encontro>/inscritos")
@login_required
def casais_inscritos(id_movimento, id_encontro):
    return listar_casais(
        id_encontro,
        url_for("movimento.encontro.index", id_movimento=id_movimento),
        novo_link=url_for(
            "movimento.encontro.novo_inscrito",
            id_movimento=id_movimento,
            id_encontro=id_encontro,
        ),
        edit_link=url_for(
            "movimento.encontro.casais_inscritos",
            id_movimento=id_movimento,
            id_encontro=id_encontro,
        ),
    )


@encontro_bp.route("/<int:id_encontro>/inscritos/novo")
@login_required
def novo_inscrito(id_movimento, id_encontro):
    return novo_casal(
        back_link=url_for(
            "movimento.encontro.casais_inscritos",
            id_movimento=id_movimento,
            id_encontro=id_encontro,
        ),
        id_inscrito=id_encontro,
    )


@encontro_bp.route("/<int:id_encontro>/inscritos/<int:id_casal>")
@login_required
def editar_inscrito(id_movimento, id_encontro, id_casal):
    return editar_casal(
        id=id_casal,
        back_link=url_for(
            "movimento.encontro.casais_inscritos",
            id_movimento=id_movimento,
            id_encontro=id_encontro,
        ),
    )


@encontro_bp.route("/<int:id_encontro>/circulos")
@login_required
def circulos(id_movimento, id_encontro):
    circulos_encontro = movimento_service.buscar_circulos_por_encontro(id_encontro)
    return render_template(
        "movimento/circulo.html",
        items=circulos_encontro,
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


@encontro_bp.route("/<int:id_encontro>/novo", methods=["GET", "POST"])
@login_required
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

    circulo_novo = circulo_form.retorna_circulo()
    circulo_novo.id_movimento = id_movimento
    circulo_novo.id_encontro = id_encontro
    circulo_novo.id_paroquia = 1

    movimento_service.criar_circulo(circulo_novo)

    return "200", 201


@encontro_bp.route(
    "/<int:id_encontro>/circulos/<int:id_circulo>",
    methods=["GET", "POST"],
)
@login_required
def editar_circulo(id_movimento, id_encontro, id_circulo):
    circulo_atual = movimento_service.buscar_circulo_por_id_e_encontro(
        id_circulo, id_encontro
    )

    circulo_form = CirculoForm()

    if request.method == "GET":
        circulo_form.id.data = circulo_atual.id
        circulo_form.nome.data = circulo_atual.nome
        circulo_form.cor.data = circulo_atual.cor
        circulo_form.id_coordenador.data = circulo_atual.id_coordenador
        if circulo_atual.coordenador:
            circulo_form.coordenador.data = f"{circulo_atual.coordenador.esposo.apelido}/{circulo_atual.coordenador.esposa.apelido}"
        return render_template(
            "movimento/circulo_registro.html",
            form=circulo_form,
            id_movimento=id_movimento,
            id_encontro=id_encontro,
        )

    if not circulo_form.validate_on_submit():
        return "Falha na validação do formulário", 400

    circulo_novo = circulo_form.retorna_circulo()
    circulo_novo.id_movimento = id_movimento
    circulo_novo.id_encontro = id_encontro
    circulo_novo.id_paroquia = 1

    movimento_service.atualizar_circulo(circulo_atual, circulo_novo)

    return "ok", 200


@encontro_bp.route(
    "/<int:id_encontro>/circulos/montagem",
    methods=["GET"],
)
@login_required
def montar_circulo(id_movimento, id_encontro):
    casais_sem_circulo = casal_service.buscar_casais_inscritos_sem_circulo(id_encontro)
    circulos_corrente = movimento_service.buscar_circulos_por_encontro(id_encontro)

    return render_template(
        "movimento/circulo_montagem.html",
        casais_sem_circulo=casais_sem_circulo,
        circulos_corrente=circulos_corrente,
        id_movimento=id_movimento,
        id_encontro=id_encontro,
    )


@encontro_bp.route("/<int:id_encontro>/equipes")
def equipes_encontro_index(id_movimento, id_encontro):
    equipes_encontro = equipe_service.buscar_equipes_por_encontro(id_encontro)
    return render_template(
        "movimento/equipe_encontro.html",
        equipes_encontro=equipes_encontro,
        id_encontro=id_encontro,
        id_movimento=id_movimento,
    )
