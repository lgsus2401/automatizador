def generate_insights(df, kpis):

    insights = []

    margen = kpis["margen_global"]

    if margen < 0.15:
        insights.append("⚠ Margen bajo. Revisar estructura de costos.")
    elif margen < 0.30:
        insights.append("Margen saludable pero mejorable.")
    else:
        insights.append("Excelente rentabilidad global.")

    # Concentración de producto

    top_producto = (
        df.groupby("producto")["ingreso_total"]
        .sum()
        .sort_values(ascending=False)
    )

    porcentaje_top = top_producto.iloc[0] / kpis["total_ingresos"]

    if porcentaje_top > 0.40:
        insights.append("⚠ Alta dependencia de un solo producto.")
    else:
        insights.append("Portafolio diversificado correctamente.")

    # Margen negativo

    productos_margen_negativo = df.groupby("producto")["utilidad_bruta"].sum()
    productos_margen_negativo = productos_margen_negativo[productos_margen_negativo < 0]

    if len(productos_margen_negativo) > 0:
        insights.append("⚠ Existen productos con pérdida acumulada.")
    else:
        insights.append("No hay productos con pérdidas acumuladas.")

    ventas_mensuales = (
        df.groupby(df["fecha"].dt.to_period("M"))["ingreso_total"]
        .sum()
    )

    if ventas_mensuales.pct_change().mean() < 0:
        insights.append("⚠ Tendencia de ventas decreciente.")
    else:
        insights.append("Tendencia de ventas estable o creciente.")
    return insights
