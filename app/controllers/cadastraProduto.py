from flask import Blueprint, jsonify, request
from app.modelo_db import HistoricoProduto, Produto, db

# Blueprint para cadastro de produto
produto_route = Blueprint("produto_route", __name__)


# Rota de cadastro de produto
@produto_route.route("/produto", methods=["POST"], endpoint="cadastrar_produto")
def cadastrar_produto():
    try:
        data = request.get_json()
        nome = data["nome"]
        preco = data["preco"]
        quantidade_em_estoque = data["quantidade_em_estoque"]
        estoque_minimo = data["estoque_minimo"]
        fornecedor_id = data.get("fornecedor_id")

        # Verificação de quantidade em estoque válida
        if quantidade_em_estoque < 0:
            return (
                jsonify({"error": "Quantidade em estoque não pode ser negativa."}),
                400,
            )

        if fornecedor_id is None:
            return jsonify({"error": "Fornecedor ID é obrigatório."}), 400

        produto = Produto(
            nome=nome,
            preco=preco,
            quantidade_em_estoque=quantidade_em_estoque,
            estoque_minimo=estoque_minimo,
            fornecedor_id=fornecedor_id,
        )
        db.session.add(produto)
        db.session.commit()

        return jsonify({"message": "Produto cadastrado com sucesso!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# Rota para excluir um produto
@produto_route.route("/produto/<int:id>", methods=["DELETE"])
def excluir_produto(id):
    produto = db.session.get(Produto, id)
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
@produto_route.route("/produtos", methods=["GET"])
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
@produto_route.route("/produto/<int:id>", methods=["GET"])
def obter_produto_por_id(id):
    produto = db.session.get(Produto, id)  # Busca o produto pelo ID
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


# rota para atualizar quantidade de estoque (manualmente)
@produto_route.route("/produto/<int:id>/estoque", methods=["PUT"])
def atualizar_estoque_produto(id):
    try:
        data = request.get_json()
        quantidade = data["quantidade"]

        # Verificação de validade
        if quantidade < 0:
            return jsonify({"error": "Quantidade não pode ser negativa."}), 400

        produto = db.session.get(Produto, id)
        if not produto:
            return jsonify({"error": "Produto não encontrado!"}), 404

        produto.quantidade_em_estoque += quantidade
        db.session.commit()

        return jsonify({"message": "Estoque atualizado com sucesso!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# Atualizando a rota de listagem para incluir o preço com desconto
@produto_route.route("/produtos", methods=["GET"])
def listar_produtos_comDesconto():
    try:
        produtos = Produto.query.all()

        produtos_data = [
            {
                "id": p.id,
                "nome": p.nome,
                "preco": p.preco,
                "quantidade_em_estoque": p.quantidade_em_estoque,
                "preco_com_desconto": (
                    p.preco * (1 - (p.desconto / 100)) if p.desconto else p.preco
                ),
            }
            for p in produtos
        ]

        return jsonify({"produtos": produtos_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# rota para adicionar promoções para produtos!!!
# Adicionando um campo de desconto ao modelo Produto
# desconto = db.Column(db.Float, nullable=True)  # Desconto em percentual


# rota para registrar um histórico de alteração em um produto
@produto_route.route("/produto/<int:id>/atualizar", methods=["PUT"])
def atualizar_produto(id):
    try:
        data = request.get_json()
        produto = db.session.get(Produto, id)

        if not produto:
            return jsonify({"error": "Produto não encontrado!"}), 404

        preco_antigo = produto.preco
        quantidade_antiga = produto.quantidade_em_estoque

        produto.nome = data.get("nome", produto.nome)
        produto.preco = data.get("preco", produto.preco)
        produto.quantidade_em_estoque = data.get(
            "quantidade_em_estoque", produto.quantidade_em_estoque
        )

        # Registrar no histórico
        historico = HistoricoProduto(
            produto_id=id,
            preco_antigo=preco_antigo,
            preco_novo=produto.preco,
            quantidade_antiga=quantidade_antiga,
            quantidade_nova=produto.quantidade_em_estoque,
        )
        db.session.add(historico)
        db.session.commit()

        return jsonify({"message": "Produto atualizado com sucesso!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
