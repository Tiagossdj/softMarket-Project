from flask import Blueprint, jsonify, request
from app.modelo_db import Produto, db

# Blueprint para cadastro de produto
cadastrar_produto = Blueprint("cadastrar_produto", __name__)


# Rota de cadastro de produto
@cadastrar_produto.route("/produto", methods=["POST"])
def cadastrar_produto_func():
    dados = request.get_json()

    if not all(
        key in dados
        for key in ("nome", "preco", "quantidade_em_estoque", "fornecedor_id")
    ):
        return jsonify({"error": "Dados incompletos."}), 400

    produto = Produto(
        nome=dados["nome"],
        preco=dados["preco"],
        quantidade_em_estoque=dados["quantidade_em_estoque"],
        fornecedor_id=dados["fornecedor_id"],
    )
    db.session.add(produto)
    db.session.commit()

    return jsonify({"message": "Produto cadastrado com sucesso!"}), 201


# Rota para excluir um produto
@cadastrar_produto.route("/produto/<int:id>", methods=["DELETE"])
def excluir_produto(id):
    produto = Produto.query.get(id)
    if produto is None:
        return jsonify({"message": "Produto não encontrado"}), 4
    # Verifica se o produto está em pedidos de estoque
    if produto.pedidos_estoque:
        return (
            jsonify(
                {
                    "message": "Produto não pode ser excluído, pois está em pedidos de estoque."
                }
            ),
            400,
        )

    db.session.delete(produto)
    db.session.commit()

    return jsonify({"message": "Produto excluído com sucesso!"}), 200


# Rota para listar todos os produtos
@cadastrar_produto.route("/produtos", methods=["GET"])
def listar_produtos():
    produtos = Produto.query.all()  # Consulta todos os produtos no banco de dados
    lista_produtos = [
        {
            "id": produto.id,
            "nome": produto.nome,
            "preco": produto.preco,
            "quantidade_em_estoque": produto.quantidade_em_estoque,
            "fornecedor_id": produto.fornecedor_id,
        }
        for produto in produtos
    ]
    return jsonify(lista_produtos), 200


# rota para buscar um produto pelo id
@cadastrar_produto.route("/produto/<int:id>", methods=["GET"])
def obter_produto_por_id(id):
    produto = Produto.query.get(id)  # Busca o produto pelo ID
    if not produto:
        return jsonify({"mensagem": "Produto não encontrado"}), 404

    produto_data = {
        "id": produto.id,
        "nome": produto.nome,
        "preco": produto.preco,
        "quantidade_em_estoque": produto.quantidade_em_estoque,
        "fornecedor_id": produto.fornecedor_id,
    }
    return jsonify(produto_data), 200
