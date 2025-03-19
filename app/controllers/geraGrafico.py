from flask import Blueprint, request, send_file
from graph.grafico_pizza import gerar_grafico_pizza
from graph.grafico_barra import gerar_grafico_barra
from graph.grafico_linha import gerar_grafico_linha

grafico_controller = Blueprint("grafico_controller", __name__)


# Função de exemplo para pegar dados de relatório
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


@grafico_controller.route("/gerar_grafico", methods=["POST"])
def gerar_grafico():
    tipo_grafico = request.json.get("tipo_grafico")
    tipo_relatorio = request.json.get("tipo_relatorio")

    # Pega os dados do relatório conforme o tipo de relatório
    dados_relatorio = get_dados_relatorio(tipo_relatorio)

    if tipo_grafico == "pizza":
        img_io = gerar_grafico_pizza(dados_relatorio)
    elif tipo_grafico == "barra":
        img_io = gerar_grafico_barra(dados_relatorio)
    elif tipo_grafico == "linha":
        img_io = gerar_grafico_linha(dados_relatorio)
    else:
        return {"error": "Tipo de gráfico inválido"}, 400

    return send_file(img_io, mimetype="image/png")
