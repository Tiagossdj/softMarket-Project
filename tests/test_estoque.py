import pytest

from app.modelo_db import Fornecedor, PedidoEstoque, Produto, db


@pytest.mark.estoque
def test_cadastrar_pedido_estoque(client):
    # Seu código para testar pedidos de estoque
    data = {
        "produto_id": 1,
        "quantidade": 50,
        "fornecedor_id": 1,
    }

    response = client.post("/pedidoEstoque", json=data)

    # Verificar resposta
    assert response.status_code == 201


# @pytest.mark.estoque
# def test_visualizar_estoque(client):
#     response = client.get("/estoque")
#     assert response.status_code == 200
#     # Verificar se a resposta contém os dados esperados (ajustar conforme necessário)
#     data = response.get_json()
#     assert isinstance(data, list)
#     assert "produto_id" in data[0]
#     assert "nome" in data[0]
#     assert "quantidade_em_estoque" in data[0]
#     assert "fornecedor" in data[0]


@pytest.mark.estoque
def test_baixa_estoque(client):
    # Dados para diminuir o estoque
    data = {
        "produto_id": 1,
        "quantidade": 10,
    }

    response = client.post("/baixaEstoque", json=data)
    assert response.status_code == 200
    assert response.get_json()["message"] == "Estoque ajustado com sucesso!"

    # Verificar se o estoque foi realmente atualizado (ajustar conforme necessário)
    produto = db.session.get(Produto, 1)
    assert (
        produto.quantidade_em_estoque == 40
    )  # Considerando que o estoque inicial era 50


# @pytest.mark.estoque
# def test_estoque_baixo(client):  # o cliente aqui
#     # Garantir que há pelo menos um produto com estoque abaixo do limite
#     fornecedor = Fornecedor(
#         nome="Fornecedor Teste", cnpj="12345678000195", contato="contato@teste.com"
#     )
#     db.session.add(fornecedor)
#     db.session.commit()  # Garantir que o fornecedor seja adicionado ao banco de dados

#     # Criando um produto com estoque baixo
#     produto_baixo_estoque = Produto(
#         nome="Produto Estoque Baixo",
#         preco=5.0,
#         quantidade_em_estoque=10,  # Definindo estoque baixo
#         fornecedor_id=fornecedor.id,
#     )
#     db.session.add(produto_baixo_estoque)
#     db.session.commit()  # Garantir que a transação seja confirmada

#     # Agora que temos um produto com estoque baixo, podemos realizar o teste
#     response = client.get("/estoqueBaixo")  # Realiza a requisição HTTP
#     assert response.status_code == 200
#     data = response.get_json()

#     assert isinstance(data, list)
#     assert (
#         len(data) > 0
#     )  # Certifique-se de que há pelo menos um produto com estoque baixo
#     assert "produto_id" in data[0]
#     assert "nome" in data[0]
#     assert "quantidade_em_estoque" in data[0]


@pytest.mark.estoque
def test_listar_pedidos_estoque(client):
    response = client.get("/pedidosEstoque")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data["pedidos"], list)
    if len(data["pedidos"]) > 0:
        assert "id" in data["pedidos"][0]
        assert "produto_id" in data["pedidos"][0]
        assert "quantidade" in data["pedidos"][0]
        assert "fornecedor_id" in data["pedidos"][0]
        assert "produto_nome" in data["pedidos"][0]
        assert "fornecedor_nome" in data["pedidos"][0]


# @pytest.mark.estoque
# def test_editar_pedido_estoque(client):
#     # Supondo que já existe um pedido de estoque com id 1
#     data = {
#         "produto_id": 1,
#         "quantidade": 100,
#         "fornecedor_id": 1,
#     }

#     response = client.put("/pedidoEstoque/1", json=data)
#     assert response.status_code == 200
#     assert response.get_json()["message"] == "Pedido de estoque atualizado com sucesso!"

#     # Verificar se os dados do pedido foram atualizados no banco (ajustar conforme necessário)
#     pedido = PedidoEstoque.query.get(1)
#     assert pedido.quantidade == 100


# @pytest.mark.estoque
# def test_excluir_pedido_estoque(client):
#     # Supondo que já existe um pedido de estoque com id 1
#     response = client.delete("/pedidoEstoque/1")
#     assert response.status_code == 200
#     assert response.get_json()["message"] == "Pedido de estoque excluído com sucesso!"

#     # Verificar se o pedido foi realmente excluído (ajustar conforme necessário)
#     pedido = PedidoEstoque.query.get(1)
#     assert pedido is None  # O pedido deve ser excluído
