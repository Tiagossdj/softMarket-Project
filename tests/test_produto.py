from app.modelo_db import db


def test_cadastrar_produto(client):
    with client.application.app_context():
        # Importe o modelo de Fornecedor
        from app.modelo_db import Fornecedor

        # Crie um fornecedor de teste
        fornecedor = Fornecedor(
            nome="Fornecedor Teste", cnpj="12345678", contato="1234567890"
        )
        db.session.add(fornecedor)
        db.session.commit()
        fornecedor_id = fornecedor.id

    # Dados para o cadastro do produto
    produto_data = {
        "nome": "Produto Teste",
        "preco": 100.0,
        "quantidade_em_estoque": 50,
        "fornecedor_id": fornecedor_id,
        "estoque_minimo": 23,
    }

    # Realizando a requisição para cadastrar o produto
    response = client.post("/produto", json=produto_data)

    # Imprime a resposta completa para depuração (log especifico)
    print(f"Status: {response.status_code}")
    print(f"Response Data: {response.data.decode('utf-8')}")

    # Verificando o status e a resposta
    assert response.status_code == 201


def test_excluir_produto(client):
    # Criando um produto de teste
    with client.application.app_context():
        from app.modelo_db import Produto, Fornecedor

        # Criando fornecedor de teste
        fornecedor = Fornecedor(
            nome="Fornecedor Teste", cnpj="12345678", contato="1234567890"
        )
        db.session.add(fornecedor)
        db.session.commit()

        # Criando produto de teste
        produto = Produto(
            nome="Produto Teste",
            preco=100.0,
            quantidade_em_estoque=50,
            estoque_minimo=40,
            fornecedor_id=fornecedor.id,
        )
        db.session.add(produto)
        db.session.commit()
        produto_id = produto.id

    # Realizando a requisição para excluir o produto
    response = client.delete(f"/produto/{produto_id}")

    # Verificando a resposta
    assert response.status_code == 200
    assert "Produto excluído com sucesso!" in response.json["message"]


def test_listar_produtos(client):
    # Criando produtos de teste
    with client.application.app_context():
        from app.modelo_db import Produto, Fornecedor

        fornecedor = Fornecedor(
            nome="Fornecedor Teste", cnpj="12345678", contato="1234567890"
        )
        db.session.add(fornecedor)
        db.session.commit()

        produto1 = Produto(
            nome="Produto 1",
            preco=50.0,
            quantidade_em_estoque=10,
            estoque_minimo=40,
            fornecedor_id=fornecedor.id,
        )
        produto2 = Produto(
            nome="Produto 2",
            preco=30.0,
            quantidade_em_estoque=5,
            estoque_minimo=40,
            fornecedor_id=fornecedor.id,
        )
        db.session.add_all([produto1, produto2])
        db.session.commit()

    # Realizando a requisição para listar os produtos
    response = client.get("/produtos")

    # Verificando a resposta
    assert response.status_code == 200
    assert len(response.json) == 2  # Espera-se 2 produtos


# def test_obter_produto_por_id(client):
#     # Criando um produto de teste
#     with client.application.app_context():
#         from app.modelo_db import Produto, Fornecedor

#         fornecedor = Fornecedor(
#             nome="Fornecedor Teste", cnpj="12345678", contato="1234567890"
#         )
#         db.session.add(fornecedor)
#         db.session.commit()

#         produto = Produto(
#             nome="Produto Teste",
#             preco=100.0,
#             quantidade_em_estoque=50,
#             estoque_minimo=40,
#             fornecedor_id=fornecedor.id,
#         )
#         db.session.add(produto)
#         db.session.commit()
#         produto_id = produto.id

#     # Realizando a requisição para obter o produto por ID
#     response = client.get(f"/produto/{produto_id}")

#     # Verificando a resposta
#     assert response.status_code == 200
#     assert response.json["id"] == produto_id
#     assert response.json["nome"] == "Produto Teste"


def test_atualizar_estoque_produto(client):
    # Criando um produto de teste
    with client.application.app_context():
        from app.modelo_db import Produto, Fornecedor

        fornecedor = Fornecedor(
            nome="Fornecedor Teste", cnpj="12345678", contato="1234567890"
        )
        db.session.add(fornecedor)
        db.session.commit()

        produto = Produto(
            nome="Produto Teste",
            preco=100.0,
            quantidade_em_estoque=50,
            estoque_minimo=40,
            fornecedor_id=fornecedor.id,
        )
        db.session.add(produto)
        db.session.commit()
        produto_id = produto.id

    # Dados para a atualização do estoque
    estoque_data = {"quantidade": 10}

    # Realizando a requisição para atualizar o estoque
    response = client.put(f"/produto/{produto_id}/estoque", json=estoque_data)

    # Verificando a resposta
    assert response.status_code == 200
    assert "Estoque atualizado com sucesso!" in response.json["message"]


# def test_atualizar_produto(client):
#     # Criando um produto de teste
#     with client.application.app_context():
#         from app.modelo_db import Produto, Fornecedor

#         fornecedor = Fornecedor(
#             nome="Fornecedor Teste", cnpj="12345678", contato="1234567890"
#         )
#         db.session.add(fornecedor)
#         db.session.commit()

#         produto = Produto(
#             nome="Produto Teste",
#             preco=100.0,
#             quantidade_em_estoque=50,
#             estoque_minimo=40,
#             fornecedor_id=fornecedor.id,
#         )
#         db.session.add(produto)
#         db.session.commit()
#         produto_id = produto.id

#     # Dados para a atualização do produto
#     atualizar_data = {
#         "nome": "Produto Teste Atualizado",
#         "preco": 120.0,
#         "quantidade_em_estoque": 60,
#     }

#     # Realizando a requisição para atualizar o produto
#     response = client.put(f"/produto/{produto_id}/atualizar", json=atualizar_data)

#     # Verificando a resposta
#     assert response.status_code == 200
#     assert "Produto atualizado com sucesso!" in response.json["message"]
