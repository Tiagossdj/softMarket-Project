import pytest


@pytest.mark.compra
def test_realiza_compra_sucesso(client):
    compra_data = {
        "itens": [
            {"produto_id": 1, "quantidade": 2, "preco_unitario": 10.0},
            {"produto_id": 2, "quantidade": 3, "preco_unitario": 20.0},
        ],
        "data": "2025-03-18T10:00:00",
        "total": 80.0,  # Total da compra
        "forma_pagamento": "pix",
    }

    # Realizar a requisição POST para criar a compra
    response = client.post("/realizaCompra", json=compra_data)

    # Verificar se a compra foi criada com sucesso e obter o ID
    assert response.status_code == 201
    compra_id = response.json.get("id")
    assert compra_id is not None


@pytest.mark.compra
def test_cancelar_compra_sucesso(client):
    # Primeiro, criar a compra
    compra_data = {
        "itens": [
            {"produto_id": 1, "quantidade": 2, "preco_unitario": 10.0},
            {"produto_id": 2, "quantidade": 3, "preco_unitario": 20.0},
        ],
        "data": "2025-03-18T10:00:00",
        "total": 80.0,  # Total da compra
        "forma_pagamento": "pix",
    }

    # Realizar a requisição POST para criar a compra
    response = client.post("/realizaCompra", json=compra_data)
    assert response.status_code == 201
    compra_id = response.json.get("id")
    assert compra_id is not None

    # cancelamento da compra com o ID obtido
    cancelamento_response = client.put(f"/cancelarCompra/{compra_id}")
    assert cancelamento_response.status_code == 200
    assert cancelamento_response.json.get("message") == "Compra cancelada com sucesso!"
