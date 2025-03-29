import pytest
from datetime import datetime
from app.modelo_db import db


@pytest.mark.compra
def test_relatorio_vendas_excel(client):
    # Criando uma venda de teste
    with client.application.app_context():
        from app.modelo_db import Compra, ItemCompra

        venda = Compra(total=200.0, data=datetime(2025, 3, 19, 14, 30))
        db.session.add(venda)
        db.session.commit()

        item_compra = ItemCompra(
            quantidade=2,
            preco_unitario=100.0,
            subtotal=200.0,
            produto_id=1,
            compra_id=venda.id,
        )
        db.session.add(item_compra)
        db.session.commit()

    # Realizando a requisição
    response = client.get(
        "/relatorio_vendas_excel?data_inicio=2025-03-19&data_fim=2025-03-19"
    )

    # Verificando a resposta
    assert response.status_code == 200
    assert "relatorio_vendas.xlsx" in response.headers["Content-Disposition"]


@pytest.mark.compra
def test_relatorio_compras_excel(client):
    # Criando uma compra de teste
    with client.application.app_context():
        from app.modelo_db import Compra, Produto, ItemCompra

        compra = Compra(total=150.0, data=datetime(2025, 3, 19, 15, 0))
        db.session.add(compra)
        db.session.commit()

        item_compra = ItemCompra(
            quantidade=3,
            preco_unitario=50.0,
            subtotal=150.0,
            produto_id=1,
            compra_id=compra.id,
        )
        db.session.add(item_compra)
        db.session.commit()

    # Realizando a requisição
    response = client.get("/relatorio_compras_excel")

    # Verificando a resposta
    assert response.status_code == 200
    assert "relatorio_compras.xlsx" in response.headers["Content-Disposition"]


@pytest.mark.estoque
def test_relatorio_fornecedores_excel(client):
    # Criando um fornecedor de teste
    with client.application.app_context():
        from app.modelo_db import Fornecedor, PedidoEstoque, Produto

        fornecedor = Fornecedor(
            nome="Fornecedor Teste", cnpj="1234567890", contato="contato@teste.com"
        )
        db.session.add(fornecedor)
        db.session.commit()

        produto = Produto(
            nome="Produto Fornecedor",
            preco=30.0,
            quantidade_em_estoque=10,
            estoque_minimo=40,
            fornecedor_id=fornecedor.id,
        )
        db.session.add(produto)
        db.session.commit()

        pedido = PedidoEstoque(
            produto_id=produto.id, fornecedor_id=fornecedor.id, quantidade=5
        )
        db.session.add(pedido)
        db.session.commit()

    # Realizando a requisição
    response = client.get("/relatorio_fornecedores_excel")

    # Verificando a resposta
    assert response.status_code == 200
    assert "relatorio_fornecedores.xlsx" in response.headers["Content-Disposition"]


@pytest.mark.estoque
def test_relatorio_estoque_excel(client):
    # Criando produtos para o estoque de teste
    with client.application.app_context():
        from app.modelo_db import Produto

        produto = Produto(
            nome="Produto Estoque",
            preco=20.0,
            quantidade_em_estoque=50,
            estoque_minimo=25,
            fornecedor_id=1,
        )
        db.session.add(produto)
        db.session.commit()

    # Realizando a requisição
    response = client.get("/relatorio_estoque_excel")

    # Verificando a resposta
    assert response.status_code == 200
    assert "relatorio_estoque.xlsx" in response.headers["Content-Disposition"]


@pytest.mark.compra
def test_relatorio_vendas_dia_excel(client):
    with client.application.app_context():
        from app.modelo_db import Compra, Produto, ItemCompra
        from datetime import datetime

        produto = Produto(
            nome="Produto Teste",
            preco=50.0,
            quantidade_em_estoque=20,
            estoque_minimo=50,
            fornecedor_id=1,
        )
        db.session.add(produto)
        db.session.commit()

        data_teste = datetime(2025, 3, 19, 16, 0)
        venda = Compra(total=150.0, data=data_teste)
        db.session.add(venda)
        db.session.commit()

        item_compra = ItemCompra(
            quantidade=3,
            preco_unitario=50.0,
            subtotal=150.0,
            produto_id=produto.id,
            compra_id=venda.id,
        )
        db.session.add(item_compra)
        db.session.commit()

        data_param = data_teste.strftime("%d-%m-%Y")

        # Testando a rota com a data criada
        response = client.get(f"/relatorio_vendas_dia_excel?data_inicio={data_param}")

        # Verificando se a resposta é bem-sucedida e retorna um arquivo Excel
        assert response.status_code == 200
        assert (
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            in response.content_type
        )


@pytest.mark.estoque
def test_relatorio_estoque_baixo_excel(client):
    with client.application.app_context():
        from app.modelo_db import Produto

        produto = Produto(
            nome="Produto Estoque Baixo",
            preco=5.0,
            quantidade_em_estoque=10,
            estoque_minimo=15,
            fornecedor_id=1,
        )
        db.session.add(produto)
        db.session.commit()

    # Realizando a requisição
    response = client.get("/relatorio_estoque_baixo_excel")

    # Verificando a resposta
    assert response.status_code == 200
    assert "relatorio_estoque_baixo.xlsx" in response.headers["Content-Disposition"]


@pytest.mark.estoque
def test_relatorio_pedidos_estoque_excel(client):
    # Criando pedidos de estoque de teste
    with client.application.app_context():
        from app.modelo_db import PedidoEstoque, Produto, Fornecedor

        fornecedor = Fornecedor(
            nome="Fornecedor Teste", cnpj="1234567890", contato="contato@teste.com"
        )
        db.session.add(fornecedor)
        db.session.commit()

        produto = Produto(
            nome="Produto Teste",
            preco=30.0,
            quantidade_em_estoque=20,
            estoque_minimo=40,
            fornecedor_id=fornecedor.id,
        )
        db.session.add(produto)
        db.session.commit()

        pedido = PedidoEstoque(
            produto_id=produto.id, fornecedor_id=fornecedor.id, quantidade=10
        )
        db.session.add(pedido)
        db.session.commit()

    # Realizando a requisição
    response = client.get("/relatorio_pedidos_estoque_excel")

    # Verificando a resposta
    assert response.status_code == 200
    assert "relatorio_pedidos_estoque.xlsx" in response.headers["Content-Disposition"]
