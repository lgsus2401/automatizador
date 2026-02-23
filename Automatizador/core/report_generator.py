import pandas as pd
from datetime import datetime
import os


def generate_report(df):

    if not os.path.exists("reports"):
        os.makedirs("reports")

    resumen = df.groupby("pais")["ingreso_total"].sum()

    html_content = f"""
    <h1>Reporte de Ventas</h1>
    <h3>Generado: {datetime.now()}</h3>
    {resumen.to_frame().to_html()}
    """

    file_path = "reports/reporte_ventas.html"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    return file_path
