from datetime import date, datetime
from flask import Blueprint, jsonify, request, send_file
import pandas as pd
from app.graph.grafico_pizza import gerar_grafico_pizza
from app.graph.grafico_barra import gerar_grafico_barra
from app.graph.grafico_linha import gerar_grafico_linha
from app.modelo_db import Compra, ItemCompra, PedidoEstoque, Produto, Fornecedor, db
from app.utils import gerar_excel
from flask import request

grafico_controller = Blueprint("grafico_controller", __name__)


# Função para pegar dados de relatório
def get_dados_relatorio(tipo_relatorio):
    if tipo_relatorio == "vendas":
        return {
            "Produto A": 2000,
            "Produto B": 1500,
            "Produto C": 5000,
            "Produto D": 3000,
        }
    elif tipo_relatorio == "estoque":
        return {
            "Produto A": 50,
            "Produto B": 20,
            "Produto C": 150,
            "Produto D": 10,
        }
    # Outros tipos de relatórios


gera_grafico_route = Blueprint("gera_grafico_route", __name__)


@grafico_controller.route("/gerar_excel", methods=["POST"])
def gerar_excel_relatorio():
    tipo_relatorio = request.json.get("tipo_relatorio")
    incluir_grafico = request.json.get("incluir_grafico", False)

    # Obter dados do relatório
    dados_relatorio = get_dados_relatorio(tipo_relatorio)

    # Criar DataFrame com os dados
    df = pd.DataFrame(
        {
            "Produto": list(dados_relatorio.keys()),
            "Valor": list(dados_relatorio.values()),
        }
    )

    # Gerar e retornar o arquivo Excel (com ou sem gráfico)
    return gerar_excel(
        dataframe=df,
        dados_grafico=dados_relatorio,
        incluir_grafico=incluir_grafico,
        nome_arquivo=f"{tipo_relatorio}_relatorio.xlsx",
        nome_planilha_dados="Relatório",
        nome_planilha_grafico="Gráfico",
    )


@gera_grafico_route.route("/grafico_vendas_por_produto", methods=["GET"])
def grafico_vendas_por_produto():
    try:
        # Consulta para pegar os dados de vendas
        compras = Compra.query.join(ItemCompra).join(Produto).all()

        if not compras:
            return {"message": "Nenhuma compra encontrada."}, 404

        # Monta os dados para o gráfico
        dados_grafico = {}
        for compra in compras:
            for item in compra.itens:
                nome_produto = item.produto.nome
                dados_grafico[nome_produto] = (
                    dados_grafico.get(nome_produto, 0) + item.quantidade
                )

        # Pega o tipo de gráfico (pode ser barra, pizza ou linha)
        tipo_grafico = request.args.get("tipo_grafico", "barra")  # Default é barra

        # Gera o gráfico com o tipo selecionado
        if tipo_grafico == "pizza":
            imagem = gerar_grafico_pizza(dados_grafico)
        elif tipo_grafico == "barra":
            imagem = gerar_grafico_barra(dados_grafico)
        elif tipo_grafico == "linha":
            imagem = gerar_grafico_linha(dados_grafico)
        else:
            return {
                "error": "Tipo de gráfico inválido"
            }, 400  # Caso o tipo de gráfico seja inválido

        # Retorna a imagem do gráfico gerado
        return send_file(imagem, mimetype="image/png")

    except Exception as e:
        return {"error": str(e)}, 500


@gera_grafico_route.route("/grafico_compras_por_produto", methods=["GET"])
def grafico_compras_por_produto():
    try:
        # Consulta para pegar os dados de compras
        compras = Compra.query.join(ItemCompra).join(Produto).all()

        if not compras:
            return {"message": "Nenhuma compra encontrada."}, 404

        # Monta os dados para o gráfico
        dados_grafico = {}
        for compra in compras:
            for item in compra.itens:
                nome_produto = item.produto.nome
                dados_grafico[nome_produto] = (
                    dados_grafico.get(nome_produto, 0) + item.quantidade
                )

        # Pega o tipo de gráfico (pode ser barra, pizza ou linha)
        tipo_grafico = request.args.get("tipo_grafico", "barra")  # Default é barra

        # Gera o gráfico com o tipo selecionado
        if tipo_grafico == "pizza":
            imagem = gerar_grafico_pizza(dados_grafico)
        elif tipo_grafico == "barra":
            imagem = gerar_grafico_barra(dados_grafico)
        elif tipo_grafico == "linha":
            imagem = gerar_grafico_linha(dados_grafico)
        else:
            return {"error": "Tipo de gráfico inválido"}, 400

        return send_file(imagem, mimetype="image/png")

    except Exception as e:
        return {"error": str(e)}, 500


