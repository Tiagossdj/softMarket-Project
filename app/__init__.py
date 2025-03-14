from flask import Flask
from app.modelo_db import db
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Registra os blueprints
    from app.controllers.cadastraCliente import cadastrar_cliente
    from app.controllers.cadastraProduto import cadastrar_produto
    from app.controllers.cadastraFornecedor import cadastrar_fornecedor
    from app.controllers.pedidoEstoque import pedido_estoque
    from app.controllers.realizaCompra import realiza_compra

    app.register_blueprint(cadastrar_cliente)
    app.register_blueprint(cadastrar_produto)
    app.register_blueprint(cadastrar_fornecedor)
    app.register_blueprint(pedido_estoque)
    app.register_blueprint(realiza_compra)

    return app
