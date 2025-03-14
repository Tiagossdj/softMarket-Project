from flask import Blueprint, request, jsonify
from app import db
from app.modelo_db import PedidoEstoque

pedido_estoque = Blueprint("pedido_estoque", __name__)


@pedido_estoque.route("/pedidoEstoque", methods=["POST"])
def cadastrar_pedido_estoque():
    try:
        data = request.get_json()
        produto_id = data["produto_id"]
        quantidade = data["quantidade"]
        fornecedor_id = data["fornecedor_id"]

        # Criar um novo pedido de estoque
        novo_pedido = PedidoEstoque(
            produto_id=produto_id, quantidade=quantidade, fornecedor_id=fornecedor_id
        )

        # Adicionar o pedido de estoque ao banco
        db.session.add(novo_pedido)
        db.session.commit()

        return jsonify({"message": "Pedido de estoque realizado com sucesso!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
