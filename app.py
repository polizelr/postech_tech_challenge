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




st.title('Exportação de Vinhos - Análise e Insights')

tab0, tab1, tab2, tab3, tab4 = st.tabs(["Home", "Dados Demográficos", "Dados Econômicos", "Dados Climáticos", "Análise Exploratória"])

with tab0:
    '''
    ## Dados de Exportação
    '''
    df_dados_exportacao = pd.read_csv('./dados/tabela_final.csv')
    df = pd.DataFrame(df_dados_exportacao)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    
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
    #Dados
    
    #Base
    df_exportacao = pd.read_csv('./dados/df_exportacao.csv')
    
    #Group ano
    df_group_exportacao_ano = df_exportacao.groupby('Year')[['Quantity (KG)', 'Value (US)']]
    desc_stats_ano = df_group_exportacao_ano.describe()
    
    #Group país
    df_group_exportacao_pais = df_exportacao.groupby('Country Name')[['Quantity (KG)', 'Value (US)']]
    desc_stats_pais = df_group_exportacao_pais.describe()
    
    #Ano
    df_exportacao_ano = pd.read_csv('./dados/df_exportacao_ano.csv')
    
    #País
    df_exportacao_pais = pd.read_csv('./dados/df_exportacao_pais.csv')
    df_exportacao_pais_top_10_qtd_sorted = df_exportacao_pais.sort_values(by='Quantity (KG)', ascending=False)
    df_exportacao_pais_top_10_valor_sorted = df_exportacao_pais.sort_values(by='Value (US)', ascending=False)
    df_exportacao_pais_top_x = pd.read_csv('./dados/df_exportacao_pais_top_x.csv')
    
    '''
    ## Análise Exploratória
    _Esta análise possui um viés técnico e é indicada para quem busca entender o workflow de trabalho seguido para encontrar os insights apresentados nas seções anteriores_
    
    Com o objetivo de realizar prospecções interessantes para a empresa e entender os mercados mais fortes para se posicionar, o primeiro passo realizado pela equipe foi o aprofundamento nas bases de dados brasileiras relativas a vinho.
    
    Foi definido como base principal a Embrapa e analisados os dados de viticultura disponíveis em:
    
    http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_01
    
    O foco é o mercado externo, então as análises foram feitas em cimas do dataset de exportação. Foram filtrados os dados entre 2007 e 2021. Além disso, devido a grande variedade de países disponíveis, a análise concentrou-se nos Top X País Importadores, isto é, o Top 10 países por quantidade e o Top 10 países por valor.
    
    ### Estatísticas Descritivas
    
    Inicialmente, analisou-se as estatísticas descritivas dos dados, com destaque para algumas métricas por ano e por país.
    
    #### Ano
    '''
    is_exibir_desc_stats_ano = st.checkbox('Estatísticas Descritivas - Ano')
    if is_exibir_desc_stats_ano:
        st.table(desc_stats_ano)
        csv = df_pib_paises_avg_30k_not_exp.to_csv(index=False)
        st.download_button(label='Download Estatísticas Descritivas - Ano (CSV)', data=csv, file_name='desc_stats_ano.csv', mime='text/csv')
    
    
    '''
    #### País
    '''
    is_exibir_desc_stats_pais = st.checkbox('Estatísticas Descritivas - País')
    if is_exibir_desc_stats_pais:
        st.table(desc_stats_pais)
        csv = df_pib_paises_avg_30k_not_exp.to_csv(index=False)
        st.download_button(label='Download Estatísticas Descritivas - País (CSV)', data=csv, file_name='desc_stats_pais.csv', mime='text/csv')
    
    
    '''
    ### Distribuição das Quantidades e Valores
    
    Após, buscou-se entender como era a distruição das quantidades e dos valores. Analisando os dados sem nenhuma agregação, os mesmos não indicaram tantos padrões, mas ao agregar por ano e país, alguns destaques já podiam ser observados.
    
    ### Ano
    Tanto em valor quanto em quantidade, encontram-se algumas frequências até 10 milhões, mas em ambos o que se destaca é um outlier, demonstrado bem a direita o que dificuldade a análise da distribuição dos dados.
    '''
    
    #Valor
    fig, ax = plt.subplots(figsize=(15, 10))

    # Plotar o histograma
    plt.hist(df_exportacao_ano['Value (US)'], bins=10)

    # Ajustar a formatação dos rótulos do eixo y
    plt.ticklabel_format(style='plain', axis='x')

    # Adicionar rótulos e título
    plt.xlabel('Valor (US)')
    plt.ylabel('Frequência - Ano')
    plt.title('Distribuição dos Valores - Agrupado por Ano')

    # Exibir o histograma
    st.pyplot(fig)
    
    
    
    #Quantidade
    fig, ax = plt.subplots(figsize=(15, 10))
    # Plotar o histograma
    plt.hist(df_exportacao_ano['Quantity (KG)'], bins=10)

    # Ajustar a formatação dos rótulos do eixo y
    plt.ticklabel_format(style='plain', axis='x')

    # Adicionar rótulos e título
    plt.xlabel('Quantidade (KG)')
    plt.ylabel('Frequência - Ano')
    plt.title('Distribuição das Quantidades - Agrupado por Ano')

    # Exibir o histograma
    st.pyplot(fig)
    
    
    '''
    ### País
    A análise por país corrobora com a distribuição previamente vista, mostrando que existem 2 países que se destacam dos demais, tanto em quantidade como em valor.
    '''
    
    #Valor
    fig, ax = plt.subplots(figsize=(15, 10))

    # Plotar o histograma
    plt.hist(df_exportacao_pais['Value (US)'], bins=10)

    # Ajustar a formatação dos rótulos do eixo y
    plt.ticklabel_format(style='plain', axis='x')

    # Adicionar rótulos e título
    plt.xlabel('Valor (US)')
    plt.ylabel('Frequência - País')
    plt.title('Distribuição dos Valores - Agrupado por País')

    # Exibir o histograma
    st.pyplot(fig)
    
    
    
    #Quantidade
    fig, ax = plt.subplots(figsize=(15, 10))

    # Plotar o histograma
    plt.hist(df_exportacao_pais['Quantity (KG)'], bins=10)

    # Ajustar a formatação dos rótulos do eixo y
    plt.ticklabel_format(style='plain', axis='x')

    # Adicionar rótulos e título
    plt.xlabel('Quantidade (KG)')
    plt.ylabel('Frequência - País')
    plt.title('Distribuição das Quantidades - Agrupado por País')

    # Exibir o histograma
    st.pyplot(fig)
    
    '''
    ### Análise Temporal
    Neste ponto, é muito importante ver como os dados estão distribuídos ao longo do tempo.   
    '''
    
    # Criando uma paleta categórica com inversão de tons
    custom_palette = sns.color_palette("Blues", n_colors=len(df_exportacao_ano))
    
    
    #Valor
    fig, ax = plt.subplots(figsize=(15, 10))

    # Plotar a evolução do valor ao longo do tempo
    ax = sns.barplot(data=df_exportacao_ano, x='Year', y='Value (US)', hue='Value (US)', palette=custom_palette, dodge=False)
    ax.legend_.remove()  # Remover a legenda do hue
    plt.xlabel('Ano')
    plt.ylabel('Valor (US)')
    plt.title('Evolução do Valor ao Longo do Tempo')

    # Remover a notação científica dos valores nos eixos
    plt.gca().get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, _: '{:,.0f}'.format(x)))

    # Encontrar o maior valor no eixo y
    max_value = df_exportacao_ano['Value (US)'].max()

    # Definir os ticks no eixo y
    yticks = list(plt.yticks()[0])

    # Definir o novo limite do eixo y e os ticks
    plt.ylim(0, max_value + 1)
    plt.yticks(yticks)
    st.pyplot(fig)
    
    
    
    #Quantidade
    fig, ax = plt.subplots(figsize=(15, 10))
    
    # Plotar a evolução da quantidade ao longo do tempo
    ax = sns.barplot(data=df_exportacao_ano, x='Year', y='Quantity (KG)', hue='Quantity (KG)', palette=custom_palette, dodge=False)
    ax.legend_.remove()  # Remover a legenda do hue
    plt.xlabel('Ano')
    plt.ylabel('Quantidade (KG)')
    plt.title('Evolução da Quantidade ao Longo do Tempo')

    # Remover a notação científica dos valores nos eixos
    plt.gca().get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, _: '{:,.0f}'.format(x)))

    # Encontrar o maior valor no eixo y
    max_value = df_exportacao_ano['Quantity (KG)'].max()

    # Definir os ticks no eixo y
    yticks = list(plt.yticks()[0])

    # Definir o novo limite do eixo y e os ticks
    plt.ylim(0, max_value + 1)
    plt.yticks(yticks)

    st.pyplot(fig)
    
    '''
    Percebe-se um outlier em 2013 quanto ao valor e em 2009 quanto a quantidade. Entender como esses dados estão distribuídos por país e por país ao longo do tempo irão nos guiar melhor para entender essas diferenças.
    
    
    ### Análise por País (Top)
    Este ponto irá nos ajudar a entender quais são os principais países importadores tanto por valor quanto por quantidade nos últimos 15 anos e também irá iniciar o detalhamento dos outliers encontrados anteriormente.
    '''
    
    #Valor
    # Criando a figura
    fig, ax = plt.subplots(figsize=(15, 10))

    # Criando uma paleta categórica com inversão de tons
    custom_palette = sns.color_palette("Blues", n_colors=len(df_exportacao_pais_top_10_valor_sorted))

    ax = sns.barplot(data=df_exportacao_pais_top_10_valor_sorted, x='Value (US)', y='Country Name', hue='Value (US)', palette=custom_palette, dodge=False)
    ax.legend_.remove()  # Remover a legenda do hue
    plt.xlabel('Valor (US)')
    plt.ylabel('País')
    plt.title('Top 10 Países por Valor (US)')

    # Remover a notação científica dos valores nos eixos
    plt.gca().get_xaxis().set_major_formatter(ticker.FuncFormatter(lambda x, _: '{:,.0f}'.format(x)))

    st.pyplot(fig)
    
    
    
    #Quantidade
    # Criando a figura
    fig, ax = plt.subplots(figsize=(15, 10))

    # Criando uma paleta categórica com inversão de tons
    custom_palette = sns.color_palette("Blues", n_colors=len(df_exportacao_pais_top_10_qtd_sorted))

    ax = sns.barplot(data=df_exportacao_pais_top_10_qtd_sorted, x='Quantity (KG)', y='Country Name', hue='Quantity (KG)', palette=custom_palette, dodge=False)
    ax.legend_.remove()  # Remover a legenda do hue
    plt.xlabel('Quantidade (KG)')
    plt.ylabel('País')
    plt.title('Top 10 Países por Quantidade (KG)')

    # Remover a notação científica dos valores nos eixos
    plt.gca().get_xaxis().set_major_formatter(ticker.FuncFormatter(lambda x, _: '{:,.0f}'.format(x)))

    st.pyplot(fig)
    
    
    
    '''
    ### Análise Temporal por País
    Agora é possível entender como os principais países se comportaram ao longo do tempo. Entendo melhor os outliers e também encontrando alguns padrões e tendências. 
    '''
    
    #Valor
    fig, ax = plt.subplots(figsize=(15, 10))

    sns.lineplot(data=df_exportacao_pais_top_x, x='Year', y='Value (US)', hue='Country Name')

    # Adicionar rótulos e título
    plt.xlabel('Ano')
    plt.ylabel('Valor (US)')
    plt.title('Valor de Exportação por País ao Longo do Tempo')
    plt.legend(loc='upper right')

    plt.gca().get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, _: '{:,.0f}'.format(x)))

    st.pyplot(fig)
        
    
    
    #Quantidade
    fig, ax = plt.subplots(figsize=(15, 10))

    sns.lineplot(data=df_exportacao_pais_top_x, x='Year', y='Quantity (KG)', hue='Country Name')

    # Adicionar rótulos e título
    plt.xlabel('Ano')
    plt.ylabel('Quantidade (KG)')
    plt.title('Quantidade de Exportação por País ao Longo do Tempo')

    plt.gca().get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, _: '{:,.0f}'.format(x)))

    st.pyplot(fig)
    
    '''
    Em ambos os casos, devidos aos outliers Paraguai e Rússia fica difícil a visualização. Então, pode-se remover pontualmente estes países para entender um pouco melhor o comportamento dos demais países.
    '''
    
    #Valor
    fig, ax = plt.subplots(figsize=(15, 10))
    sns.lineplot(data=df_exportacao_pais_top_x.query("`Country Name` not in ['Rússia', 'Paraguai']"), x='Year', y='Value (US)', hue='Country Name')

    # Adicionar rótulos e título
    plt.xlabel('Ano')
    plt.ylabel('Valor (US)')
    plt.title('Valor de Exportação por País ao Longo do Tempo')

    plt.gca().get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, _: '{:,.0f}'.format(x)))
    st.pyplot(fig)
    
    
    
    #Quantidade
    fig, ax = plt.subplots(figsize=(15, 10))
    sns.lineplot(data=df_exportacao_pais_top_x.query("`Country Name` not in ['Rússia', 'Paraguai']"), x='Year', y='Quantity (KG)', hue='Country Name')

    # Adicionar rótulos e título
    plt.xlabel('Ano')
    plt.ylabel('Quantidade (KG)')
    plt.title('Quantidade de Exportação por País ao Longo do Tempo')

    plt.gca().get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, _: '{:,.0f}'.format(x)))
    st.pyplot(fig)
    
    '''
    Agora, estamos ciente dos dados atuais. Sabemos que a Rússia se destaca na quantidade comprada e possui picos em alguns anos, não demonstrando uma tendência de crescimento. Já o Paraguai - país com maior valor gasto - por outro lado, mostra uma tendência de crescimento nos últimos anos.
    
    Alguns outros países como Espanha e China também tiveram picos de compra em quantidades, contudo, os mdemais países seguem uma certa tendência. 
    '''