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

    filtro_Relacao = st.sidebar.selectbox("Filtrar por Relação Jurídico Administrativa:", ["Todos", *df["REL_JUR_ADM"].unique()])

    # Aplicar filtro apenas se não for "Todos"
    if filtro_Relacao  != "Todos":
        df_filtrado = df[df['REL_JUR_ADM'] == filtro_Relacao]
    else:
        df_filtrado = df  # Sem filtro se "Todos" for selecionado

    total_funcionarios = df_filtrado["REGISTRO"].nunique()
    total_mulheres = df_filtrado.drop_duplicates(subset=['REGISTRO']).loc[df['SEXO'] == 'F', 'SEXO'].value_counts()
    total_homens = df_filtrado.drop_duplicates(subset=['REGISTRO']).loc[df['SEXO'] == 'M', 'SEXO'].value_counts()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Funcionários", total_funcionarios)
        style_metric_cards(border_left_color="#FF4500")

    with col2:
        st.metric("Total Mulheres", total_mulheres)

    with col3:
        st.metric("Total Homens", total_homens)


    
    total_sexo = df_filtrado.drop_duplicates(subset=['REGISTRO'])['SEXO'].value_counts().reset_index().rename(columns={"index":"SEXO", "SEXO":"Total"})


    total_raca = df_filtrado.drop_duplicates(subset=['REGISTRO'])['RACA'].value_counts().reset_index().rename(columns={"index":"Raça", "RACA":"Total"})

    total_tempo = df_filtrado["GRUPO_TEMPO_EXERCICIO"].value_counts().reset_index().\
                    rename(columns={"index":"Grupo", "GRUPO_TEMPO_EXERCICIO":"Total"})

    
    fig = px.pie(total_sexo, values='count', names='Total', title='Proporção de funcionários por Sexo', color_discrete_sequence=["#FF4500"])
    st.plotly_chart(fig)

    
    fig1= px.bar(total_raca, x='Total', y='count', title="Total de Funcionários por Raça",
             text="count", color_discrete_sequence=["#FF4500"])
    st.plotly_chart(fig1)

    
    fig2 = px.bar(total_tempo, x='Total', y='count', title="Total de Funcionários por Tempo de casa",text="count", color_discrete_sequence=["#FF4500"])
    st.plotly_chart(fig2)


if __name__ == "__main__":
    main()