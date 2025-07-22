
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard Lead Time", layout="wide")
st.title("📦 Dashboard de Seguimiento Lead Time")

archivo = st.file_uploader("📁 Sube el archivo Excel combinado", type=["xlsx"])

if archivo:
    df = pd.read_excel(archivo)

    if "ESTADO_LOGÍSTICO" not in df.columns:
        st.error("⚠️ La columna 'ESTADO_LOGÍSTICO' no existe. Asegúrate de subir el archivo correcto.")
    else:
        st.sidebar.header("🔍 Filtros")
        paises = df["PAIS"].dropna().unique()
        estados = df["ESTADO_LOGÍSTICO"].dropna().unique()
        proveedores = df["Proveedor"].dropna().unique()

        pais_filtro = st.sidebar.multiselect("Filtrar por país", paises, default=paises)
        estado_filtro = st.sidebar.multiselect("Filtrar por estado logístico", estados, default=estados)
        proveedor_filtro = st.sidebar.multiselect("Filtrar por proveedor", proveedores)

        df_filtrado = df[
            (df["PAIS"].isin(pais_filtro)) &
            (df["ESTADO_LOGÍSTICO"].isin(estado_filtro))
        ]
        if proveedor_filtro:
            df_filtrado = df_filtrado[df_filtrado["Proveedor"].isin(proveedor_filtro)]

        st.subheader("📊 Indicadores generales")
        total = df_filtrado.shape[0]
        a_tiempo = df_filtrado[df_filtrado["ESTADO_LOGÍSTICO"] == "A TIEMPO"].shape[0]
        alerta = df_filtrado[df_filtrado["ESTADO_LOGÍSTICO"] == "ALERTA"].shape[0]
        retrasado = df_filtrado[df_filtrado["ESTADO_LOGÍSTICO"] == "RETRASADO"].shape[0]

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total referencias", total)
        col2.metric("A tiempo", a_tiempo)
        col3.metric("Alerta", alerta)
        col4.metric("Retrasado", retrasado)

        st.subheader("📋 Tabla de resultados")
        st.dataframe(df_filtrado)

        st.subheader("⬇️ Descargar archivo filtrado")
        @st.cache_data
        def convertir_a_excel(df):
            from io import BytesIO
            output = BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="Filtrado")
            output.seek(0)
            return output

        excel_filtrado = convertir_a_excel(df_filtrado)
        st.download_button("📥 Descargar Excel", data=excel_filtrado, file_name="seguimiento_filtrado.xlsx")
