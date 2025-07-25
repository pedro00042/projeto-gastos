import streamlit as st
import pandas as pd

st.set_page_config(page_title="Análise de Gastos", layout="wide")

st.title("📊 Análise de Gastos - ContaAzul")

# Upload da planilha
arquivo = st.file_uploader("Envie a planilha do ContaAzul (.xlsx)", type="xlsx")

if arquivo:
    try:
        df = pd.read_excel(arquivo)

        # Exibe os dados da planilha
        st.subheader("🔍 Visualização dos dados")
        st.dataframe(df)

        # Ajuste conforme as colunas da sua planilha:
        df["Data"] = pd.to_datetime(df["Data"])
        df["Mês"] = df["Data"].dt.strftime("%B/%Y")

        # Gastos por mês
        gastos_mes = df.groupby("Mês")["Valor"].sum().sort_index()
        st.subheader("📅 Gastos por Mês")
        st.bar_chart(gastos_mes)

        # Gastos por categoria
        gastos_categoria = df.groupby("Categoria")["Valor"].sum().sort_values(ascending=False)
        st.subheader("📦 Gastos por Categoria")
        st.bar_chart(gastos_categoria)

    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
