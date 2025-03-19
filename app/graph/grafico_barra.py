import matplotlib.pyplot as plt
import io


def gerar_grafico_barra(dados):
    # Lógica para gerar o gráfico de barra
    labels = dados.keys()
    values = dados.values()
    fig, ax = plt.subplots()
    ax.bar(labels, values)

    img_io = io.BytesIO()
    fig.savefig(img_io, format="png")
    img_io.seek(0)
    return img_io
