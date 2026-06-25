from datetime import datetime

from flask import Flask, flash, redirect, render_template, request, url_for
from sqlalchemy.exc import IntegrityError

from config import Config
from models import Aluno, Matricula, Plano, db

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Garante as tabelas também quando a aplicação é iniciada pelo Gunicorn no Render.
with app.app_context():
    db.create_all()


def garantir_matricula_automatica(aluno, status_preferido=None):
    """Cria uma matrícula somente se o aluno ainda não possuir uma."""
    existente = Matricula.query.filter_by(aluno_id=aluno.id).first()
    if existente:
        return False

    status_matricula = status_preferido or (
        "Ativa" if aluno.status == "Ativo" else "Pendente"
    )
    db.session.add(
        Matricula(
            aluno_id=aluno.id,
            data_inicio=datetime.today().date(),
            status=status_matricula,
        )
    )
    db.session.commit()
    return True


@app.route("/")
def home():
    total_alunos = Aluno.query.count()
    alunos_ativos = Aluno.query.filter_by(status="Ativo").count()
    total_planos = Plano.query.count()
    total_matriculas = Matricula.query.count()
    alunos_inativos = max(total_alunos - alunos_ativos, 0)
    percentual_ativos = round((alunos_ativos / total_alunos) * 100) if total_alunos else 0

    planos = Plano.query.order_by(Plano.nome).all()
    planos_resumo = [
        {"nome": plano.nome, "total": len(plano.alunos)}
        for plano in planos
    ]
    maior_total_plano = max((item["total"] for item in planos_resumo), default=1)

    return render_template(
        "index.html",
        total_alunos=total_alunos,
        alunos_ativos=alunos_ativos,
        alunos_inativos=alunos_inativos,
        percentual_ativos=percentual_ativos,
        total_planos=total_planos,
        total_matriculas=total_matriculas,
        planos_resumo=planos_resumo,
        maior_total_plano=maior_total_plano,
        alunos_recentes=Aluno.query.order_by(Aluno.id.desc()).limit(5).all(),
        matriculas_recentes=Matricula.query.order_by(Matricula.id.desc()).limit(5).all(),
    )


# ALUNOS
@app.route("/alunos")
def listar_alunos():
    return render_template(
        "alunos.html",
        alunos=Aluno.query.order_by(Aluno.id.desc()).all(),
    )


@app.route("/novo-aluno", methods=["GET", "POST"])
def novo_aluno():
    planos = Plano.query.order_by(Plano.nome).all()

    if request.method == "POST":
        aluno = Aluno(
            nome=request.form["nome"].strip(),
            cpf=request.form["cpf"].strip(),
            telefone=request.form.get("telefone", "").strip(),
            email=request.form.get("email", "").strip(),
            status=request.form.get("status", "Ativo"),
            plano_id=request.form.get("plano_id") or None,
        )
        try:
            db.session.add(aluno)
            db.session.commit()
            garantir_matricula_automatica(aluno)
        except IntegrityError:
            db.session.rollback()
            flash("Já existe um aluno cadastrado com esse CPF.", "error")
            return render_template("novo_aluno.html", planos=planos)

        flash(
            "Aluno cadastrado com sucesso. A matrícula foi criada automaticamente!",
            "success",
        )
        return redirect(url_for("listar_alunos"))

    return render_template("novo_aluno.html", planos=planos)


@app.route("/editar-aluno/<int:id>", methods=["GET", "POST"])
def editar_aluno(id):
    aluno = Aluno.query.get_or_404(id)
    planos = Plano.query.order_by(Plano.nome).all()

    if request.method == "POST":
        aluno.nome = request.form["nome"].strip()
        aluno.cpf = request.form["cpf"].strip()
        aluno.telefone = request.form.get("telefone", "").strip()
        aluno.email = request.form.get("email", "").strip()
        aluno.status = request.form.get("status", "Ativo")
        aluno.plano_id = request.form.get("plano_id") or None
        try:
            db.session.commit()
            garantir_matricula_automatica(aluno)
        except IntegrityError:
            db.session.rollback()
            flash("Já existe outro aluno cadastrado com esse CPF.", "error")
            return render_template("editar_aluno.html", aluno=aluno, planos=planos)

        flash("Aluno atualizado com sucesso!", "success")
        return redirect(url_for("listar_alunos"))

    return render_template("editar_aluno.html", aluno=aluno, planos=planos)


