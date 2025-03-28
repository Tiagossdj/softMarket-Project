from datetime import date, datetime
from flask import Blueprint, request, jsonify
from app.modelo_db import Compra, Fornecedor, ItemCompra, PedidoEstoque, Produto, db
import pandas as pd
from app.utils.gerar_excel import gerar_excel
from sqlalchemy.orm import joinedload
import logging


relatorio_route = Blueprint("relatorio", __name__)


@relatorio_route.route("/relatorio_vendas_excel", methods=["GET"])
def relatorio_vendas_excel():
    try:
        data_inicio = request.args.get("data_inicio")
        data_fim = request.args.get("data_fim")

        if data_inicio:
            data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d")
        if data_fim:
            data_fim = datetime.strptime(data_fim, "%Y-%m-%d")

        query = Compra.query
        if data_inicio and data_fim:
            query = query.filter(Compra.data >= data_inicio, Compra.data <= data_fim)
        elif data_inicio:
            query = query.filter(Compra.data >= data_inicio)
        elif data_fim:
            query = query.filter(Compra.data <= data_fim)

        vendas = query.all()

        dados = [
            {
                "ID": venda.id,
                "Data": venda.data.strftime("%d/%m/%Y %H:%M"),
                "Total (R$)": f"{venda.total:.2f}",
            }
            for venda in vendas
        ]

        total_geral = sum(venda.total for venda in vendas)
        dados.append(
            {"ID": "", "Data": "Total Geral", "Total (R$)": f"{total_geral:.2f}"}
        )

        df = pd.DataFrame(dados)
        return gerar_excel(
            df, nome_arquivo="relatorio_vendas.xlsx", nome_planilha="Vendas"
        )

    except Exception as e:
        return jsonify({"error": f"Ocorreu um erro: {str(e)}"}), 500


@relatorio_route.route("/relatorio_compras_excel", methods=["GET"])
def relatorio_compras_excel():
    try:
        compras = Compra.query.join(ItemCompra).join(Produto).all()
        if not compras:
            return jsonify({"message": "Nenhuma compra encontrada."}), 404

        dados = []
        for compra in compras:
            for item in compra.itens:
                dados.append(
                    {
                        "ID Compra": compra.id,
                        "Produto": item.produto.nome,
                        "Quantidade": item.quantidade,
                        "Preço Unitário": item.preco_unitario,
                        "Subtotal": item.subtotal,
                    }
                )

        df = pd.DataFrame(dados)
        return gerar_excel(
            df, nome_arquivo="relatorio_compras.xlsx", nome_planilha="Compras"
        )
    except Exception as e:
        return jsonify({"error": f"Ocorreu um erro: {str(e)}"}), 500


