import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards 

@st.cache_data
def carregar_dados():
    
    df = pd.read_parquet('funcionarios-ativos.parquet')
    df["DATA_INICIO_EXERC"] = pd.to_datetime(df["DATA_INICIO_EXERC"], format='%d/%m/%Y')
    df['TEMPO_DE_EXERCICIO'] = ((pd.to_datetime('today') - df['DATA_INICIO_EXERC']).dt.days / 365.25).astype(int)
    bins = [-np.inf, 1, 5, 10, 15, 21, np.inf]
    labels = ['menos de 1', '1 - 5 anos', '6 - 10 anos', '11 - 15 anos', '16 - 21 anos', '+ 21 anos']
    df['GRUPO_TEMPO_EXERCICIO'] = pd.cut(df['TEMPO_DE_EXERCICIO'], bins=bins, labels=labels)

    return df

def main():

    st.set_page_config(layout ="wide")
    st.sidebar.image("f3.png", width=150)
    st.title("Relação de Servidores Ativos da Prefeitura de São Paulo")



    df = carregar_dados()
    pd.set_option('display.max_columns', None)

    filtro_Relacao = st.sidebar.selectbox("Filtrar por Relação Jurídico Administrativa:", ["Todos", *df["REL_JUR_ADM"].unique()])

    filtro_tempo = st.sidebar.selectbox("Filtrar por Tempo Exercício:", ["Todos", *df["GRUPO_TEMPO_EXERCICIO"].unique()])

    # Aplicar filtro apenas se não for "Todos"
    if filtro_Relacao != "Todos" and filtro_tempo != "Todos":
        df_filtrado = df[(df['REL_JUR_ADM'] == filtro_Relacao) & (df['GRUPO_TEMPO_EXERCICIO'] == filtro_tempo)]
    elif filtro_Relacao != "Todos":
        df_filtrado = df[df['REL_JUR_ADM'] == filtro_Relacao]
    elif filtro_tempo != "Todos":
        df_filtrado = df[df['GRUPO_TEMPO_EXERCICIO'] == filtro_tempo]
    else:
        df_filtrado = df  # Sem filtro se "Todos" for selecionado

    st.dataframe(df_filtrado)

if __name__ == "__main__":
    main()