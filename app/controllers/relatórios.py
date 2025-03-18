from datetime import date, datetime
from flask import Blueprint, request, jsonify
from app.modelo_db import Compra, Fornecedor, ItemCompra, PedidoEstoque, Produto, db

relatorio_route = Blueprint("relatorio", __name__)


# Relatório de vendas(total) de um período
@relatorio_route.route("/relatorio_vendas", methods=["GET"])
def relatorio_vendas():
    try:
        # Recebe as datas de filtro
        data_inicio = request.args.get("data_inicio")
        data_fim = request.args.get("data_fim")

        # Converte as datas para o formato datetime
        if data_inicio:
            data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d")
        if data_fim:
            data_fim = datetime.strptime(data_fim, "%Y-%m-%d")

        # Filtro de vendas com base nas datas, se fornecido
        query = Compra.query
        if data_inicio and data_fim:
            query = query.filter(Compra.data >= data_inicio, Compra.data <= data_fim)
        elif data_inicio:
            query = query.filter(Compra.data >= data_inicio)
        elif data_fim:
            query = query.filter(Compra.data <= data_fim)

        # Obtém todas as compras no intervalo de datas
        vendas = query.all()

        # Prepara os dados para exibição
        total_vendas = sum(compra.total for compra in vendas)
        resultados = [
            {"id": venda.id, "data": venda.data, "total": venda.total}
            for venda in vendas
        ]

        # Retorna o resultado com o total de vendas
        return jsonify({"vendas": resultados, "total_vendas": total_vendas}), 200

    except Exception as e:
        return jsonify({"error": f"Ocorreu um erro: {str(e)}"}), 500


# Relatório de pedidos de estoque -- JOIN para juntar produto e fornecedor a cada pedidoEstoque
@relatorio_route.route("/r_realizadoselatorio_pedidos_estoque", methods=["GET"])
def relatorio_pedidos_estoque():
    try:
        # Consultar todos os pedidos de estoque
        pedidos_estoque = PedidoEstoque.query.join(Produto).join(Fornecedor).all()

        if not pedidos_estoque:
            return jsonify({"message": "Nenhum pedido de estoque encontrado."}), 404

        resultado = [
            {
                "id_pedido": pedido.id,
                "produto": pedido.produto.nome,
                "fornecedor": pedido.fornecedor.nome,
                "quantidade": pedido.quantidade,
                "data_pedido": pedido.id,  # Aqui você pode adicionar o campo de data do pedido se tiver
            }
            for pedido in pedidos_estoque
        ]

        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Relatório de compras realizadas, com os produtos adquiridos, quantidade, preço unitário e subtotal.
@relatorio_route.route("/relatorio_compras", methods=["GET"])
def relatorio_compras():
    try:
        # Consultar todas as compras
        compras = Compra.query.join(ItemCompra).join(Produto).all()

        if not compras:
            return jsonify({"message": "Nenhuma compra encontrada."}), 404

        resultado = []
        for compra in compras:
            for item in compra.itens:
                resultado.append(
                    {
                        "id_compra": compra.id,
                        "produto": item.produto.nome,
                        "quantidade": item.quantidade,
                        "preco_unitario": item.preco_unitario,
                        "subtotal": item.subtotal,
                    }
                )

        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Relatórios de fornecedores, lista e todas informações associadas a ele.
@relatorio_route.route("/relatorio_fornecedores", methods=["GET"])
def relatorio_fornecedores():
    try:
        # Consultar todos os fornecedores com seus pedidos de estoque
        fornecedores = Fornecedor.query.join(PedidoEstoque).join(Produto).all()

        if not fornecedores:
            return jsonify({"message": "Nenhum fornecedor encontrado."}), 404

        resultado = []
        for fornecedor in fornecedores:
            for pedido in fornecedor.pedidos_estoque:
                resultado.append(
                    {
                        "id_fornecedor": fornecedor.id,
                        "nome_fornecedor": fornecedor.nome,
                        "cnpj": fornecedor.cnpj,
                        "contato": fornecedor.contato,
                        "produto": pedido.produto.nome,
                        "quantidade_pedido": pedido.quantidade,
                    }
                )

        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Relatório de compras
# @relatorio_route.route("/relatorio_compras", methods=["GET"])
# def relatorio_compras():
#     try:
#         # Consultar todas as compras com seus itens
#         compras = Compra.query.all()

