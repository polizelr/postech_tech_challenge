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

tab0, tab1, tab2, tab3, tab4 = st.tabs(["Dados de Exportação", "Dados Demográficos", "Dados Econômicos", "Dados Climáticos", "Análise Exploratória"])

with tab0:
    '''
    ## Dados de Exportação
    '''
    df_dados_exportacao = pd.read_csv('./dados/tabela_final.csv')
    df = pd.DataFrame(df_dados_exportacao)
    st.dataframe(df, use_container_width=True)
    
    
with tab1:
    #Dados
    
    #Base
    df_exportacao_pais_top_x_pib_demographic = pd.read_csv('./dados/df_exportacao_pais_top_x_pib_demographic.csv')
    
    #População Total
    df_exportacao_pais_pib_demograficos_pop = df_exportacao_pais_top_x_pib_demographic.groupby('Country Name').agg({'Total Population Millions': 'mean'}).reset_index()
    df_exportacao_pais_pib_demograficos_pop_sorted = df_exportacao_pais_pib_demograficos_pop.sort_values(by='Total Population Millions', ascending=False)
    
    #Média Idade
    df_exportacao_pais_pib_demograficos_med_age = df_exportacao_pais_top_x_pib_demographic.groupby('Country Name').agg({'Median Age': 'mean'}).reset_index()
    df_exportacao_pais_pib_demograficos_med_age_sorted = df_exportacao_pais_pib_demograficos_med_age.sort_values(by='Median Age', ascending=False)
    
    #Expectativa de Vida
    df_exportacao_pais_pib_demograficos_exp_vida = df_exportacao_pais_top_x_pib_demographic.groupby('Country Name').agg({'Life Expectation': 'mean'}).reset_index()
    df_exportacao_pais_pib_demograficos_sorted = df_exportacao_pais_pib_demograficos_exp_vida.sort_values(by='Life Expectation', ascending=False)
    
    '''
    ## Dados Demográficos
    
    https://population.un.org/wpp/

    A Revisão de 2022 das Perspectivas da População Mundial é a vigésima sétima edição das estimativas e projeções populacionais oficiais das Nações Unidas que foram preparadas pela Divisão de População do Departamento de Assuntos Econômicos e Sociais do Secretariado das Nações Unidas.
    
    Apresenta estimativas populacionais de 1950 até o presente para 237 países ou áreas, sustentadas por análises de tendências demográficas históricas. Esta última avaliação considera os resultados de 1.758 censos populacionais nacionais realizados entre 1950 e 2022, bem como informações de sistemas de registro vital e de 2.890 pesquisas de amostra nacionalmente representativas. nos níveis global, regional e nacional.
    
    ### População
    Ao tentar analisar a população dos Top importadores podemos ver que não há um padrão definido:
    '''
    
    ####### Gráfico de barras #####
    # Criando a figura
    fig, ax = plt.subplots(figsize=(15, 10))

    # Criando uma paleta categórica com inversão de tons
    custom_palette = sns.color_palette("Blues", n_colors=len(df_exportacao_pais_pib_demograficos_pop_sorted))

    sns.barplot(data=df_exportacao_pais_pib_demograficos_pop_sorted, x='Total Population Millions', y='Country Name', hue='Total Population Millions', palette=custom_palette, dodge=False, ax=ax)
    ax.legend_.remove()  # Remover a legenda do hue
    ax.set_xlabel('População média (em milhões)')
    ax.set_ylabel('País')
    ax.set_title('Top Países Importadores - População')

    # Remover a notação científica dos valores nos eixos
    ax.get_xaxis().set_major_formatter(ticker.FuncFormatter(lambda x, _: '{:,.0f}'.format(x)))
    
    st.pyplot(fig)
    #############################
    is_exibir_exp_pop = st.checkbox('Tabela População Top Importadores')
    if is_exibir_exp_pop:
        st.dataframe(df_exportacao_pais_pib_demograficos_pop_sorted, use_container_width=True, hide_index=True)
        csv = df_exportacao_pais_pib_demograficos_pop_sorted.to_csv(index=False)
        st.download_button(label='Download Top População (CSV)', data=csv, file_name='exp_top_populacao.csv', mime='text/csv')    
    
    
    '''
    - A China possui uma população muito maior do que os outros países, o que poderia gerar pensamentos como a buscar por outros mercados que possuem a mesma característica, como a Índia, por exemplo 
    - Contudo, os demais países possuem uma população muito abaixo, indicando que este não deve ser um fator com grande peso na tomada de decisão
    '''
    
    
    
    '''
    ### Idade Média
    Ao analisar a Idade Média, porém, temos alguns destaques:
    '''
    ####### Gráfico de barras #####
    # Criando a figura
    fig, ax = plt.subplots(figsize=(15, 10))

    # Criando uma paleta categórica com inversão de tons
    custom_palette = sns.color_palette("Blues", n_colors=len(df_exportacao_pais_pib_demograficos_med_age_sorted))

    sns.barplot(data=df_exportacao_pais_pib_demograficos_med_age_sorted, x='Median Age', y='Country Name', hue='Median Age', palette=custom_palette, dodge=False, ax=ax)
    ax.legend_.remove()  # Remover a legenda do hue
    ax.set_xlabel('Idade média da população')
    ax.set_ylabel('País')
    ax.set_title('Top Países Importadores - Idade média da população')

    # Remover a notação científica dos valores nos eixos
    ax.get_xaxis().set_major_formatter(ticker.FuncFormatter(lambda x, _: '{:,.0f}'.format(x)))
    
    st.pyplot(fig)
    #############################
    is_exibir_exp_med_age = st.checkbox('Tabela Média Idade Top Importadores')
    if is_exibir_exp_med_age:
        st.dataframe(df_exportacao_pais_pib_demograficos_med_age_sorted, use_container_width=True, hide_index=True)
        csv = df_exportacao_pais_pib_demograficos_med_age_sorted.to_csv(index=False)
        st.download_button(label='Download Média Idade (CSV)', data=csv, file_name='exp_ med_idade.csv', mime='text/csv') 
    
    '''
    Uma parte considerável dos top países importadores do Brasil tem uma idade média na casa dos 38 anos - com destaque para o Japão e Alemanha.
    '''
    
    ####### Gráfico de barras #####
    ax.axvline(x=38, color='red', linestyle='--')
    st.pyplot(fig)
    #############################
    
    '''
    Mostrando um possível forte mercado, traçando um filtro e buscando os países com idade média próxima dessa faixa
    
    ### ADICIONAR GRÁFICO
    '''
    
    #TODO: @RODRIGO adicionar csv e gráfico com os países de maior média de idade que não estão nos top importadores
    
    '''
    ### Expectativa de Vida
    Ao analisar a expectativa de vida, vemos que os principais compradores do Brasil possuem uma expectativa de vida consideravelmente, reforçando a relação com a análise anterior
    '''
    
    ####### Gráfico de barras #####
    # Criando a figura
    fig, ax = plt.subplots(figsize=(15, 10))

    # Criando uma paleta categórica com inversão de tons
    custom_palette = sns.color_palette("Blues", n_colors=len(df_exportacao_pais_pib_demograficos_sorted))

    sns.barplot(data=df_exportacao_pais_pib_demograficos_sorted, x='Life Expectation', y='Country Name', hue='Life Expectation', palette=custom_palette, dodge=False, ax=ax)
    ax.legend_.remove()  # Remover a legenda do hue
    ax.set_xlabel('Expectativa de vida média da população')
    ax.set_ylabel('País')
    ax.set_title('Top Países Importadores - Expectativa de vida média da população')

    # Remover a notação científica dos valores nos eixos
    ax.get_xaxis().set_major_formatter(ticker.FuncFormatter(lambda x, _: '{:,.0f}'.format(x)))
    
    st.pyplot(fig)
    #############################
    
    '''
    Podemos então destacar outros mercados com expectativa de vida elevada como fortes candidatos
    ### ADICIONAR GRÁFICO
    '''
    
    #TODO: @RODRIGO adicionar csv e gráfico com os países de maior expectativa de vida que não estão nos top importadores
    
    
    
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
    is_exibir_exp_pib = st.checkbox('Tabela PIB Top Importadores')
    if is_exibir_exp_pib:
        st.dataframe(df_exportacao_pais_top_x_pib_sorted, use_container_width=True, hide_index=True)
        csv = df_exportacao_pais_top_x_pib_sorted.to_csv(index=False)
        st.download_button(label='Download PIB Top Importadores (CSV)', data=csv, file_name='exp_top_pib.csv', mime='text/csv')
        
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

    is_exibir_ins_pib = st.checkbox('Tabela Insights PIB')
    if is_exibir_ins_pib:
        st.dataframe(df_pib_paises_avg_30k_not_exp, use_container_width=True)
        csv = df_pib_paises_avg_30k_not_exp.to_csv(index=False)
        st.download_button(label='Download Insights PIB (CSV)', data=csv, file_name='insights_pib.csv', mime='text/csv')

    
with tab3:
    '''
    ## Dados Climáticos
    '''
    
with tab4:
    '''
    ## Análise Exploratória
    _Esta análise tem um viés técnico e é indicada para quem buscar entender melhor o workflow de trabalho seguido para encontrar os insights já apresentados_
    
    Com o objetivo de realizar prospecções interessantes para a empresa e entender os mercados mais fortes para se posicionar, o primeiro passo realizado pela equipe foi o aprofundamento nas bases de dados brasileiras relativas a vinho.
    
    Foi definido como base principal a Embrapa e analisados os dados de viticultura disponíveis em:
    
    http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_01
    
    
    '''