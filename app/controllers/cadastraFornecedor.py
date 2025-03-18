from flask import Blueprint, request, jsonify
from app.modelo_db import db, Fornecedor

# Define o Blueprint
fornecedor_route = Blueprint("fornecedor_route", __name__)


# Cadastrar fornecedor
@fornecedor_route.route("/fornecedor", methods=["POST"])
def fornecedor_route_func():
    try:
        dados = request.get_json()
        nome = dados.get("nome")
        cnpj = dados.get("cnpj")
        contato = dados.get("contato")

        if not nome or not cnpj or not contato:
            return (
                jsonify({"error": "Dados incompletos. Informe nome, CNPJ e contato."}),
                400,
            )

        fornecedor = Fornecedor(nome=nome, cnpj=cnpj, contato=contato)
        db.session.add(fornecedor)
        db.session.commit()

        # Garantir que o id do fornecedor seja retornado corretamente
        return (
            jsonify(
                {"id": fornecedor.id, "message": "Fornecedor cadastrado com sucesso!"}
            ),
            201,
        )

    except Exception as e:
        return (
            jsonify({"error": f"Ocorreu um erro ao cadastrar o fornecedor: {str(e)}"}),
            500,
        )


# Excluir fornecedor
@fornecedor_route.route("/fornecedor/<int:id>", methods=["DELETE"])
def excluir_fornecedor(id):
    # Tenta buscar o fornecedor pelo ID
    fornecedor = db.session.get(Fornecedor, id)

    # Verifica se o fornecedor existe
    if fornecedor is None:
        return jsonify({"message": "Fornecedor não encontrado"}), 404

    # Verifica se o fornecedor está associado a produtos ou pedidos de estoque
    if fornecedor.produtos or fornecedor.pedidos_estoque:
        print(
            f"Fornecedor {fornecedor.id} não pode ser excluído, pois está associado a produtos ou pedidos de estoque."
        )
        return (
            jsonify(
                {
                    "message": "Fornecedor não pode ser excluído, pois está associado a produtos ou pedidos de estoque."
                }
            ),
            400,
        )

    # Exclui o fornecedor do banco de dados
    db.session.delete(fornecedor)
    db.session.commit()

    # Retorna uma mensagem de sucesso
    return jsonify({"message": "Fornecedor excluído com sucesso!"}), 200


# Rota para listar fornecedores
@fornecedor_route.route("/fornecedores", methods=["GET"])
def get_fornecedores():
    fornecedores = Fornecedor.query.all()  # Obtém todos os fornecedores
    if not fornecedores:
        return jsonify({"message": "Nenhum fornecedor encontrado."}), 404

    # Retorna os dados dos fornecedores em formato JSON
    resultado = [
        {
            "id": fornecedor.id,
            "nome": fornecedor.nome,
            "cnpj": fornecedor.cnpj,
            "contato": fornecedor.contato,
        }
        for fornecedor in fornecedores
    ]

    return jsonify(resultado), 200


# Rota para listar um fornecedor especifico pelo id
@fornecedor_route.route("/fornecedor/<int:id>", methods=["GET"])
def get_fornecedor_por_id(id):
    fornecedor = fornecedor = db.session.get(
        Fornecedor, id
    )  # Busca o fornecedor pelo ID
    if not fornecedor:
        return jsonify({"mensagem": "Fornecedor não encontrado."}), 404

    resultado = {
        "id": fornecedor.id,
        "nome": fornecedor.nome,
        "cnpj": fornecedor.cnpj,
        "contato": fornecedor.contato,
    }

    return jsonify(resultado), 200


# Rota para atualizar um fornecedor
@fornecedor_route.route("/fornecedor/<int:id>", methods=["PUT"])
def atualizar_fornecedor(id):
    fornecedor = db.session.get(Fornecedor, id)
    if not fornecedor:
        return jsonify({"message": "Fornecedor não encontrado"}), 404

    dados = request.get_json()
    nome = dados.get("nome", fornecedor.nome)
    cnpj = dados.get("cnpj", fornecedor.cnpj)
    contato = dados.get("contato", fornecedor.contato)

    fornecedor.nome = nome
    fornecedor.cnpj = cnpj
    fornecedor.contato = contato

    db.session.commit()

    return jsonify({"message": "Fornecedor atualizado com sucesso!"}), 200
