from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Optional
from modulos.autenticacao import service as usuario_service
from modulos import auth_bp, encontro_bp, casal_bp


app = Flask(__name__)
app.config["SECRET_KEY"] = "something only you know"
login = LoginManager(app)
login.login_view = "authentication.login"

app.register_blueprint(auth_bp)
app.register_blueprint(encontro_bp)
app.register_blueprint(casal_bp)


class UsuarioForm(FlaskForm):
    matricula = StringField("Matrícula", validators=[DataRequired()])
    nome = StringField("Nome", validators=[DataRequired()])
    id = IntegerField("Id", validators=[Optional()])


@login.user_loader
def load_user(id):
    return usuario_service.buscar_por_id(int(id))


@app.route("/api/alunos", methods=["GET", "POST"])
def alunos():
    usuarioForm = UsuarioForm()
    if request.method == "GET":
        dados = usuario_service.buscar_todos_alunos()
        return render_template("alunos-ajax.html", alunos=dados)

    if not usuarioForm.validate_on_submit():
        print(usuarioForm.errors)
        return "Dados do usuário inválidos", 400

    usuario = None
    try:
        usuario_service.salvar_aluno(usuario)
        flash("Aluno Criado com Sucesso!", category="success")
        return f"/{usuario.id}", 201
    except:
        flash("Matrícula do aluno existe!", category="danger")
        return "Validation error", 406


@app.route("/api/alunos/add")
def add_aluno():
    usuarioForm = UsuarioForm()
    return render_template("cad-aluno-ajax.html", form=usuarioForm)


@app.route("/api/alunos/<int:id>", methods=["GET", "POST"])
def edit_aluno(id):
    aluno = usuario_service.buscar_por_id(id)
    usuarioForm = UsuarioForm()
    if request.method == "GET":
        usuarioForm.id.data = aluno.id
        usuarioForm.matricula.data = aluno.matricula
        usuarioForm.nome.data = aluno.name
        return render_template("cad-aluno-ajax.html", form=usuarioForm)

    if not usuarioForm.validate_on_submit():
        return "Dados do usuário inválidos", 400

    usuario = None
    usuario_service.atualizar_aluno(id, usuario)
    flash("Aluno Atualizado com Sucesso!", category="success")
    return f"/{usuario.id}", 200


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
@login_required
def root(path):
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
