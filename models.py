from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class Plano(db.Model):
    __tablename__ = "planos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    duracao_meses = db.Column(db.Integer, nullable=False)

    alunos = db.relationship("Aluno", backref="plano", lazy=True)

class Aluno(db.Model):
    __tablename__ = "alunos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    status = db.Column(db.String(20), default="Ativo")

    plano_id = db.Column(db.Integer, db.ForeignKey("planos.id"), nullable=True)
    matriculas = db.relationship("Matricula", backref="aluno", lazy=True, cascade="all, delete-orphan")

class Matricula(db.Model):
    __tablename__ = "matriculas"

    id = db.Column(db.Integer, primary_key=True)
    data_inicio = db.Column(db.Date, default=date.today)
    status = db.Column(db.String(20), default="Ativa")
    aluno_id = db.Column(db.Integer, db.ForeignKey("alunos.id"), nullable=False)