@gera_grafico_route.route("/grafico_fornecedores", methods=["GET"])
def grafico_fornecedores():
    try:
        # Consulta os fornecedores e os produtos que eles fornecem
        fornecedores = Fornecedor.query.all()

        if not fornecedores:
            return {"message": "Nenhum fornecedor encontrado."}, 404

        # Monta os dados para o gráfico
        dados_grafico = {}

        for fornecedor in fornecedores:
            for produto in fornecedor.produtos:
                dados_grafico[fornecedor.nome] = (
                    dados_grafico.get(fornecedor.nome, 0) + 1
                )

        tipo_grafico = request.args.get("tipo_grafico", "barra")  # Default é barra

        # Gera gráfico com base no tipo solicitado
        if tipo_grafico == "pizza":
            imagem = gerar_grafico_pizza(dados_grafico)
        elif tipo_grafico == "barra":
            imagem = gerar_grafico_barra(dados_grafico)
        elif tipo_grafico == "linha":
            imagem = gerar_grafico_linha(dados_grafico)
        else:
            return {"error": "Tipo de gráfico inválido"}, 400

        return send_file(imagem, mimetype="image/png")

    except Exception as e:
        return {"error": str(e)}, 500


@gera_grafico_route.route("/grafico_estoque_baixo", methods=["GET"])
def grafico_estoque_baixo():
    try:
        # Consulta os produtos com estoque abaixo do mínimo
        produtos = Produto.query.filter(
            Produto.quantidade_em_estoque < Produto.estoque_minimo
        ).all()

        if not produtos:
            return {"message": "Nenhum produto com estoque baixo encontrado."}, 404

        # Monta os dados para o gráfico
        dados_grafico = {}
        for produto in produtos:
            dados_grafico[produto.nome] = produto.quantidade_em_estoque

        tipo_grafico = request.args.get("tipo_grafico", "barra")  # Default é barra

        # Gera gráfico com base no tipo solicitado
        if tipo_grafico == "pizza":
            imagem = gerar_grafico_pizza(dados_grafico)
        elif tipo_grafico == "barra":
            imagem = gerar_grafico_barra(dados_grafico)
        elif tipo_grafico == "linha":
            imagem = gerar_grafico_linha(dados_grafico)
        else:
            return {"error": "Tipo de gráfico inválido"}, 400

        return send_file(imagem, mimetype="image/png")

    except Exception as e:
        return {"error": str(e)}, 500


@gera_grafico_route.route("/grafico_vendas_dia", methods=["GET"])
def grafico_vendas_dia():
    try:
        # Pega a data passada no formato yyyy-mm-dd
        data_str = request.args.get("data")
        if data_str:
            try:
                data_filtro = datetime.strptime(data_str, "%Y-%m-%d").date()
            except ValueError:
                return (
                    jsonify({"error": "Formato de data inválido. Use YYYY-MM-DD."}),
                    400,
                )
        else:
            data_filtro = date.today()  # Pega a data atual se não fornecer data

        # Consulta as vendas do dia
        vendas = Compra.query.filter(db.func.date(Compra.data) == data_filtro).all()

        if not vendas:
            return {"message": "Nenhuma venda encontrada para o dia especificado."}, 404

        # Monta os dados para o gráfico
        dados_grafico = {}
        for venda in vendas:
            for item in venda.itens:
                nome_produto = item.produto.nome
                dados_grafico[nome_produto] = (
                    dados_grafico.get(nome_produto, 0) + item.quantidade
                )

        tipo_grafico = request.args.get("tipo_grafico", "barra")  # Default é barra

        # Gera gráfico com base no tipo solicitado
        if tipo_grafico == "pizza":
            imagem = gerar_grafico_pizza(dados_grafico)
        elif tipo_grafico == "barra":
            imagem = gerar_grafico_barra(dados_grafico)
        elif tipo_grafico == "linha":
            imagem = gerar_grafico_linha(dados_grafico)
        else:
            return {"error": "Tipo de gráfico inválido"}, 400

        return send_file(imagem, mimetype="image/png")

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@gera_grafico_route.route("/grafico_pedidos_estoque_produto", methods=["GET"])
def grafico_pedidos_estoque_produto():
    try:
        # Consulta de pedidos de estoque
        pedidos = PedidoEstoque.query.all()

        if not pedidos:
            return {"message": "Nenhum pedido de estoque encontrado."}, 404

        # Monta os dados para o gráfico
        dados_grafico = {}

        for pedido in pedidos:
            nome_produto = (
                pedido.produto.nome if pedido.produto else "Produto não encontrado"
            )
            dados_grafico[nome_produto] = (
                dados_grafico.get(nome_produto, 0) + pedido.quantidade
            )

        tipo_grafico = request.args.get("tipo_grafico", "barra")  # Default é barra

        # Gera gráfico com base no tipo solicitado
        if tipo_grafico == "pizza":
            imagem = gerar_grafico_pizza(dados_grafico)
        elif tipo_grafico == "barra":
            imagem = gerar_grafico_barra(dados_grafico)
        elif tipo_grafico == "linha":
            imagem = gerar_grafico_linha(dados_grafico)
        else:
            return {"error": "Tipo de gráfico inválido"}, 400

        return send_file(imagem, mimetype="image/png")

    except Exception as e:
        return {"error": str(e)}, 500
