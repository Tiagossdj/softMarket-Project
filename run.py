from app import create_app
from app.modelo_db import Fornecedor, Produto, db

# Criar a aplicação
app = create_app()

from flask import Flask, render_template, redirect, url_for
from app.controllers import (
    geraGrafico,
    usuario,
    cadastraProduto,
    pedidoEstoque,
    cadastraFornecedor,
    realizaCompra,
    relatórios,
)

app = Flask(__name__)

# Rota para login
app.add_url_rule("/login", view_func=usuario.login.show_login)

# Rota para register
app.add_url_rule("/register", view_func=usuario.register.show_register)

# Rota para o Dashboard
app.add_url_rule("/dashboard", view_func=dashboard.show_dashboard)  # type: ignore

# Rota para Produtos
app.add_url_rule("/produtos", view_func=Produto.show_produtos)

# Rota para Estoque
app.add_url_rule("/estoque", view_func=pedidoEstoque.show_estoque)

# Rota para Fornecedores
app.add_url_rule("/fornecedores", view_func=Fornecedor().show_fornecedores)

# Rota para Vendas
app.add_url_rule("/vendas", view_func=realizaCompra.show_vendas)

# Rota para Relatórios
app.add_url_rule("/relatorios", view_func=relatórios.show_relatorios)

if __name__ == "__main__":
    app.run(debug=True)
