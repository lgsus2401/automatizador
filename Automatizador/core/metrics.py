import pandas as pd


def add_financial_columns(df):
    df["ingreso_total"] = df["cantidad"] * df["precio_unitario"]
    df["costo_total"] = df["cantidad"] * df["costo_unitario"]
    df["utilidad_bruta"] = df["ingreso_total"] - df["costo_total"]
    df["margen_bruto_pct"] = df["utilidad_bruta"] / df["ingreso_total"]
    df["margen_bruto_pct"] = df["margen_bruto_pct"].fillna(0)
    return df


def calculate_global_metrics(df):
    metrics = {
        "total_ingresos": df["ingreso_total"].sum(),
        "total_utilidad": df["utilidad_bruta"].sum(),
        "total_costo": df["costo_total"].sum(),
        "margen_global": df["utilidad_bruta"].sum() / df["ingreso_total"].sum(),
        "ticket_promedio": df["ingreso_total"].mean(),
        "total_transacciones": len(df)
    }

    return metrics


def top_5_products(df):
    return (
        df.groupby("producto")["ingreso_total"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )
