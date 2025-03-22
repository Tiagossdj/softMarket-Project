from datetime import timedelta
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.modelo_db import db
from config import Config


def create_app():
    app = Flask(__name__)
    CORS(app, origins=["http://127.0.0.1:5500"])
    app.config.from_object(Config)

    app.config["SECRET_KEY"] = "minha_chave_flask"

    app.config["SECRET_KEY"] = "MinhaChaveSuperSecreta"  # Configure a chave secreta
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)  # tempo de expiração

    db.init_app(app)
    JWTManager(app)

    # Registra os blueprints

    from app.controllers.cadastraProduto import produto_route
    from app.controllers.cadastraFornecedor import fornecedor_route
    from app.controllers.pedidoEstoque import pedido_estoque
    from app.controllers.realizaCompra import realiza_compra
    from app.controllers.relatórios import relatorio_route
    from app.controllers.geraGrafico import grafico_controller
    from app.controllers.realizaCompra import formas_pagamento_bp
    from app.controllers.geraGrafico import gera_grafico_route
    from app.controllers.usuario import registra_usuario

    app.register_blueprint(produto_route)
    app.register_blueprint(fornecedor_route)
    app.register_blueprint(pedido_estoque)
    app.register_blueprint(realiza_compra)
    app.register_blueprint(relatorio_route)
    app.register_blueprint(grafico_controller)
    app.register_blueprint(formas_pagamento_bp)
    app.register_blueprint(gera_grafico_route)
    app.register_blueprint(registra_usuario, url_prefix="/auth")

    return app