#         if not compras:
#             return jsonify({"message": "Nenhuma compra encontrada."}), 404

#         resultado = []
#         for compra in compras:
#             itens = []
#             for item in compra.itens:
#                 itens.append(
#                     {
#                         "produto": item.produto.nome,
#                         "quantidade": item.quantidade,
#                         "preco_unitario": item.preco_unitario,
#                         "subtotal": item.subtotal,
#                     }
#                 )
#             resultado.append(
#                 {
#                     "id_compra": compra.id,
#                     "data_compra": compra.data,
#                     "total_compra": compra.total,
#                     "itens": itens,
#                 }
#             )

#         return jsonify(resultado), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# Relatório de estoque, com a quantidade disponivel e o valor total de cada produto
@relatorio_route.route("/relatorio_estoque", methods=["GET"])
def relatorio_estoque():
    try:
        # Consultar todos os produtos
        produtos = Produto.query.all()

        if not produtos:
            return jsonify({"message": "Nenhum produto encontrado no estoque."}), 404

        resultado = []
        for produto in produtos:
            valor_total = produto.preco * produto.quantidade_em_estoque
            resultado.append(
                {
                    "produto": produto.nome,
                    "quantidade_em_estoque": produto.quantidade_em_estoque,
                    "preco_unitario": produto.preco,
                    "valor_total_estoque": valor_total,
                }
            )

        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Relatório de vendas do dia: exibir todas as vendas do dia atual, com detalhes
@relatorio_route.route("/relatorios/vendas-dia", methods=["GET"])
def relatorio_vendas_dia():
    try:
        # Obtém a data informada na query string (ex: ?data=2025-03-18)
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
            data_filtro = date.today()

        # Filtra as vendas pela data
        vendas = Compra.query.filter(db.func.date(Compra.data) == data_filtro).all()

        resultado = []
        for venda in vendas:
            itens = ItemCompra.query.filter_by(compra_id=venda.id).all()
            detalhes_itens = []
            for item in itens:
                produto = Produto.query.get(item.produto_id)
                detalhes_itens.append(
                    {
                        "produto": produto.nome,
                        "quantidade": item.quantidade,
                        "preco_unitario": item.preco_unitario,
                        "subtotal": item.subtotal,
                    }
                )

            resultado.append(
                {
                    "id": venda.id,
                    "data": venda.data.strftime("%d/%m/%Y %H:%M"),
                    "total": venda.total,
                    "itens": detalhes_itens,
                }
            )

        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# relatório de produtos com estoque baixo (colocar límite definido!!!)
@relatorio_route.route("/relatorio/estoque-baixo", methods=["GET"])
def relatorio_estoque_baixo():
    try:
        produtos = Produto.query.filter(
            Produto.quantidade < Produto.estoque_minimo
        ).all()

        if not produtos:
            return (
                jsonify({"message": "Nenhum produto com estoque baixo encontrado."}),
                200,
            )

        resultado = [
            {
                "id": produto.id,
                "nome": produto.nome,
                "quantidade_estoque": produto.quantidade,
                "estoque_minimo": produto.estoque_minimo,
                "preco": f"R$ {produto.preco:.2f}",
                "fornecedor": (
                    produto.fornecedor.nome
                    if produto.fornecedor
                    else "Fornecedor não encontrado"
                ),
            }
            for produto in produtos
        ]

        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Relatório de pedidos de estoque realizados (produtos ja abastecidos)
@relatorio_route.route("/relatorio/pedidos-estoque", methods=["GET"])
def relatorio_pedidos_estoque_realizados():
    try:
        pedidos = PedidoEstoque.query.all()

        if not pedidos:
            return jsonify({"message": "Nenhum pedido de estoque encontrado."}), 200

        resultado = [
            {
                "id": pedido.id,
                "produto": (
                    pedido.produto.nome if pedido.produto else "Produto não encontrado"
                ),
                "quantidade": pedido.quantidade,
                "data_pedido": (
                    pedido.data_pedido.strftime("%d/%m/%Y")
                    if pedido.data_pedido
                    else "Data não registrada"
                ),
                "fornecedor": (
                    pedido.fornecedor.nome
                    if pedido.fornecedor
                    else "Fornecedor não encontrado"
                ),
            }
            for pedido in pedidos
        ]

        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
