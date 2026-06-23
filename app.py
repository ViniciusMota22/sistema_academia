from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from models import db, Aluno, Plano, Matricula
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route("/")
def home():
    total_alunos = Aluno.query.count()
    total_planos = Plano.query.count()
    total_matriculas = Matricula.query.count()
    alunos_ativos = Aluno.query.filter_by(status="Ativo").count()
    return render_template(
        "index.html",
        total_alunos=total_alunos,
        total_planos=total_planos,
        total_matriculas=total_matriculas,
        alunos_ativos=alunos_ativos,
    )

# ALUNOS
@app.route("/alunos")
def listar_alunos():
    alunos = Aluno.query.order_by(Aluno.id.desc()).all()
    return render_template("alunos.html", alunos=alunos)

@app.route("/novo-aluno", methods=["GET", "POST"])
def novo_aluno():
    planos = Plano.query.order_by(Plano.nome).all()

    if request.method == "POST":
        plano_id = request.form.get("plano_id") or None
        aluno = Aluno(
            nome=request.form["nome"],
            cpf=request.form["cpf"],
            telefone=request.form.get("telefone"),
            email=request.form.get("email"),
            status=request.form.get("status", "Ativo"),
            plano_id=plano_id,
        )
        db.session.add(aluno)
        db.session.commit()
        flash("Aluno cadastrado com sucesso!", "success")
        return redirect(url_for("listar_alunos"))

    return render_template("novo_aluno.html", planos=planos)

@app.route("/editar-aluno/<int:id>", methods=["GET", "POST"])
def editar_aluno(id):
    aluno = Aluno.query.get_or_404(id)
    planos = Plano.query.order_by(Plano.nome).all()

    if request.method == "POST":
        aluno.nome = request.form["nome"]
        aluno.cpf = request.form["cpf"]
        aluno.telefone = request.form.get("telefone")
        aluno.email = request.form.get("email")
        aluno.status = request.form.get("status", "Ativo")
        aluno.plano_id = request.form.get("plano_id") or None
        db.session.commit()
        flash("Aluno atualizado com sucesso!", "success")
        return redirect(url_for("listar_alunos"))

    return render_template("editar_aluno.html", aluno=aluno, planos=planos)

@app.route("/excluir-aluno/<int:id>")
def excluir_aluno(id):
    aluno = Aluno.query.get_or_404(id)
    db.session.delete(aluno)
    db.session.commit()
    flash("Aluno excluído com sucesso!", "success")
    return redirect(url_for("listar_alunos"))

# PLANOS
@app.route("/planos")
def listar_planos():
    planos = Plano.query.order_by(Plano.id.desc()).all()
    return render_template("planos.html", planos=planos)

@app.route("/novo-plano", methods=["GET", "POST"])
def novo_plano():
    if request.method == "POST":
        plano = Plano(
            nome=request.form["nome"],
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
        plano.nome = request.form["nome"]
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
    matriculas = Matricula.query.order_by(Matricula.id.desc()).all()
    return render_template("matriculas.html", matriculas=matriculas)

@app.route("/nova-matricula", methods=["GET", "POST"])
def nova_matricula():
    alunos = Aluno.query.order_by(Aluno.nome).all()

    if request.method == "POST":
        data_txt = request.form.get("data_inicio")
        data_inicio = datetime.strptime(data_txt, "%Y-%m-%d").date() if data_txt else None
        matricula = Matricula(
            aluno_id=int(request.form["aluno_id"]),
            data_inicio=data_inicio,
            status=request.form.get("status", "Ativa"),
        )
        db.session.add(matricula)
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
    with app.app_context():
        db.create_all()
    app.run(debug=True)
