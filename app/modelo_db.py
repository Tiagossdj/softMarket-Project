from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    quantidade_em_estoque = db.Column(db.Integer, nullable=False)
    fornecedor_id = db.Column(
        db.Integer, db.ForeignKey("fornecedor.id"), nullable=False
    )
    fornecedor = db.relationship("Fornecedor", back_populates="produtos")
    pedidos_estoque = db.relationship("PedidoEstoque", back_populates="produto")


class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    compras = db.relationship("Compra", back_populates="cliente")


class Fornecedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(14), nullable=False, unique=True)
    contato = db.Column(db.String(100), nullable=False)
    produtos = db.relationship("Produto", back_populates="fornecedor")
    pedidos_estoque = db.relationship("PedidoEstoque", back_populates="fornecedor")


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
