from flask import Blueprint, jsonify, request
from app.modelo_db import Cliente, db

# Define o Blueprint
cadastrar_cliente = Blueprint("cadastrar_cliente", __name__)


# Rota de cadastro de cliente
@cadastrar_cliente.route("/cliente", methods=["POST"])
def cadastrar_cliente_func():
    try:
        dados = request.get_json()

        nome = dados.get("nome")
        cpf = dados.get("cpf")
        email = dados.get("email")

        if not nome or not cpf or not email:
            return (
                jsonify({"error": "Dados incompletos. Informe nome, CPF e email."}),
                400,
            )

        cliente = Cliente(nome=nome, cpf=cpf, email=email)
        db.session.add(cliente)
        db.session.commit()

        return jsonify({"message": "Cliente cadastrado com sucesso!"}), 201

    except Exception as e:
        return (
            jsonify({"error": f"Ocorreu um erro ao cadastrar o cliente: {str(e)}"}),
            500,
        )


# Rota para excluir um cliente
@cadastrar_cliente.route("/cliente/<int:id>", methods=["DELETE"])
def excluir_cliente(id):
    cliente = Cliente.query.get(id)
    if cliente is None:
        return jsonify({"message": "Cliente não encontrado"}), 404

    db.session.delete(cliente)
    db.session.commit()

    return jsonify({"message": "Cliente excluído com sucesso!"}), 200


# Rota para listar todos os clientes
@cadastrar_cliente.route("/clientes", methods=["GET"])
def listar_clientes():
    clientes = Cliente.query.all()  # Consulta todos os clientes no banco de dados
    lista_clientes = [
        {
            "id": cliente.id,
            "nome": cliente.nome,
            "cpf": cliente.cpf,
            "email": cliente.email,
        }
        for cliente in clientes
    ]
    return jsonify(lista_clientes), 200
