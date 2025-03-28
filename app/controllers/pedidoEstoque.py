from datetime import datetime
from flask import Blueprint, request, jsonify
from app import db
from app.modelo_db import PedidoEstoque, Produto

pedido_estoque = Blueprint("pedido_estoque", __name__)


@pedido_estoque.route("/pedidoEstoque", methods=["POST"])
def cadastrar_pedido_estoque():
    try:
        # Obtém os dados da requisição
        data = request.get_json()
        print("Dados recebidos:", data)  # Exibe os dados no terminal para depuração

        # Validação dos dados
        if (
            not data.get("produto_id")
            or not data.get("quantidade")
            or not data.get("fornecedor_id")
        ):
            return (
                jsonify(
                    {
                        "error": "Os campos produto_id, quantidade e fornecedor_id são obrigatórios!"
                    }
                ),
                400,
            )

        produto_id = data["produto_id"]
        quantidade = data["quantidade"]
        fornecedor_id = data["fornecedor_id"]
        print(
            f"produto_id: {produto_id}, quantidade: {quantidade}, fornecedor_id: {fornecedor_id}"
        )  # Logando as variáveis

        # Verificar se o produto existe no banco de dados
        produto = Produto.query.get(produto_id)
        if not produto:
            return jsonify({"error": "Produto não encontrado!"}), 404
        print("Produto encontrado:", produto)  # Logando se o produto foi encontrado

        # Criar um novo pedido de estoque
        novo_pedido = PedidoEstoque(
            produto_id=produto_id,
            quantidade=quantidade,
            fornecedor_id=fornecedor_id,
            data_pedido=datetime.utcnow(),
        )
        print(f"Novo pedido criado: {novo_pedido}")  # Logando o pedido criado

        # Adicionar o pedido de estoque ao banco de dados
        db.session.add(novo_pedido)
        db.session.commit()

        return jsonify({"message": "Pedido de estoque realizado com sucesso!"}), 201

    except Exception as e:
        # Se ocorrer um erro, faz o rollback e retorna a mensagem de erro
        db.session.rollback()
        print("Erro:", str(e))  # Exibe o erro no terminal para depuração
        return jsonify({"error": str(e)}), 500


@pedido_estoque.route("/estoque", methods=["GET"])
def visualizar_estoque():
    try:
        produtos = Produto.query.all()
        estoque = []
        for produto in produtos:
            estoque.append(
                {
                    "produto_id": produto.id,
                    "nome": produto.nome,
                    "quantidade_em_estoque": produto.quantidade_em_estoque,
                }
            )
        return jsonify(estoque), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@pedido_estoque.route("/baixaEstoque", methods=["POST"])
def baixa_estoque():
    try:
        data = request.get_json()
        produto_id = data["produto_id"]
        quantidade = data["quantidade"]

        produto = Produto.query.get(produto_id)
        if produto and produto.quantidade_em_estoque >= quantidade:
            produto.quantidade_em_estoque -= quantidade
            db.session.commit()
            return jsonify({"message": "Estoque ajustado com sucesso!"}), 200
        else:
            return (
                jsonify({"error": "Quantidade inválida ou produto não encontrado!"}),
                400,
            )
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@pedido_estoque.route("/estoqueBaixo", methods=["GET"])
def estoque_baixo():
    try:
        limite_estoque = 30  # Defina aqui o limite que considera "baixo"
        produtos_baixo_estoque = Produto.query.filter(
            Produto.quantidade_em_estoque < limite_estoque
        ).all()
        estoque_baixo = []
        for produto in produtos_baixo_estoque:
            estoque_baixo.append(
                {
                    "produto_id": produto.id,
                    "nome": produto.nome,
                    "quantidade_em_estoque": produto.quantidade_em_estoque,
                }
            )
        return jsonify(estoque_baixo), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Tela de pedidos: Visualizar todos os pedidos, editar e excluir


@pedido_estoque.route("/pedidosEstoque", methods=["GET"])
def listar_pedidos_estoque():
    try:
        pedidos = PedidoEstoque.query.all()
        pedidos_data = [
            {
                "id": pedido.id,
                "produto_id": pedido.produto_id,
                "quantidade": pedido.quantidade,
                "fornecedor_id": pedido.fornecedor_id,
                "produto_nome": pedido.produto.nome,
                "fornecedor_nome": pedido.fornecedor.nome,
                "data_pedido": (
                    pedido.data_pedido.isoformat() if pedido.data_pedido else None
                ),
            }
            for pedido in pedidos
        ]
        return jsonify({"pedidos": pedidos_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@pedido_estoque.route("/pedidoEstoque/<int:id>", methods=["PUT"])
def editar_pedido_estoque(id):
    try:
        data = request.get_json()
        pedido = PedidoEstoque.query.get_or_404(id)

        # Atualizar os campos do pedido
        pedido.produto_id = data.get("produto_id", pedido.produto_id)
        pedido.quantidade = data.get("quantidade", pedido.quantidade)
        pedido.fornecedor_id = data.get("fornecedor_id", pedido.fornecedor_id)

        # Manter a data original ou atualizar se necessário
        pedido.data_pedido = pedido.data_pedido or datetime.utcnow()

        db.session.commit()
        return jsonify({"message": "Pedido de estoque atualizado com sucesso!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@pedido_estoque.route("/pedidoEstoque/<int:id>", methods=["DELETE"])
def excluir_pedido_estoque(id):
    try:
        pedido = PedidoEstoque.query.get_or_404(id)

        # Excluir o pedido de estoque
        db.session.delete(pedido)
        db.session.commit()

        return jsonify({"message": "Pedido de estoque excluído com sucesso!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
