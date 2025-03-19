import io
import pandas as pd
from flask import send_file


def gerar_excel(dataframe, nome_arquivo="relatorio.xlsx", nome_planilha="Relatório"):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        dataframe.to_excel(writer, index=False, sheet_name=nome_planilha)
    output.seek(0)
    return send_file(
        output,
        as_attachment=True,
        download_name=nome_arquivo,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
