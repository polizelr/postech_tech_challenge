import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go 
from plotly.subplots import make_subplots

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.2f' % x)




st.title('FIAPWine')

tab0, tab1, tab2, tab3, tab4 = st.tabs(["Dados de Exportação", "Dados Demográficos", "Dados Econômicos", "Dados Climáticos", "Dados de Avaliações de Vinhos"])

with tab0:
    '''
    ## Dados de Exportação
    '''
    df_dados_exportacao = pd.read_csv('./dados/tabela_final.csv')
    df = pd.DataFrame(df_dados_exportacao)
    st.dataframe(df, use_container_width=True)
    
    
with tab1:
    '''
    ## Dados Demográficos
    '''

    
with tab2:
    #Dados
    df_exportacao_pais_pib = pd.read_csv('./dados/df_exportacao_pais_pib.csv')    
    df_exportacao_pais_top_x_pib_sorted = df_exportacao_pais_pib.sort_values(by='GDP', ascending=False)    
    df_pib_paises_avg_30k_not_exp = pd.read_csv('./dados/df_pib_paises_avg_30k_not_exp.csv')    
    
    '''
    ## Dados Econômicos
    
    https://data.worldbank.org/indicator/NY.GDP.MKTP.CD
    
    O PIB (GDP) per capita é o produto interno bruto dividido pela população no meio do ano.
    
    Ele é calculado através da soma do valor bruto adicionado por todos os produtores residentes na economia mais quaisquer impostos sobre produtos e menos quaisquer subsídios não incluídos no valor dos produtos. É calculado sem fazer deduções para depreciação de ativos fabricados ou para esgotamento e degradação de recursos naturais.
    
    _Os dados estão em dólares americanos_.

    ### Top Importadores do Brasil - PIB
    Ao analisar o PIB dos Top importadores alguns pontos podem ser destacados
    '''
    
    ####### Gráfico de barras #####
    # Criando a figura
    fig, ax = plt.subplots(figsize=(15, 10))

    # Criando uma paleta categórica com inversão de tons
    custom_palette = sns.color_palette("Blues", n_colors=len(df_exportacao_pais_top_x_pib_sorted))

    sns.barplot(data=df_exportacao_pais_top_x_pib_sorted, x='GDP', y='Country Name', hue='GDP', palette=custom_palette, dodge=False, ax=ax)
    ax.legend_.remove()  # Remover a legenda do hue
    ax.set_xlabel('PIB per Capita Médio')
    ax.set_ylabel('País')
    ax.set_title('Top Países Importadores - PIB')

    # Remover a notação científica dos valores nos eixos
    ax.get_xaxis().set_major_formatter(ticker.FuncFormatter(lambda x, _: '{:,.0f}'.format(x)))

    st.pyplot(fig)
    #############################
    
    #Tabela
    
    #Opcao com checkbox
    is_exibir = st.checkbox('Tabela PIB Top Importadores')
    if is_exibir:
        st.dataframe(df_exportacao_pais_top_x_pib_sorted, use_container_width=True, hide_index=True)
        csv = df_exportacao_pais_top_x_pib_sorted.to_csv(index=False)
        st.download_button(label='Download Top Importadores (CSV)', data=csv, file_name='data.csv', mime='text/csv')
        
    #Opcao com botao - Tem que ajustar para ter mais de um botão
    #if 'button' not in st.session_state:
    #    st.session_state.button = False

    #def click_button():
    #    st.session_state.button = not st.session_state.button

    #st.button('Dados Detalhados - Top Países', on_click=click_button)
    
    #if st.session_state.button:
    #    st.dataframe(df_exportacao_pais_top_x_pib_sorted, use_container_width=True, hide_index=True)
    #    csv = df_exportacao_pais_top_x_pib_sorted.to_csv(index=False)
    #    st.download_button(label='Download CSV', data=csv, file_name='data.csv', mime='text/csv')

    '''
    
    '''
    
    '''    
    - Não há uma relação direta do PIB per Capita médio dos últimos anos com as exportações para todos os países. Rússia e Paraguai que se destacam tanto em quantidade e valor possuem um PIB per capita médio bem abaixo da maioria dos demais top importadores do Brasil.
    - Contudo, é visto que dentro os atuais Top 10 países, 6 possuem um PIB per Capita médio em torno de 30k.
    '''
    
    ####### Gráfico de barras #####
    ax.axvline(x=30_000, color='red', linestyle='--')
    st.pyplot(fig)
    #############################
    
    '''
    Gerando um insight de possíveis mercados para entrar ou aumentar a oferta baseado nessa linha de corte (PIB médio >= 30k)
    '''    
    
    ####### Gráfico de barras #####
    # Criando a figura
    fig, ax = plt.subplots(figsize=(15, 10))

    # Criando uma paleta categórica com inversão de tons
    custom_palette = sns.color_palette("Blues", n_colors=len(df_pib_paises_avg_30k_not_exp))

    sns.barplot(data=df_pib_paises_avg_30k_not_exp, x='GDP', y='Country Name', hue='GDP', palette=custom_palette, dodge=False, ax=ax)
    ax.legend_.remove()  # Remover a legenda do hue
    ax.set_xlabel('PIB per Capita Médio')
    ax.set_ylabel('País')
    ax.set_title('Países com PIB per Capita Médio > 30 mil')
    ax.axvline(x=30_000, color='red', linestyle='--')

    # Remover a notação científica dos valores nos eixos
    ax.get_xaxis().set_major_formatter(ticker.FuncFormatter(lambda x, _: '{:,.0f}'.format(x)))
    st.pyplot(fig)
    #############################

    #Tabela
    #st.dataframe(df_pib_paises_avg_30k_not_exp, use_container_width=True)

    is_exibir = st.checkbox('Tabela Insights PIB')
    if is_exibir:
        st.dataframe(df_pib_paises_avg_30k_not_exp, use_container_width=True)
        csv = df_pib_paises_avg_30k_not_exp.to_csv(index=False)
        st.download_button(label='Download Insights PIB (CSV)', data=csv, file_name='data.csv', mime='text/csv')

    
with tab3:
    '''
    ## Dados Climáticos
    '''
    
with tab4:
    '''
    ## Dados de Avaliações de Vinhos
    '''