@app.route("/excluir-aluno/<int:id>")
def excluir_aluno(id):
    aluno = Aluno.query.get_or_404(id)
    db.session.delete(aluno)
    db.session.commit()
    flash("Aluno e suas matrículas foram excluídos.", "success")
    return redirect(url_for("listar_alunos"))


# PLANOS
@app.route("/planos")
def listar_planos():
    return render_template(
        "planos.html",
        planos=Plano.query.order_by(Plano.id.desc()).all(),
    )


@app.route("/novo-plano", methods=["GET", "POST"])
def novo_plano():
    if request.method == "POST":
        plano = Plano(
            nome=request.form["nome"].strip(),
            valor=float(request.form["valor"].replace(",", ".")),
            duracao_meses=int(request.form["duracao_meses"]),
        )
        db.session.add(plano)
        db.session.commit()
        flash("Plano cadastrado com sucesso!", "success")
        return redirect(url_for("listar_planos"))

    return render_template("novo_plano.html")


@app.route("/editar-plano/<int:id>", methods=["GET", "POST"])
def editar_plano(id):
    plano = Plano.query.get_or_404(id)

    if request.method == "POST":
        plano.nome = request.form["nome"].strip()
        plano.valor = float(request.form["valor"].replace(",", "."))
        plano.duracao_meses = int(request.form["duracao_meses"])
        db.session.commit()
        flash("Plano atualizado com sucesso!", "success")
        return redirect(url_for("listar_planos"))

    return render_template("editar_plano.html", plano=plano)


@app.route("/excluir-plano/<int:id>")
def excluir_plano(id):
    plano = Plano.query.get_or_404(id)
    if plano.alunos:
        flash("Não é possível excluir um plano vinculado a alunos.", "error")
        return redirect(url_for("listar_planos"))

    db.session.delete(plano)
    db.session.commit()
    flash("Plano excluído com sucesso!", "success")
    return redirect(url_for("listar_planos"))


# MATRÍCULAS
@app.route("/matriculas")
def listar_matriculas():
    return render_template(
        "matriculas.html",
        matriculas=Matricula.query.order_by(Matricula.id.desc()).all(),
    )


@app.route("/nova-matricula", methods=["GET", "POST"])
def nova_matricula():
    alunos = Aluno.query.order_by(Aluno.nome).all()

    if request.method == "POST":
        aluno_id = int(request.form["aluno_id"])
        existente = Matricula.query.filter_by(aluno_id=aluno_id).first()
        if existente:
            flash("Esse aluno já possui uma matrícula.", "error")
            return render_template("nova_matricula.html", alunos=alunos)

        data_txt = request.form.get("data_inicio")
        data_inicio = (
            datetime.strptime(data_txt, "%Y-%m-%d").date()
            if data_txt
            else datetime.today().date()
        )
        db.session.add(
            Matricula(
                aluno_id=aluno_id,
                data_inicio=data_inicio,
                status=request.form.get("status", "Ativa"),
            )
        )
        db.session.commit()
        flash("Matrícula cadastrada com sucesso!", "success")
        return redirect(url_for("listar_matriculas"))

    return render_template("nova_matricula.html", alunos=alunos)


@app.route("/excluir-matricula/<int:id>")
def excluir_matricula(id):
    matricula = Matricula.query.get_or_404(id)
    db.session.delete(matricula)
    db.session.commit()
    flash("Matrícula excluída com sucesso!", "success")
    return redirect(url_for("listar_matriculas"))


if __name__ == "__main__":
    app.run(debug=True)
