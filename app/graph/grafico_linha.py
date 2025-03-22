import matplotlib.pyplot as plt
import io


def gerar_grafico_linha(dados):
    # Lógica para gerar o gráfico de linha
    labels = dados.keys()
    values = dados.values()
    fig, ax = plt.subplots()
    ax.plot(labels, values, marker="o")

    img_io = io.BytesIO()
    fig.savefig(img_io, format="png")
    img_io.seek(0)
    return img_io
