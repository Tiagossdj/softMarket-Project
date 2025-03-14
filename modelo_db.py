from turtle import back
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://usuario:senha@localhost:5432/softmarket"
)

db = SQLAlchemy(app)

# Modelos


class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), sqlalchemy.Nullable(False))
    preco = db.Column(db.Float, sqlalchemy.Nullable(False))
    quantidade_em_estoque = db.Column(db.Integer, sqlalchemy.Nullable(False))
    fornecedor_id = db.Column(
        db.Integer, db.ForeignKey("fornecedor.id"), sqlalchemy.Nullable(False)
    )
    fornecedor = db.relationship("fornecedor", back_populates="produtos")


class Cliente(db.Model):
    id = db.Column(db.Integer, PrimaryKey=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)


class Fornecedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(14), nullable=False, unique=True)
    contato = db.Column(db.String(100), nullable=False)
    produtos = db.relationship("Produto", back_populates="fornecedor")


class Compra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"), nullable=False)
    data = db.Column(db.DateTime, nullable=False)
    total = db.Column(db.Float, nullable=False)
    cliente = db.relationship("Cliente", back_populates="compras")


class PedidoEstoque(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey("produto.id"), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    fornecedor_id = db.Column(
        db.Integer, db.ForeignKey("fornecedor.id"), nullable=False
    )
    produto = db.relationship("Produto", back_populates="pedidos_estoque")
    fornecedor = db.relationship("Fornecedor", back_populates="pedidos_estoque")


# relação de compra - cliente
Cliente.compras = db.relationship("compra", back_populates="cliente")

# Inicializa o banco de dados
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
