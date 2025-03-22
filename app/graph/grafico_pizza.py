import matplotlib.pyplot as plt
import io


def gerar_grafico_pizza(dados):
    # Lógica para gerar o gráfico de pizza
    labels = dados.keys()
    sizes = dados.values()

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")

    img_io = io.BytesIO()
    fig.savefig(img_io, format="png")
    img_io.seek(0)
    return img_io
