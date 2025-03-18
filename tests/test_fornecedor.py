import time
import pytest
from app import db, create_app
from app.modelo_db import Fornecedor  # Importe seu app e db corretamente


def test_cadastrar_fornecedor(client):
    fornecedor_data = {
        "nome": "Fornecedor Teste",
        "cnpj": "12345678000195",
        "contato": "1234567890",
    }

    response = client.post("/fornecedor", json=fornecedor_data)

    # print especifico para erros
    print(f"Status: {response.status_code}")
    print(f"Response Data: {response.data.decode('utf-8')}")

    assert response.status_code == 201
    assert "Fornecedor cadastrado com sucesso!" in response.get_data(as_text=True)


def test_excluir_fornecedor(client):
    # Criação do fornecedor
    fornecedor_data = {
        "nome": "Fornecedor Exclusivo",
        "cnpj": "98765432000123",
        "contato": "9876543210",
    }
    response = client.post("/fornecedor", json=fornecedor_data)
    assert (
        response.status_code == 201
    )  # Verifica se o fornecedor foi criado corretamente

    # Acessa o id do fornecedor criado
    fornecedor_id = response.json.get("id")
    print(f"Fornecedor ID: {fornecedor_id}")  # Verificação adicional
    assert fornecedor_id is not None  # Verifica se o id foi retornado

    # Exclui o fornecedor
    response = client.delete(f"/fornecedor/{fornecedor_id}")
    print(f"Status Code: {response.status_code}")  # Verificação adicional
    print(f"Response: {response.json}")  # Verificação adicional
    assert response.status_code == 200  # Verifica se a exclusão foi bem-sucedida


def test_listar_fornecedores(client):
    # Dados para criar um fornecedor
    fornecedor_data = {
        "nome": "Fornecedor Teste",
        "cnpj": "12345678000195",
        "contato": "1234567890",
    }

    # Realiza a requisição POST para criar um fornecedor
    response = client.post("/fornecedor", json=fornecedor_data)

    # Verifica se o fornecedor foi criado com sucesso
    assert response.status_code == 201
    assert "id" in response.json  # Verifica se o ID do fornecedor foi retornado

    # Realiza a requisição GET para listar os fornecedores
    response = client.get("/fornecedores")

    # Imprime o status da resposta e os dados para depuração
    print(f"Status: {response.status_code}")
    print(f"Response Data: {response.data.decode('utf-8')}")

    # Verifica se o status code da resposta é 200
    assert response.status_code == 200

    # Verifica se a resposta é uma lista
    assert isinstance(response.json, list)

    # Verifica se a lista contém pelo menos um fornecedor
    assert len(response.json) > 0


def test_listar_fornecedor_por_id(client):
    # Primeiro, crie um fornecedor para poder consultá-lo
    fornecedor_data = {
        "nome": "Fornecedor Teste",
        "cnpj": "12345678000195",
        "contato": "1234567890",
    }
    response = client.post("/fornecedor", json=fornecedor_data)
    fornecedor_id = response.json.get("id")

    response = client.get(f"/fornecedor/{fornecedor_id}")

    print(f"Status: {response.status_code}")
    print(f"Response Data: {response.data.decode('utf-8')}")

    assert response.status_code == 200
    assert response.json["id"] == fornecedor_id


def test_atualizar_fornecedor(client):
    # Primeiro, crie um fornecedor para poder atualizá-lo
    fornecedor_data = {
        "nome": "Fornecedor Teste",
        "cnpj": "12345678000195",
        "contato": "1234567890",
    }
    response = client.post("/fornecedor", json=fornecedor_data)
    fornecedor_id = response.json.get("id")

    # Dados para atualização
    updated_data = {
        "nome": "Fornecedor Teste Atualizado",
        "cnpj": "98765432000123",
        "contato": "0987654321",
    }

    response = client.put(f"/fornecedor/{fornecedor_id}", json=updated_data)

    print(f"Status: {response.status_code}")
    print(f"Response Data: {response.data.decode('utf-8')}")

    assert response.status_code == 200
    assert "Fornecedor atualizado com sucesso!" in response.get_data(as_text=True)
