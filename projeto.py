# pip install streamlit
# pip install streamlit-option-menu

# python -m streamlit run projeto.py

import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

#Configurações iniciais
st.set_page_config(page_title="Dashboard de vendas", page_icon="🚀", layout="wide")

# Carregar os dados
df = pd.read_excel("Vendas.xlsx")

# FILTROS
# SideBar - Menu do lado
st.sidebar.header("Selecione os filtros")

# Filtro por loja 
lojas = st.sidebar.multiselect(
    "Lojas",
    # Opções do filtro
    options=df["ID Loja"].unique(),
    # Opção que vem por padrão no filtro
    default=df["ID Loja"].unique(),
    # Chave unica
    key="Loja" 
)

# Filtro de produto
produto = st.sidebar.multiselect(
    "Podutos",
    # Opções do filtro
    options=df["Produto"].unique(),
    # Opção que vem por padrão no filtro 
    default=df["Produto"].unique(),
    # Chave unica
    key="produto"
)

# Filtrar o dataframe de acordo com as opções selecionadas
df_selecao = df.query("`ID Loja` in @lojas and Produto in @produto") # Verifica os filtros que foram aplicados

# Grafico e na função da página
def Home(): # Tela principal - Primeira tela
    st.title("Faturamento das lojas")

    total_vendas = df["Quantidade"].sum()
    media = df["Quantidade"].mean()
    mediana = df["Quantidade"].median()

    total1, total2, total3 = st.columns(3)
    with total1:
        # Exibir indicadores rápidos
        st.metric("Total Vendido", value=int(total_vendas)) 
    
    with total2:
        st.metric("Média por produto", value=f"{media:.1f}")
                  
    with total3:
        st.metric("Mediana", value=int(mediana))

    st.markdown("---") # Passa um traçado em baixo dos valores para separação

def Graficos():
    # Gráfico de barras, mostrando a quantidade de produtos por loja
    fig_barras = px.bar(
        df_selecao, 
        x="Produto",
        y="Quantidade",
        color= "ID Loja", # Diferencia as lojas por cores
        barmode = "group",
        title= "Quantidade de Produtos Vendidos por Loja"
    )

    # Grafico de linha, com o total de vendas por loja 
    fig_linha = px.line(
        df.groupby(["ID Loja"]).sum(numeric_only= True).reset_index(),
        x = "ID Loja",
        y = "Quantidade",
        title= "Total de Vendas por Loja"
    )

    graf1, graf2 = st.columns(2)
    with graf1:
        st.plotly_chart(fig_barras, use_container_width=True)

    with graf2:
        st.plotly_chart(fig_linha, use_container_width=True)



def sidebar():
    with st.sidebar:
        selecionado = option_menu(
            menu_title= "Menu", 
            options=["Home", "Gráficos"],
            icons= ["house", "bar-chart"],
            default_index=0
        )

    if selecionado == "Home":
        Home()
        Graficos()
    elif selecionado == "Gráficos":
        Graficos()

sidebar()