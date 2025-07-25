import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Análise de Gastos")

arquivo = st.file_uploader("Envie a planilha (.xlsx)", type="xlsx")

if arquivo:
    try:
        df = pd.read_excel(arquivo)
        st.subheader("Tabela completa")
        st.dataframe(df)

        if "Data" in df.columns and "Valor" in df.columns:
            df["Data"] = pd.to_datetime(df["Data"], errors="coerce")
            df = df.dropna(subset=["Data"])
            df["Mês"] = df["Data"].dt.strftime("%B/%Y")

            gastos_mes = df.groupby("Mês")["Valor"].sum().sort_index()

            # Escolha do gráfico para gastos por mês
            tipo_graf_mes = st.selectbox("Escolha o tipo de gráfico para Gastos por Mês",
                                        ["Barra", "Linha", "Pizza"])

            st.subheader("Gastos por Mês")

            if tipo_graf_mes == "Barra":
                st.bar_chart(gastos_mes)
            elif tipo_graf_mes == "Linha":
                st.line_chart(gastos_mes)
            else:  # Pizza
                fig, ax = plt.subplots()
                ax.pie(gastos_mes, labels=gastos_mes.index, autopct="%1.1f%%", startangle=90)
                ax.axis("equal")
                st.pyplot(fig)

            # Gastos por categoria
            if "Categoria" in df.columns:
                gastos_cat = df.groupby("Categoria")["Valor"].sum()

                tipo_graf_cat = st.selectbox("Escolha o tipo de gráfico para Gastos por Categoria",
                                            ["Barra", "Pizza", "Linha"])

                st.subheader("Gastos por Categoria")

                if tipo_graf_cat == "Barra":
                    st.bar_chart(gastos_cat)
                elif tipo_graf_cat == "Linha":
                    st.line_chart(gastos_cat)
                else:
                    fig, ax = plt.subplots()
                    ax.pie(gastos_cat, labels=gastos_cat.index, autopct="%1.1f%%", startangle=90)
                    ax.axis("equal")
                    st.pyplot(fig)

            else:
                st.info("Coluna 'Categoria' não encontrada para gráfico por categoria.")

        else:
            st.info("A planilha precisa das colunas 'Data' e 'Valor' para gerar gráficos.")

    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
