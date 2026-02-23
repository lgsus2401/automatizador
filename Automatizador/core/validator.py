import pandas as pd

REQUIRED_COLUMNS = ["id_transaccion",
                    "fecha",
                    "cliente",
                    "pais",
                    "producto",
                    "cantidad",
                    "precio_unitario",
                    "costo_unitario",
                    "canal_venta"]

OPTIONAL_COLUMNS = ["ingreso_total", "costo_total", "utilidad_bruta"]


def normalize_columns(df):
    df.columns = [
        col.strip().lower().replace(" ", "_")
        for col in df.columns
    ]
    return df


def validate_required_columns(df):
    faltantes = [col for col in REQUIRED_COLUMNS if col not in df.columns]

    if faltantes:
        raise ValueError(f"Faltan columnas obligatorias: {faltantes}")
    return True


def validate_file_not_empty(df):
    if df.shape[0] == 0:
        raise ValueError("El archivo está vacío o no contiene registros.")
    return True


def run_validation(df):
    df = normalize_columns(df)
    validate_file_not_empty(df)
    validate_required_columns(df)
    validate_and_convert_types(df)
    return df


def validate_and_convert_types(df):
    df["cantidad"] = pd.to_numeric(df["cantidad"], errors="coerce")
    df["precio_unitario"] = pd.to_numeric(
        df["precio_unitario"], errors="coerce")
    df["costo_unitario"] = pd.to_numeric(df["costo_unitario"], errors="coerce")
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")

    rows_before = len(df)
    df = df.dropna(
        subset=["cantidad", "precio_unitario", "costo_unitario", "fecha"])
    rows_after = len(df)

    registros_eliminados = rows_before - rows_after

    print(f"Registros eliminados por datos inválidos: {registros_eliminados}")

    return df