# Relatórios de fornecedores, lista e todas informações associadas a ele.
@relatorio_route.route("/relatorio_fornecedores_excel", methods=["GET"])
def relatorio_fornecedores_excel():
    try:
        fornecedores = Fornecedor.query.join(PedidoEstoque).join(Produto).all()

        if not fornecedores:
            return jsonify({"message": "Nenhum fornecedor encontrado."}), 404

        dados = []
        for fornecedor in fornecedores:
            for pedido in fornecedor.pedidos_estoque:
                dados.append(
                    {
                        "ID Fornecedor": fornecedor.id,
                        "Nome": fornecedor.nome,
                        "CNPJ": fornecedor.cnpj,
                        "Contato": fornecedor.contato,
                        "Produto Pedido": pedido.produto.nome,
                        "Quantidade Pedido": pedido.quantidade,
                    }
                )

        df = pd.DataFrame(dados)
        return gerar_excel(
            df, nome_arquivo="relatorio_fornecedores.xlsx", nome_planilha="Fornecedores"
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Relatório de estoque, com a quantidade disponivel e o valor total de cada produto
@relatorio_route.route("/relatorio_estoque_excel", methods=["GET"])
def relatorio_estoque_excel():
    try:
        produtos = Produto.query.all()

        if not produtos:
            return jsonify({"message": "Nenhum produto encontrado no estoque."}), 404

        dados = []
        for produto in produtos:
            valor_total = produto.preco * produto.quantidade_em_estoque
            dados.append(
                {
                    "Produto": produto.nome,
                    "Quantidade em Estoque": produto.quantidade_em_estoque,
                    "Preço Unitário (R$)": f"{produto.preco:.2f}",
                    "Valor Total em Estoque (R$)": f"{valor_total:.2f}",
                }
            )

        df = pd.DataFrame(dados)
        return gerar_excel(
            df, nome_arquivo="relatorio_estoque.xlsx", nome_planilha="Estoque"
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# endpoint para gerar o relatório de vendas do dia em Excel
@relatorio_route.route("/relatorio_vendas_dia_excel", methods=["GET"])
def relatorio_vendas_dia_excel():
    try:
        # Pega a data enviada na requisição, agora usando data_inicio
        data_str = request.args.get("data_inicio")

        if data_str:
            try:
                # Mudança no formato de parsing para DD-MM-YYYY
                data_filtro = datetime.strptime(data_str, "%d-%m-%Y").date()
            except ValueError:
                return (
                    jsonify({"error": "Formato de data inválido. Use DD-MM-YYYY."}),
                    400,
                )
        else:
            data_filtro = date.today()

        logging.debug(f"Filtrando vendas para a data: {data_filtro}")

        # Mantém a mesma lógica de consulta
        vendas = (
            Compra.query.filter(db.func.date(Compra.data) == data_filtro)
            .options(joinedload(Compra.itens))  # Para carregar os itens da compra
            .all()
        )

        logging.debug(f"Total de vendas encontradas: {len(vendas)}")

        dados = []
        for venda in vendas:
            logging.debug(f"Processando venda ID: {venda.id}")
            for item in venda.itens:
                logging.debug(
                    f"Item: {item.produto.nome}, Quantidade: {item.quantidade}"
                )
                dados.append(
                    {
                        "ID Venda": venda.id,
                        "Data": venda.data.strftime("%d/%m/%Y %H:%M"),
                        "Produto": item.produto.nome,
                        "Quantidade": item.quantidade,
                        "Preço Unitário (R$)": f"{item.preco_unitario:.2f}",
                        "Subtotal (R$)": f"{item.subtotal:.2f}",
                        "Total da Venda (R$)": f"{venda.total:.2f}",
                    }
                )

        logging.debug(f"Total de itens de venda: {len(dados)}")

        # Verifica se há dados antes de criar o DataFrame
        if not dados:
            logging.warning("Nenhum dado encontrado para a data especificada")
            return jsonify({"message": "Sem vendas para a data selecionada"}), 404

        # Converte os dados para um DataFrame
        df = pd.DataFrame(dados)

        # Chama a função para gerar e retornar o arquivo Excel
        arquivo_excel = gerar_excel(df, "relatorio_vendas_dia.xlsx", "Vendas do Dia")

        # Retorna o arquivo como resposta para download
        return arquivo_excel

    except Exception as e:
        logging.error(f"Erro ao gerar relatório: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500


# relatório de produtos com estoque baixo (colocar límite definido!!!)
@relatorio_route.route("/relatorio_estoque_baixo_excel", methods=["GET"])
def relatorio_estoque_baixo_excel():
    try:
        produtos = Produto.query.filter(
            Produto.quantidade_em_estoque < Produto.estoque_minimo
        ).all()

        if not produtos:
            return (
                jsonify({"message": "Nenhum produto com estoque baixo encontrado."}),
                200,
            )

        dados = []
        for produto in produtos:
            dados.append(
                {
                    "ID Produto": produto.id,
                    "Nome": produto.nome,
                    "Quantidade em Estoque": produto.quantidade_em_estoque,
                    "Estoque Mínimo": produto.estoque_minimo,
                    "Preço (R$)": f"{produto.preco:.2f}",
                    "Fornecedor": (
                        produto.fornecedor.nome
                        if produto.fornecedor
                        else "Não encontrado"
                    ),
                }
            )

        df = pd.DataFrame(dados)
        return gerar_excel(
            df,
            nome_arquivo="relatorio_estoque_baixo.xlsx",
            nome_planilha="Estoque Baixo",
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@relatorio_route.route("/relatorio_pedidos_estoque_excel", methods=["GET"])
def relatorio_pedidos_estoque_excel():
    try:
        # Usando joinedload para carregar os relacionamentos
        pedidos = PedidoEstoque.query.options(
            joinedload(PedidoEstoque.produto), joinedload(PedidoEstoque.fornecedor)
        ).all()

        if not pedidos:
            return jsonify({"message": "Nenhum pedido de estoque encontrado."}), 200

        dados = []
        for pedido in pedidos:
            dados.append(
                {
                    "ID Pedido": pedido.id,
                    "Produto": (
                        pedido.produto.nome if pedido.produto else "Não encontrado"
                    ),
                    "Quantidade": pedido.quantidade,
                    "Data do Pedido": (
                        pedido.data_pedido.strftime("%d/%m/%Y")
                        if pedido.data_pedido
                        else "Não registrado"
                    ),
                    "Fornecedor": (
                        pedido.fornecedor.nome
                        if pedido.fornecedor
                        else "Não encontrado"
                    ),
                }
            )

        df = pd.DataFrame(dados)
        return gerar_excel(
            df,
            nome_arquivo="relatorio_pedidos_estoque.xlsx",
            nome_planilha="Pedidos de Estoque",
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Novo endpoint JSON para vendas do dia
@relatorio_route.route("/relatorio_vendas_dia_json", methods=["GET"])
def relatorio_vendas_dia_json():
    try:
        data_str = request.args.get("data_inicio")
        if data_str:
            try:
                data_filtro = datetime.strptime(data_str, "%Y-%m-%d").date()
            except ValueError:
                return (
                    jsonify({"error": "Formato de data inválido. Use YYYY-MM-DD."}),
                    400,
                )
        else:
            data_filtro = date.today()

        vendas = Compra.query.filter(db.func.date(Compra.data) == data_filtro).all()

        dados = []
        for venda in vendas:
            for item in venda.itens:
                dados.append(
                    {
                        "ID Venda": venda.id,
                        "Data": venda.data.strftime("%d/%m/%Y %H:%M"),
                        "Produto": item.produto.nome,
                        "Quantidade": item.quantidade,
                        "Preço Unitário (R$)": f"{item.preco_unitario:.2f}",
                        "Subtotal (R$)": f"{item.subtotal:.2f}",
                        "Total da Venda (R$)": f"{venda.total:.2f}",
                    }
                )

        return jsonify(dados)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Novo endpoint JSON para estoque
@relatorio_route.route("/relatorio_estoque_json", methods=["GET"])
def relatorio_estoque_json():
    try:
        produtos = Produto.query.all()

        if not produtos:
            return jsonify([])

        dados = []
        for produto in produtos:
            valor_total = produto.preco * produto.quantidade_em_estoque
            dados.append(
                {
                    "Produto": produto.nome,
                    "Quantidade em Estoque": produto.quantidade_em_estoque,
                    "Preço Unitário (R$)": f"{produto.preco:.2f}",
                    "Valor Total em Estoque (R$)": f"{valor_total:.2f}",
                }
            )

        return jsonify(dados)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Novo endpoint JSON para estoque baixo
@relatorio_route.route("/relatorio_estoque_baixo_json", methods=["GET"])
def relatorio_estoque_baixo_json():
    try:
        produtos = Produto.query.filter(
            Produto.quantidade_em_estoque < Produto.estoque_minimo
        ).all()

        if not produtos:
            return jsonify([])

        dados = []
        for produto in produtos:
            dados.append(
                {
                    "ID Produto": produto.id,
                    "Nome": produto.nome,
                    "Quantidade em Estoque": produto.quantidade_em_estoque,
                    "Estoque Mínimo": produto.estoque_minimo,
                    "Preço (R$)": f"{produto.preco:.2f}",
                    "Fornecedor": (
                        produto.fornecedor.nome
                        if produto.fornecedor
                        else "Não encontrado"
                    ),
                }
            )

        return jsonify(dados)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Novo endpoint JSON para vendas
@relatorio_route.route("/relatorio_vendas_json", methods=["GET"])
def relatorio_vendas_json():
    try:
        data_inicio = request.args.get("data_inicio")
        data_fim = request.args.get("data_fim")

        if data_inicio:
            data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d")
        if data_fim:
            data_fim = datetime.strptime(data_fim, "%Y-%m-%d")

        query = Compra.query
        if data_inicio and data_fim:
            query = query.filter(Compra.data >= data_inicio, Compra.data <= data_fim)
        elif data_inicio:
            query = query.filter(Compra.data >= data_inicio)
        elif data_fim:
            query = query.filter(Compra.data <= data_fim)

        vendas = query.all()

        dados = [
            {
                "ID": venda.id,
                "Data": venda.data.strftime("%d/%m/%Y %H:%M"),
                "Total (R$)": f"{venda.total:.2f}",
            }
            for venda in vendas
        ]

        return jsonify(dados)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Novos endpoints seguindo o mesmo padrão para os outros relatórios
@relatorio_route.route("/relatorio_compras_json", methods=["GET"])
def relatorio_compras_json():
    try:
        compras = Compra.query.join(ItemCompra).join(Produto).all()
        if not compras:
            return jsonify([])

        dados = []
        for compra in compras:
            for item in compra.itens:
                dados.append(
                    {
                        "ID Compra": compra.id,
                        "Produto": item.produto.nome,
                        "Quantidade": item.quantidade,
                        "Preço Unitário": item.preco_unitario,
                        "Subtotal": item.subtotal,
                    }
                )

        return jsonify(dados)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@relatorio_route.route("/relatorio_fornecedores_json", methods=["GET"])
def relatorio_fornecedores_json():
    try:
        fornecedores = Fornecedor.query.join(PedidoEstoque).join(Produto).all()

        if not fornecedores:
            return jsonify([])

        dados = []
        for fornecedor in fornecedores:
            for pedido in fornecedor.pedidos_estoque:
                dados.append(
                    {
                        "ID Fornecedor": fornecedor.id,
                        "Nome": fornecedor.nome,
                        "CNPJ": fornecedor.cnpj,
                        "Contato": fornecedor.contato,
                        "Produto Pedido": pedido.produto.nome,
                        "Quantidade Pedido": pedido.quantidade,
                    }
                )

        return jsonify(dados)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@relatorio_route.route("/relatorio_pedidos_estoque_json", methods=["GET"])
def relatorio_pedidos_estoque_json():
    try:
        pedidos = PedidoEstoque.query.options(
            joinedload(PedidoEstoque.produto), joinedload(PedidoEstoque.fornecedor)
        ).all()

        if not pedidos:
            return jsonify([])

        dados = []
        for pedido in pedidos:
            dados.append(
                {
                    "ID Pedido": pedido.id,
                    "Produto": (
                        pedido.produto.nome if pedido.produto else "Não encontrado"
                    ),
                    "Quantidade": pedido.quantidade,
                    "Data do Pedido": (
                        pedido.data_pedido.strftime("%d/%m/%Y")
                        if pedido.data_pedido
                        else "Não registrado"
                    ),
                    "Fornecedor": (
                        pedido.fornecedor.nome
                        if pedido.fornecedor
                        else "Não encontrado"
                    ),
                }
            )

        return jsonify(dados)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
