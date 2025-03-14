from flask import Blueprint, request, jsonify
from app.modelo_db import db, Fornecedor

# Define o Blueprint
cadastrar_fornecedor = Blueprint("cadastrar_fornecedor", __name__)


# Cadastrar fornecedor
@cadastrar_fornecedor.route("/fornecedor", methods=["POST"])
def cadastrar_fornecedor_func():
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

        return jsonify({"message": "Fornecedor cadastrado com sucesso!"}), 201

    except Exception as e:
        return (
            jsonify({"error": f"Ocorreu um erro ao cadastrar o fornecedor: {str(e)}"}),
            500,
        )


# Excluir fornecedor
@cadastrar_fornecedor.route("/fornecedor/<int:id>", methods=["DELETE"])
def excluir_fornecedor(id):
    fornecedor = Fornecedor.query.get(id)
    if fornecedor is None:
        return jsonify({"message": "Fornecedor não encontrado"}), 404

    # Verifica se o fornecedor está associado a produtos ou pedidos de estoque
    if fornecedor.produtos or fornecedor.pedidos_estoque:
        return (
            jsonify(
                {
                    "message": "Fornecedor não pode ser excluído, pois está associado a produtos ou pedidos de estoque."
                }
            ),
            400,
        )

    db.session.delete(fornecedor)
    db.session.commit()

    return jsonify({"message": "Fornecedor excluído com sucesso!"}), 200


# Rota para listar fornecedores
@cadastrar_fornecedor.route("/fornecedores", methods=["GET"])
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
