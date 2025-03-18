from flask import Flask
from app.modelo_db import db
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Registra os blueprints

    from app.controllers.cadastraProduto import produto_route
    from app.controllers.cadastraFornecedor import fornecedor_route
    from app.controllers.pedidoEstoque import pedido_estoque
    from app.controllers.realizaCompra import realiza_compra
    from app.controllers.relatórios import relatorio_route

    app.register_blueprint(produto_route)
    app.register_blueprint(fornecedor_route)
    app.register_blueprint(pedido_estoque)
    app.register_blueprint(realiza_compra)
    app.register_blueprint(relatorio_route)

    return app
