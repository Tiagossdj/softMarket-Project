from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    quantidade_em_estoque = db.Column(db.Integer, nullable=False)
    estoque_minimo = db.Column(db.Integer, nullable=False)  # controle de estoque mínimo
    fornecedor_id = db.Column(
        db.Integer, db.ForeignKey("fornecedor.id"), nullable=False
    )

    fornecedor = db.relationship("Fornecedor", back_populates="produtos")
    pedidos_estoque = db.relationship("PedidoEstoque", back_populates="produto")

    itens = db.relationship("ItemCompra", back_populates="produto", lazy=True)


class Fornecedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(14), nullable=False, unique=True)
    contato = db.Column(db.String(100), nullable=False)
    produtos = db.relationship("Produto", back_populates="fornecedor")
    pedidos_estoque = db.relationship("PedidoEstoque", back_populates="fornecedor")


class Compra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, nullable=False)
    total = db.Column(db.Float, nullable=False)

    # Relacionamento <reverso> para acessar os itens da compra
    itens = db.relationship("ItemCompra", back_populates="compra")


from datetime import datetime


class PedidoEstoque(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey("produto.id"), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    fornecedor_id = db.Column(
        db.Integer, db.ForeignKey("fornecedor.id"), nullable=False
    )
    data_pedido = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    produto = db.relationship("Produto", back_populates="pedidos_estoque", lazy=True)
    fornecedor = db.relationship(
        "Fornecedor", back_populates="pedidos_estoque", lazy=True
    )


class ItemCompra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    compra_id = db.Column(db.Integer, db.ForeignKey("compra.id"), nullable=True)
    produto_id = db.Column(db.Integer, db.ForeignKey("produto.id"), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)

    compra = db.relationship("Compra", back_populates="itens")
    produto = db.relationship("Produto", back_populates="itens")


class HistoricoProduto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey("produto.id"), nullable=False)
    preco_antigo = db.Column(db.Float, nullable=False)
    preco_novo = db.Column(db.Float, nullable=False)
    quantidade_antiga = db.Column(db.Integer, nullable=False)
    quantidade_nova = db.Column(db.Integer, nullable=False)
    data_alteracao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    produto = db.relationship("Produto", backref="historico_produto")
