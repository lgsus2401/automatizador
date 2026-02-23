import pandas as pd
from core.validator import normalize_columns
from core.validator import run_validation
from core.metrics import add_financial_columns, calculate_global_metrics, top_5_products
from core.insights import generate_insights
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


try:
    df = pd.read_csv("base_financiera.csv")

    df = run_validation(df)
    print("Validación exitosa")

    df = add_financial_columns(df)

    kpis = calculate_global_metrics(df)

    insights = generate_insights(df, kpis)

    print("\nInsights Estratégicos:")
    for i in insights:
        print("-", i)

    print("\nKPIs Generales:")
    print(kpis)

    print("\nTop 5 Productos:")
    print(top_5_products(df))

except Exception as e:
    print(f"Error en validación: {e}")
