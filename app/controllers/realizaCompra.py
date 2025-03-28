from flask import Blueprint, request, jsonify
from app import db
from app.modelo_db import Compra, ItemCompra, Produto
import logging

realiza_compra = Blueprint("realiza_compra", __name__)


@realiza_compra.route("/realizaCompra", methods=["POST"])
def realiza_compra_func():
    try:
        compra_data = request.get_json()

        # Verificação de estoque antes de realizar a venda
        for item_data in compra_data["itens"]:
            produto = Produto.query.get(item_data["produto_id"])
            if not produto:
                return (
                    jsonify(
                        {"error": f"Produto {item_data['produto_id']} não encontrado"}
                    ),
                    404,
                )

            if produto.quantidade_em_estoque < item_data["quantidade"]:
                return (
                    jsonify(
                        {
                            "error": f"Estoque insuficiente para o produto {produto.nome}. "
                            f"Estoque atual: {produto.quantidade_em_estoque}, "
                            f"Quantidade solicitada: {item_data['quantidade']}"
                        }
                    ),
                    400,
                )

        # Resto do código permanece igual
        compra = Compra(
            data=compra_data["data"],
            total=compra_data["total"],
            forma_pagamento=compra_data["forma_pagamento"],
        )
        db.session.add(compra)
        db.session.flush()  # Para obter o ID da compra antes de salvar os itens

        for item_data in compra_data["itens"]:
            subtotal = item_data["quantidade"] * item_data["preco_unitario"]

            item_compra = ItemCompra(
                compra_id=compra.id,
                produto_id=item_data["produto_id"],
                quantidade=item_data["quantidade"],
                preco_unitario=item_data["preco_unitario"],
                subtotal=subtotal,
            )
            db.session.add(item_compra)

            # Atualizar o estoque do produto
            produto = Produto.query.get(item_data["produto_id"])
            produto.quantidade_em_estoque -= item_data["quantidade"]

        db.session.commit()

        return (
            jsonify({"message": "Compra realizada com sucesso!", "id": compra.id}),
            201,
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# Cancelamento de compra
import logging

# Configuração do logging
logging.basicConfig(level=logging.DEBUG)


@realiza_compra.route("/cancelarCompra/<int:id>", methods=["PUT"])
def cancelar_compra(id):
    try:
        compra = Compra.query.get(id)
        if not compra:
            return jsonify({"error": "Compra não encontrada!"}), 404

        # Copiar itens antes de modificar
        itens_compra = list(compra.itens)

        for item in itens_compra:
            produto = Produto.query.get(item.produto_id)
            if not produto:
                return (
                    jsonify({"error": f"Produto {item.produto_id} não encontrado!"}),
                    404,
                )

            # Adicionar verificação de estoque antes de reverter
            produto.quantidade_em_estoque += item.quantidade
            db.session.add(produto)

            # Aqui você pode optar por remover ou não a referência à compra
            item.compra_id = None
            db.session.add(item)

        db.session.commit()

        # Remover a compra
        db.session.delete(compra)
        db.session.commit()

        return jsonify({"message": "Compra cancelada com sucesso!"}), 200

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao cancelar compra: {str(e)}")
        return jsonify({"error": str(e)}), 500


@realiza_compra.route("/formasPagamento", methods=["GET"])
def listar_formas_pagamento():
    formas = ["Cartão de Crédito", "Cartão de Débito", "Dinheiro", "Pix"]
    return jsonify({"formas_pagamento": formas})
