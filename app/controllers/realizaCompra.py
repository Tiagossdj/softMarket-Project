from flask import Blueprint, request, jsonify
from app import db
from app.modelo_db import Compra, ItemCompra, Produto
import logging

realiza_compra = Blueprint("realiza_compra", __name__)


@realiza_compra.route("/realizaCompra", methods=["POST"])
def realiza_compra_func():
    try:
        compra_data = request.get_json()

        # Criação da compra
        compra = Compra(
            data=compra_data["data"],
            total=compra_data["total"],
            forma_pagamento=compra_data["forma_pagamento"],
        )
        db.session.add(compra)
        db.session.flush()  # Para obter o ID da compra antes de salvar os itens

        for item_data in compra_data["itens"]:
            # Calcular o subtotal para cada item
            subtotal = item_data["quantidade"] * item_data["preco_unitario"]

            item_compra = ItemCompra(
                compra_id=compra.id,
                produto_id=item_data["produto_id"],
                quantidade=item_data["quantidade"],
                preco_unitario=item_data["preco_unitario"],
                subtotal=subtotal,  # Passar o subtotal calculado
            )
            db.session.add(item_compra)

            # Atualizar o estoque do produto
            produto = Produto.query.get(item_data["produto_id"])
            if produto:
                produto.quantidade_em_estoque -= item_data["quantidade"]

        db.session.commit()

        # Retornar a resposta com o ID da compra
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
        # Obter a compra pelo ID
        compra = Compra.query.get(id)
        if not compra:
            return jsonify({"error": "Compra não encontrada!"}), 404

        # Reverter o estoque dos itens da compra e guardar os itens
        itens_compra = list(compra.itens)  # Fazer uma cópia da lista de itens

        for item in itens_compra:
            produto = Produto.query.get(item.produto_id)
            if produto:
                produto.quantidade_em_estoque += item.quantidade
            else:
                return (
                    jsonify({"error": f"Produto {item.produto_id} não encontrado!"}),
                    404,
                )

            # Remover a referência à compra
            item.compra_id = None
            db.session.add(item)

        # Primeiro fazer commit dos itens atualizados
        db.session.commit()

        # Agora remover a compra
        db.session.delete(compra)
        db.session.commit()

        return jsonify({"message": "Compra cancelada com sucesso!"}), 200

    except Exception as e:
        db.session.rollback()
        print(f"Erro ao cancelar compra: {str(e)}")  # Log do erro para depuração
        return jsonify({"error": str(e)}), 500


formas_pagamento_bp = Blueprint("formas_pagamento", __name__)


@formas_pagamento_bp.route("/formasPagamento", methods=["GET"])
def listar_formas_pagamento():
    formas = ["Cartão de Crédito", "Cartão de Débito", "Dinheiro", "Pix"]
    return jsonify({"formas_pagamento": formas})
