from core.insights import generate_insights
from core.metrics import add_financial_columns, calculate_global_metrics
from core.validator import run_validation
from core.email_service import send_email
from core.report_generator import generate_report

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

@st.cache_data
def load_data():
    return pd.read_csv("Automatizador/base_financiera.csv")

df = load_data()

st.set_page_config(
    page_title="Dashboard Financiero Internacional", layout="wide")

st.markdown("""
<style>
body {
    background-color: #0E1117;
    color: white;
}
[data-testid="stMetricValue"] {
    font-size: 28px;
}
</style>
""", unsafe_allow_html=True)


st.title("🌍 Dashboard Financiero Internacional")

# Cargar datos

df = pd.read_csv("Automatizador/base_financiera.csv", encoding="utf-8")

df = run_validation(df)
df = add_financial_columns(df)

mapa_paises = {
    "España": "Spain",
    "México": "Mexico",
    "Perú": "Peru",
    "Colombia": "Colombia",
    "Estados Unidos": "United States"
}

df["pais"] = df["pais"].replace(mapa_paises)

# Normalizar nombres de columnas
df.columns = (
    df.columns
    .str.strip()        # elimina espacios
    .str.lower()        # todo en minúscula
    .str.replace(" ", "_")  # espacios a _
)

# SIDEBAR - FILTROS
# =========================

st.sidebar.header("🎛 Filtros Dinámicos")

# Filtro país
paises = st.sidebar.multiselect(
    "Seleccionar País",
    options=df["pais"].unique(),
    default=df["pais"].unique()
)

# Filtro producto
productos = st.sidebar.multiselect(
    "Seleccionar Producto",
    options=df["producto"].unique(),
    default=df["producto"].unique()
)

# Filtro canal
canales = st.sidebar.multiselect(
    "Seleccionar Canal de Venta",
    options=df["canal_venta"].unique(),
    default=df["canal_venta"].unique()
)

# Filtro fechas
fecha_min = df["fecha"].min()
fecha_max = df["fecha"].max()

rango_fechas = st.sidebar.date_input(
    "Seleccionar Rango de Fechas",
    [fecha_min, fecha_max]
)

# =========================
# APLICAR FILTROS
# =========================


df_filtrado = df[
    (df["pais"].isin(paises)) &
    (df["producto"].isin(productos)) &
    (df["canal_venta"].isin(canales)) &
    (df["fecha"] >= pd.to_datetime(rango_fechas[0])) &
    (df["fecha"] <= pd.to_datetime(rango_fechas[1]))
]


# KPIS

kpis = calculate_global_metrics(df_filtrado)
insights = generate_insights(df_filtrado, kpis)

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Ingresos Totales", f"${kpis['total_ingresos']:,.0f}")
col2.metric("📈 Margen Global", f"{kpis['margen_global']*100:.2f}%")
col3.metric("🛒 Ticket Promedio", f"${kpis['ticket_promedio']:,.0f}")
col4.metric("🔄 Transacciones", kpis["total_transacciones"])

st.divider()

# Ventas por país (Mapa)


df["pais"] = df["pais"].replace(mapa_paises)


ventas_por_pais = (
    df_filtrado.groupby("pais")["ingreso_total"]
    .sum()
    .reset_index()
)

fig_map = px.choropleth(
    ventas_por_pais,
    locations="pais",
    locationmode="country names",
    color="ingreso_total",
    color_continuous_scale="RdYlGn",
    template="plotly_dark",
    title="Ventas por País"
)

fig_map.update_geos(showcoastlines=True, projection_type="natural earth")


st.plotly_chart(fig_map, use_container_width=True)

# Top productos

top_productos = (
    df_filtrado.groupby("producto")["ingreso_total"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_bar = px.bar(
    top_productos,
    x="producto",
    y="ingreso_total",
    title="Top 10 productos por Ingresos"
)

st.plotly_chart(fig_bar, use_container_width=True)

# Tendencia mensual

df_filtrado = df_filtrado.copy()
df_filtrado["mes"] = df["fecha"].dt.to_period("M").astype(str)

ventas_mensuales = (
    df_filtrado.groupby("mes")["ingreso_total"]
    .sum()
    .reset_index()
)

fig_line = px.line(
    ventas_mensuales,
    x="mes",
    y="ingreso_total",
    title="Tendencia Mensual de Ventas"
)

st.plotly_chart(fig_line, use_container_width=True)

# insights

st.subheader("🧠 Insights Estratégicos")

for i in insights:
    st.write("•", i)

st.divider()
st.subheader("📩 Enviar reporte por correo")

email_destino = st.text_input("Correo destinatario")

if st.button("Generar y Enviar Reporte"):

    if email_destino:

        with st.spinner("Generando reporte..."):
            file_path = generate_report(df_filtrado)

        with st.spinner("Enviando correo..."):
            send_email(email_destino, file_path, insights)

        st.success("Reporte enviado correctamente 🚀")

    else:
        st.warning("Ingresa un correo válido.")


