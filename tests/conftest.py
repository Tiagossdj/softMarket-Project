import pytest
import sys
import os

# Adiciona o diretório raiz do projeto ao PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app, db
from app.modelo_db import Fornecedor, Produto  # Importando o modelo Produto


# Fixture para os testes de Compra e Estoque
@pytest.fixture
def client(request):
    # Criação do app de teste
    app = create_app()

    # Configuração do banco de dados de teste
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "postgresql://postgres:123456@localhost:5432/test_db"  # Banco de dados de teste
    )

    # Criação das tabelas no banco de dados de teste
    with app.app_context():
        db.create_all()

        # Verifica se o teste atual é marcado com a marca 'estoque'
        if "estoque" in request.keywords:
            # Criação de fornecedor e produtos apenas para os testes de estoque
            fornecedor = Fornecedor(
                nome="Fornecedor Teste Estoque",
                cnpj="98765432000195",
                contato="estoque@teste.com",
            )
            db.session.add(fornecedor)
            db.session.commit()  # Commit para garantir que o fornecedor tenha um ID atribuído

            # Criação de produtos de teste com fornecedor_id
            produto1 = Produto(
                nome="Produto Estoque 1",
                preco=10.0,
                quantidade_em_estoque=50,
                fornecedor_id=fornecedor.id,
            )
            produto2 = Produto(
                nome="Produto Estoque 2",
                preco=20.0,
                quantidade_em_estoque=30,
                fornecedor_id=fornecedor.id,
            )

            # Produto com estoque baixo (abaixo de 30)
            produto_baixo_estoque = Produto(
                nome="Produto Estoque Baixo",
                preco=5.0,
                quantidade_em_estoque=10,  # Estoque baixo
                fornecedor_id=fornecedor.id,
            )

            db.session.add(produto1)
            db.session.add(produto2)
            db.session.add(
                produto_baixo_estoque
            )  # Adiciona o produto com estoque baixo

            # Commit para salvar os produtos
            db.session.commit()

        # Verifica se o teste atual é marcado com a marca 'compra'
        if "compra" in request.keywords:
            # Criação de fornecedor e produtos apenas para os testes de compra
            fornecedor = Fornecedor(
                nome="Fornecedor Teste Compra",
                cnpj="12345678000195",
                contato="compra@teste.com",
            )
            db.session.add(fornecedor)
            db.session.commit()

            # Criação de produtos de teste com fornecedor_id
            produto1 = Produto(
                nome="Produto Compra 1",
                preco=15.0,
                quantidade_em_estoque=100,
                fornecedor_id=fornecedor.id,
            )
            produto2 = Produto(
                nome="Produto Compra 2",
                preco=25.0,
                quantidade_em_estoque=100,
                fornecedor_id=fornecedor.id,
            )
            db.session.add(produto1)
            db.session.add(produto2)

            # Commit para salvar os produtos
            db.session.commit()

    # Criação do client de teste
    with app.test_client() as client:
        yield client

    # Limpeza após o teste
    with app.app_context():
        db.session.remove()  # Remove a sessão ativa do banco de dados
        db.drop_all()  # Dropa todas as tabelas para limpar o banco
