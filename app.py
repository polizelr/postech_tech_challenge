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

tab0, tab1, tab2, tab3, tab4, tab5 = st.tabs(["Home", "Dados Demográficos", "Dados Econômicos", "Dados Climáticos", "Análise Exploratória", "Fontes"])

with tab0:
    '''
    ## Home

    A partir da análise de dados dos dados brasileiros de vitivinicultura e da correlação destes dados com dados demográficos e dados econômicos, os seguintes insights foram encontrados.
    
    ## Novos Mercados
    Os seguintes países obtiveram destaque e posicionam-se como fortes mercados a serem analisados:
    - Austrália
    - Áustria
    - Bélgica
    - Canadá
    - Itália
    - Suécia
    - Suíça
    '''
    
    # Dados dos países
    data = {
        'Country': ['Australia', 'Austria', 'Belgium', 'Canada', 'Italy', 'Sweden', 'Switzerland'],
        'Highlight': [1, 1, 1, 1, 1, 1, 1]
    }

    # Criação do DataFrame
    df = pd.DataFrame(data)

    # Criação do mapa-múndi com destaque nos países mencionados
    fig = px.choropleth(locations=df['Country'], locationmode='country names', color=df['Highlight'],
                        color_continuous_scale='blues', range_color=[0, 1], labels={'color': 'Highlight'})
    fig.update_layout(geo=dict(showframe=False, projection_type='natural earth'))

    fig.update_coloraxes(showscale=False)

    # Exibição do mapa
    st.plotly_chart(fig)
    
    '''
    Estes países se destacaram tanto na análise do PIB, por possuir um PIB per Capita médio acima de 30 mil dólares anuais, quanto na análise demográfica, com uma população de idade média igual ou superior a 36 anos e, principalmente, expectativa de vida igual ou maior a 77 anos. Estas análises podem ser vistas em detalhas nas respectivas abas.
    
    
    ## Atuais Compradores
    
    Dentre os atuais top importadores do Brasil, Paraguai, Rússia e Haiti destacaram-se.

    '''
    
    # Dados dos países
    data = {
        'Country': ['Paraguay', 'Russia', 'Haiti'],
        'Highlight': [1, 1, 1]
    }

    # Criação do DataFrame
    df = pd.DataFrame(data)

    # Criação do mapa-múndi com destaque nos países mencionados
    fig = px.choropleth(locations=df['Country'], locationmode='country names', color=df['Highlight'],
                        color_continuous_scale='RdPu', range_color=[0, 1], labels={'color': 'Highlight'})
    fig.update_layout(geo=dict(showframe=False, projection_type='natural earth'))

    fig.update_coloraxes(showscale=False)

    # Exibição do mapa
    st.plotly_chart(fig)
    
    '''
    A Rússia por ser o país que comprou as maiores quantidades nos últimos 15 anos. Paraguai e Haiti, mesmo apresentando valores abaixos nos 3 indicadores demográficos analisados perante aos demais países, são os que apresentam grande tendência de crescimento nos últimos anos. Paraguai ainda se destaca por ter sido o país com maior valor gasto nos últimos 15 anos. Estes dados estão detalhamente analisados na aba Análise Exploratória.
    '''
    
    '''
    ## Melhorias de Qualidade
    
    Além disso, entendeu-se a importância da produção e da qualidade das uvas, não apenas pensando na exportação, mas também no impacto positivo no comércio interno. Então, foi realizado um estudo específico sobre como mitigar os riscos associados à produção de uva.
    '''
    
    '''
    ## Dados de Exportação
    
    Este é o atual montante de exportação nos últimos 15 anos, mostrando o país de origem (Braisl), país de destino, quantidade de litros de vinho exportados e valor em US$.
    '''
    df_dados_exportacao = pd.read_csv('./dados/tabela_final.csv')
    df_dados_exportacao['Ano'] = df_dados_exportacao['Ano'].astype(str)
    st.dataframe(df_dados_exportacao, use_container_width=True, hide_index=True)
    csv = df_dados_exportacao.to_csv(index=False)
    st.download_button(label='Download (CSV)', data=csv, file_name='exportacao_15_anos.csv', mime='text/csv')
    
    
with tab1:
    #Dados
    
    #Base
    df_exportacao_pais_top_x_pib_demographic = pd.read_csv('./dados/df_exportacao_pais_top_x_pib_demographic.csv')
    df_exportacao_demographic = pd.read_csv('./dados/df_exportacao_demographic.csv')
    paises_top_10_exp = list(df_exportacao_pais_top_x_pib_demographic['Country Name'])
    
    #População Total
    df_exportacao_pais_pib_demograficos_pop = df_exportacao_pais_top_x_pib_demographic.groupby('Country Name').agg({'Total Population Millions': 'mean'}).reset_index()
    df_exportacao_pais_pib_demograficos_pop_sorted = df_exportacao_pais_pib_demograficos_pop.sort_values(by='Total Population Millions', ascending=False)
    
    #Média Idade
    df_exportacao_pais_pib_demograficos_med_age = df_exportacao_pais_top_x_pib_demographic.groupby('Country Name').agg({'Median Age': 'mean'}).reset_index()
    df_exportacao_pais_pib_demograficos_med_age_sorted = df_exportacao_pais_pib_demograficos_med_age.sort_values(by='Median Age', ascending=False)
    df_exportacao_pais_nao_top_x_demographic_med_age_sorted = df_exportacao_demographic.query("(`Median Age` >= 36 and `Total Population Millions` >= 10) and `Country Name` not in @paises_top_10_exp").sort_values(by='Median Age', ascending=False)
    df_exportacao_pais_nao_top_x_demographic_med_age_sorted = df_exportacao_pais_nao_top_x_demographic_med_age_sorted[['Country Name', 'Median Age']]
    
    #Expectativa de Vida
    df_exportacao_pais_pib_demograficos_exp_vida = df_exportacao_pais_top_x_pib_demographic.groupby('Country Name').agg({'Life Expectation': 'mean'}).reset_index()
    df_exportacao_pais_pib_demograficos_sorted = df_exportacao_pais_pib_demograficos_exp_vida.sort_values(by='Life Expectation', ascending=False)
    df_exportacao_pais_nao_top_x_demographic_life_exp_sorted = df_exportacao_demographic.query("`Life Expectation` >= 77 and `Country Name` not in @paises_top_10_exp").sort_values(by='Life Expectation', ascending=False)
    df_exportacao_pais_nao_top_x_demographic_life_exp_sorted = df_exportacao_pais_nao_top_x_demographic_life_exp_sorted[['Country Name', 'Life Expectation']].head(10)

    # Juntando os 3
    df_exportacao_pais_nao_top_x_demographic_pop_medage_lifeexp_sorted = df_exportacao_demographic.query("(`Life Expectation` >= 77 and `Median Age` >= 36 and `Total Population Millions` >= 6.1) and `Country Name` not in @paises_top_10_exp").sort_values(by='Total Population Millions', ascending=False)

    '''
    ## Dados Demográficos [2]
    
    https://population.un.org/wpp/

    A Revisão de 2022 das Perspectivas da População Mundial é a vigésima sétima edição das estimativas e projeções populacionais oficiais das Nações Unidas que foram preparadas pela Divisão de População do Departamento de Assuntos Econômicos e Sociais do Secretariado das Nações Unidas.
    
    Apresenta estimativas populacionais de 1950 até o presente para 237 países ou áreas, sustentadas por análises de tendências demográficas históricas. Esta última avaliação considera os resultados de 1.758 censos populacionais nacionais realizados entre 1950 e 2022, bem como informações de sistemas de registro vital e de 2.890 pesquisas de amostra nacionalmente representativas nos níveis global, regional e nacional.
    
    ### População
    Ao analisar a população média dos top importadores, podemos ver que não existe um padrão definido:
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
    is_exibir_exp_pop = st.checkbox('Tabela com a população média (em milhões) dos Top Importadores')
    if is_exibir_exp_pop:
        st.dataframe(df_exportacao_pais_pib_demograficos_pop_sorted, use_container_width=True, hide_index=True)
        csv = df_exportacao_pais_pib_demograficos_pop_sorted.to_csv(index=False)
        st.download_button(label='Download (CSV)', data=csv, file_name='populacao_media_paises_top_10.csv', mime='text/csv')    
    
    
    '''
    - A China possui uma população média muito maior do que a dos outros países, o que poderia gerar pensamentos como o de buscar por outros mercados que possuem a mesma característica, como a Índia, por exemplo.
    - Contudo, os demais países possuem uma população média consideravelmente menor (Países Baixos, Haiti e Paraguai, especialmente), o que nos leva a acreditar que esse indicador, se analisado isoladamente, não deve ser um fator com grande peso na tomada de decisão.
    '''
    
    
    '''
    ### Idade Média
    Ao analisar a Idade Média da população, porém, temos alguns destaques:
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
    is_exibir_exp_med_age = st.checkbox('Tabela com a idade média dos Top Importadores')
    if is_exibir_exp_med_age:
        st.dataframe(df_exportacao_pais_pib_demograficos_med_age_sorted, use_container_width=True, hide_index=True)
        csv = df_exportacao_pais_pib_demograficos_med_age_sorted.to_csv(index=False)
        st.download_button(label='Download (CSV)', data=csv, file_name='idade_media_paises_top_10.csv', mime='text/csv') 
    
    '''
    Uma parte considerável dos top países importadores do Brasil tem uma idade média na casa dos 36 anos, com destaque para o Japão e a Alemanha.
    '''
    
    ####### Gráfico de barras #####
    ax.axvline(x=36, color='red', linestyle='--')
    st.pyplot(fig)
    #############################
    
    '''
    Esse fato pode indicar um potencial mercado. Portanto, vamos utilizar essa média (36 anos) como parâmetro para buscar outros países que possuem uma idade média a partir dessa faixa.
    '''

    ####### Gráfico de barras #####
    # Criando a figura
    fig, ax = plt.subplots(figsize=(15, 10))

    # Criando uma paleta categórica com inversão de tons
    custom_palette = sns.color_palette("Blues", n_colors=len(df_exportacao_pais_nao_top_x_demographic_med_age_sorted))

    sns.barplot(data=df_exportacao_pais_nao_top_x_demographic_med_age_sorted, x='Median Age', y='Country Name', hue='Median Age', palette=custom_palette, dodge=False, ax=ax)
    ax.legend_.remove()  # Remover a legenda do hue
    ax.set_xlabel('Idade média da população')
    ax.set_ylabel('País')
    ax.set_title('Top Países Importadores - Idade média da população')

    # Remover a notação científica dos valores nos eixos
    ax.get_xaxis().set_major_formatter(ticker.FuncFormatter(lambda x, _: '{:,.0f}'.format(x)))
    
    st.pyplot(fig)
    #############################
    
    is_exibir_exp_med_age_pais_nao_top_x = st.checkbox('Tabela com a idade média dos países que não estão entre os Top Importadores')
    if is_exibir_exp_med_age_pais_nao_top_x:
        st.dataframe(df_exportacao_pais_nao_top_x_demographic_med_age_sorted, use_container_width=True, hide_index=True)
        csv = df_exportacao_pais_nao_top_x_demographic_med_age_sorted.to_csv(index=False)
        st.download_button(label='Download (CSV)', data=csv, file_name='idade_media_paises_fora_top_10.csv.csv', mime='text/csv') 
    
    '''
    ### Expectativa de Vida
    Ao analisar a expectativa de vida, vemos que os principais compradores do Brasil possuem uma expectativa de vida consideravelmente alta, reforçando a relação com a análise anterior.
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

    is_exibir_exp_life_exp_pais_nao_top_x = st.checkbox('Tabela com a expectativa de vida média dos países que estão entre os Top Importadores')
    if is_exibir_exp_life_exp_pais_nao_top_x:
        st.dataframe(df_exportacao_pais_pib_demograficos_sorted, use_container_width=True, hide_index=True)
        csv = df_exportacao_pais_pib_demograficos_sorted.to_csv(index=False)
        st.download_button(label='Download (CSV)', data=csv, file_name='expectativa_media_paises_top_10.csv.csv', mime='text/csv') 

    
    '''
    A partir disso, podemos então destacar outros mercados com expectativa de vida elevada como fortes candidatos.
    '''
    ####### Gráfico de barras #####
    # Criando a figura
    fig, ax = plt.subplots(figsize=(15, 10))

    # Criando uma paleta categórica com inversão de tons
    custom_palette = sns.color_palette("Blues", n_colors=len(df_exportacao_pais_nao_top_x_demographic_life_exp_sorted))

    sns.barplot(data=df_exportacao_pais_nao_top_x_demographic_life_exp_sorted, x='Life Expectation', y='Country Name', hue='Life Expectation', palette=custom_palette, dodge=False, ax=ax)
    ax.legend_.remove()  # Remover a legenda do hue
    ax.set_xlabel('Expectativa de vida média da população')
    ax.set_ylabel('País')
    ax.set_title('Top Países Importadores - Expectativa de vida média da população')

    # Remover a notação científica dos valores nos eixos
    ax.get_xaxis().set_major_formatter(ticker.FuncFormatter(lambda x, _: '{:,.0f}'.format(x)))
    
    st.pyplot(fig)
    #############################
    
    is_exibir_exp_expec_age_pais_nao_top_x = st.checkbox('Tabela com a expectativa média de vida dos países que não estão entre os Top Importadores')
    if is_exibir_exp_expec_age_pais_nao_top_x:
        st.dataframe(df_exportacao_pais_nao_top_x_demographic_life_exp_sorted, use_container_width=True, hide_index=True)
        csv = df_exportacao_pais_nao_top_x_demographic_life_exp_sorted.to_csv(index=False)
        st.download_button(label='Download (CSV)', data=csv, file_name='expectativa_media_paises_fora_top_10.csv.csv', mime='text/csv')     


    '''
    ### TODOS...
    E se buscarmos simultaneamente de acordo com os 2 últimos indicadores?
    - Idade média da população maior ou igual a 36 anos;
    - Expectativa de vida maior ou igual a 77 anos;
    
    Além disso, apesar de a população total não ser, de maneira isolada, um indicador forte, a tendência é de que quanto maior a população do país, mais pessoas disponíveis para consumir. Portanto, vamos selecionar apenas países com uma população média maior que 6.1 milhões - população do Paraguai, o país de menor população entre os top importadores.

    Os países da lista abaixo são exemplos de países cujo mercado possui bom potencial para ser explorado.
    '''
    st.dataframe(df_exportacao_pais_nao_top_x_demographic_pop_medage_lifeexp_sorted, use_container_width=True, hide_index=True)
    csv = df_exportacao_pais_nao_top_x_demographic_pop_medage_lifeexp_sorted.to_csv(index=False)
    st.download_button(label='Download (CSV)', data=csv, file_name='potenciais_mercados.csv', mime='text/csv') 


    
    
    
with tab2:
    #Dados
    df_exportacao_pais_pib = pd.read_csv('./dados/df_exportacao_pais_pib.csv')    
    df_exportacao_pais_top_x_pib_sorted = df_exportacao_pais_pib.sort_values(by='GDP', ascending=False)    
    df_pib_paises_avg_30k_not_exp = pd.read_csv('./dados/df_pib_paises_avg_30k_not_exp.csv')    
    
    '''
    ## Dados Econômicos
    
    https://data.worldbank.org/indicator/NY.GDP.MKTP.CD
    
    O PIB per capita é o produto interno bruto dividido pela população no meio do ano.
    
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
        st.download_button(label='Download (CSV)', data=csv, file_name='exp_top_pib.csv', mime='text/csv')
        
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
        st.dataframe(df_pib_paises_avg_30k_not_exp, use_container_width=True, hide_index=True)
        csv = df_pib_paises_avg_30k_not_exp.to_csv(index=False)
        st.download_button(label='Download (CSV)', data=csv, file_name='insights_pib.csv', mime='text/csv')

with tab3:
    #Dados
    df_dados_climaticos_media_mes = pd.read_csv('./dados/dados_climaticos_rs_media_mes_versao_final.csv')
    df_dados_climaticos_media_ano = pd.read_csv('./dados/dados_climaticos_rs_media_ano_versao_final.csv')
    
    '''
    ## Dados Climáticos
    
    O Rio Grande do Sul possui o clima favorável para o cultivo de uvas de qualidade para a produção de vinhos, uma vez que se aproxima ao clima mediterrâneo, com verões quentes e invernos frios.
    
    Contudo, faz-se extremamente necessário analisar as variações climáticas, para que ações relativas ao manejo das videiras sejam tomadas de modo que a produção, qualidade das uvas e, consequentemente, o comércio interno e de exportação não sejam afetados.
    
    '''
    
    
    # -----------------------------------------------------------------------------------------------------------------------------
    
    '''
    ## Temperatura
    
    O Rio Grande do Sul apresenta uma temperatura média compensada que varia entre  12°C a 24°C, dependendo da localização específica. 
    
    Através da análise do gráfico abaixo, podemos constatar que durante o verão (dezembro a fevereiro), as temperaturas médias mínima e máxima variam entre 17°C a 30°C. No inverno (junho a agosto), as temperaturas médias mínima e máxima caem consideravelmente e variam entre 8°C a 21°C. Já no outono (março a maio) e na primavera (setembro a novembro) variam entre 11°C a 28°C.
    
    Contudo, durante o verão, ondas de calor podem ocorrer, causando desidratação e estresse térmico nas videiras. No inverno, as geadas ocasionadas por temperaturas abaixo de zero, podem danificar as plantas e reduzir a produtividade.
    
    
    '''
    
    # Criar o gráfico
    df_dc_mes = pd.DataFrame(df_dados_climaticos_media_mes) 
    
    fig_dc_2 = go.Figure()

    fig_dc_2.add_trace(go.Scatter(x=df_dc_mes['mes'], y=df_dc_mes['temperatura_media_compensada'], name='Temperatura Média Compensada'))
    fig_dc_2.add_trace(go.Scatter(x=df_dc_mes['mes'], y=df_dc_mes['temperatura_min_media'], name='Temperatura Média Mínima'))
    fig_dc_2.add_trace(go.Scatter(x=df_dc_mes['mes'], y=df_dc_mes['temperatura_max_media'], name='Temperatura Média Máxima', line=dict(color='rgb(0, 0, 120)')))
    fig_dc_2.add_annotation(x=0, y=-0.30, showarrow=False, text="Fonte: INMET - Instituto Nacional de Meteorologia", font=dict(size=12, color="black"),
                       xref="paper", yref="paper")
    fig_dc_2.update_layout(
        title='Temperaturas Máxima, Mínima e Média Compensada Mensal no Período de 2007 até 2021',
        xaxis=dict(
            title='Mês',
            tickmode='linear',
            tick0=df_dc_mes['mes'].min(),
            dtick=1
        ),
        yaxis=dict(
            title='Temperatura Média (°C)',
            range=[0, 30]
        ),
        showlegend=True,
        legend=dict(
            title='Variáveis',
            x=0,            
            y=-1,                        
            bordercolor='Black',
            borderwidth=1
        ),
        plot_bgcolor='white',
        grid=dict(
            rows=1,
            columns=1,
            subplots=[['xy']]
        )
    )
    
    # Adicionando linhas verticais
    fig_dc_2.add_shape(
        type='line',
        x0=1.5,
        y0=0,
        x1=1.5,
        y1=30,
        line=dict(
            color='gray',
            width=1,
            dash='dash'
        )
    )
    fig_dc_2.add_shape(
        type='line',
        x0=4.5,
        y0=0,
        x1=4.5,
        y1=30,
        line=dict(
            color='gray',
            width=1,
            dash='dash'
        )
    )
    fig_dc_2.add_shape(
        type='line',
        x0=7.5,
        y0=0,
        x1=7.5,
        y1=30,
        line=dict(
            color='gray',
            width=1,
            dash='dash'
        )
    )
    fig_dc_2.add_shape(
        type='line',
        x0=10.5,
        y0=0,
        x1=10.5,
        y1=30,
        line=dict(
            color='gray',
            width=1,
            dash='dash'
        )
    )

    # Renderizar o gráfico utilizando o Streamlit
    st.plotly_chart(fig_dc_2, use_container_width=True)
    
    
    
   # ----------------------------------------------------------------------------------------------------------------------------- 
        
    '''
    ## Precipitação
    
    A precipitação no Rio Grande do Sul é bem distribuída ao longo do ano, porém apresenta algumas variações sazonais significativas.
         
    Através da análise do gráfico abaixo, podemos constatar que as estações mais chuvosas são a primavera (setembro à novembro) e o verão (dezembro à fevereiro), 
    com precipitação média mensal variando entre 120mm à 200mm. O inverno (junho à agosto) apresenta níveis intermediários de precipitação variando entre 120mm à 150mm.
    Enquanto no outono (março à maio), a precipitação é menor, variando entre 100mm à 150mm. O outono corresponde ao período de seca no estado.
    
    Contudo, é importante ressaltar que o Rio Grande do Sul apresenta episódios de chuvas intensas, especialmente no verão, que causam encharcamento do solo, afetando assim a saúde das videiras e contribuindo para o aumento do risco de doenças, como exemplo doenças fúngicas (míldio, oídio e mofo-cinzento) e bacterianas. 
    
    '''
    
    # Criar o gráfico
    df_dc_mes = pd.DataFrame(df_dados_climaticos_media_mes) 
    
    fig_dc_2 = go.Figure()

    fig_dc_2.add_trace(go.Scatter(x=df_dc_mes['mes'], y=df_dc_mes['precipitacao'], name='Precipitação Média (mm)'))    
    fig_dc_2.add_annotation(x=0, y=-0.30, showarrow=False, text="Fonte: INMET - Instituto Nacional de Meteorologia", font=dict(size=12, color="black"),
                       xref="paper", yref="paper")
    fig_dc_2.update_layout(
        title='Precipitação Média Mensal no Período de 2007 até 2021',
        xaxis=dict(
            title='Mês',
            tickmode='linear',
            tick0=df_dc_mes['mes'].min(),
            dtick=1
        ),
        yaxis=dict(
            title='Precipitação Média (mm)',
            #range=[0, 30]
        ),
        showlegend=True,
        legend=dict(
            title='Variáveis',
            x=0,            
            y=-1,                        
            bordercolor='Black',
            borderwidth=1
        ),
        plot_bgcolor='white',
        grid=dict(
            rows=1,
            columns=1,
            subplots=[['xy']]
        )
    )
    
    # Adicionando linhas verticais
    fig_dc_2.add_shape(
        type='line',
        x0=1.5,
        y0=0,
        x1=1.5,
        y1=200,
        line=dict(
            color='gray',
            width=1,
            dash='dash'
        )
    )
    fig_dc_2.add_shape(
        type='line',
        x0=4.5,
        y0=0,
        x1=4.5,
        y1=200,
        line=dict(
            color='gray',
            width=1,
            dash='dash'
        )
    )
    fig_dc_2.add_shape(
        type='line',
        x0=7.5,
        y0=0,
        x1=7.5,
        y1=200,
        line=dict(
            color='gray',
            width=1,
            dash='dash'
        )
    )
    fig_dc_2.add_shape(
        type='line',
        x0=10.5,
        y0=0,
        x1=10.5,
        y1=200,
        line=dict(
            color='gray',
            width=1,
            dash='dash'
        )
    )

    # Renderizar o gráfico utilizando o Streamlit
    st.plotly_chart(fig_dc_2, use_container_width=True)
    
    # -----------------------------------------------------------------------------------------------------------------------------    
    
    '''
    ## Umidade Relativa do Ar
    
    A umidade relativa do ar no Rio Grande do Sul possui médias anuais que variam entre 70% a 90%, devido a proximidade do oceano Atlântico e pela circulação de massas de ar úmidas.
    
    Ela desempenha um papel crucial durante todo o ciclo de cultivo da videira, influenciando tanto os aspectos fisiológicos da planta quanto a ocorrência de doenças causadas por fungos e bactérias. Quando a umidade relativa do ar é alta, isso tende a promover o crescimento de ramos mais vigorosos, acelerar a brotação das folhas e contribuir para uma vida útil prolongada da planta. No entanto, se essa alta umidade estiver combinada com temperaturas elevadas, há um aumento significativo na incidência de doenças fúngicas e bacterianas. Essas condições propiciam um ambiente mais favorável para a proliferação dessas doenças, representando um desafio para a saúde da videira ao longo do seu ciclo de crescimento. (Fonte: Sistema de Produção - Cultivo da Videira)
    '''
    
    
    # Criar o gráfico
    df_dc_mes = pd.DataFrame(df_dados_climaticos_media_mes) 
    
    fig_dc_2 = go.Figure()

    fig_dc_2.add_trace(go.Scatter(x=df_dc_mes['mes'], y=df_dc_mes['umidade_relativa_ar_media'], name='Umidade Relativa do Ar'))    
    fig_dc_2.add_annotation(x=0, y=-0.30, showarrow=False, text="Fonte: INMET - Instituto Nacional de Meteorologia", font=dict(size=12, color="black"),
                       xref="paper", yref="paper")
    fig_dc_2.update_layout(
        title='Umidade Relativa do Ar Média Mensal no Período de 2007 até 2021',
        xaxis=dict(
            title='Mês',
            tickmode='linear',
            tick0=df_dc_mes['mes'].min(),
            dtick=1
        ),
        yaxis=dict(
            title='Umidade Relativa do Ar (%)',
            range=[50, 90]
        ),
        showlegend=True,
        legend=dict(
            title='Variáveis',
            x=0,            
            y=-1,                        
            bordercolor='Black',
            borderwidth=1
        ),
        plot_bgcolor='white',
        grid=dict(
            rows=1,
            columns=1,
            subplots=[['xy']]
        )
    )
    
    # Adicionando linhas verticais
    fig_dc_2.add_shape(
        type='line',
        x0=1.5,
        y0=0,
        x1=1.5,
        y1=200,
        line=dict(
            color='gray',
            width=1,
            dash='dash'
        )
    )
    fig_dc_2.add_shape(
        type='line',
        x0=4.5,
        y0=0,
        x1=4.5,
        y1=200,
        line=dict(
            color='gray',
            width=1,
            dash='dash'
        )
    )
    fig_dc_2.add_shape(
        type='line',
        x0=7.5,
        y0=0,
        x1=7.5,
        y1=200,
        line=dict(
            color='gray',
            width=1,
            dash='dash'
        )
    )
    fig_dc_2.add_shape(
        type='line',
        x0=10.5,
        y0=0,
        x1=10.5,
        y1=200,
        line=dict(
            color='gray',
            width=1,
            dash='dash'
        )
    )

    # Renderizar o gráfico utilizando o Streamlit
    st.plotly_chart(fig_dc_2, use_container_width=True)
    
    
    # -----------------------------------------------------------------------------------------------------------------------------    
    
    '''
    ## Padrões Sazonais
    
    Conforme podemos observar no gráfico abaixo, o estado do Rio Grande do Sul experimenta as quatro estações do ano de forma bem definida. O outono (março a maio) é caracterizado por temperaturas amenas e queda na quantidade de chuvas. No inverno (junho a agosto), as temperaturas 
    são mais baixas e podem ocorrer geadas. Na primavera (setembro a novembro), as temperaturas começam a subir e a precipitação é intensa. No verão (dezembro a fevereiro), as temperaturas são mais elevadas e podem ocorrer episódios de chuvas intensas.   
    
    
    '''
    
    # Create figure with secondary y-axis
    fig_dc_3 = go.Figure()
    fig_dc_3 = make_subplots(specs=[[{"secondary_y": True}]])
    

    # Add traces
    fig_dc_3.add_trace(
        go.Scatter(x=df_dc_mes['mes'], y=df_dc_mes['temperatura_media_compensada'], name='Temperatura Média Compensada (°C)'),
        secondary_y=False,
    )

    fig_dc_3.add_trace(
        go.Scatter(x=df_dc_mes['mes'], y=df_dc_mes['precipitacao'], name="Precipitação Média (mm)"),
        secondary_y=True,
    )
    
    fig_dc_3.add_annotation(x=0, y=-0.30, showarrow=False, text="Fonte: INMET - Instituto Nacional de Meteorologia", font=dict(size=12, color="black"),
                       xref="paper", yref="paper")

    # Add figure title
    fig_dc_3.update_layout(
        title_text="Temperatura Média Compensada e Precipitação Média Mensal no Período de 2007 até 2021",
        showlegend=True,
        legend=dict(
            title='Variáveis',
            x=0,            
            y=-1,                        
            bordercolor='Black',
            borderwidth=1
        ),
        grid=dict(
            rows=1,
            columns=1,
            subplots=[['xy']]
            
        )
    )

    # Set x-axis title
    fig_dc_3.update_xaxes(title_text="Mês")

    # Set y-axes titles
    fig_dc_3.update_yaxes(title_text="Temperatura Média Compensada (°C)", range=[0, 32], secondary_y=False)
    fig_dc_3.update_yaxes(title_text="Precipitação Média (mm)", range=[100, 202], secondary_y=True)
    
    # Adicionando linhas verticais
    fig_dc_3.add_shape(
        type='line',
        x0=1.5,
        y0=0,
        x1=1.5,
        y1=200,
        line=dict(
            color='gray',
            width=1,
            dash='dash'
        )
    )
    fig_dc_3.add_shape(
        type='line',
        x0=4.5,
        y0=0,
        x1=4.5,
        y1=200,
        line=dict(
            color='gray',
            width=1,
            dash='dash'
        )
    )
    fig_dc_3.add_shape(
        type='line',
        x0=7.5,
        y0=0,
        x1=7.5,
        y1=200,
        line=dict(
            color='gray',
            width=1,
            dash='dash'
        )
    )
    fig_dc_3.add_shape(
        type='line',
        x0=10.5,
        y0=0,
        x1=10.5,
        y1=200,
        line=dict(
            color='gray',
            width=1,
            dash='dash'
        )
    )
    
    st.plotly_chart(fig_dc_3, use_container_width=True)
    
    
    
    
    # -----------------------------------------------------------------------------------------------------------------------------
       
    '''
    ## Ações para Melhoria na Quantidade e Qualidade da Produção de Vinhos 
    
    
    Através da análise dos dados climáticos do Rio Grande do Sul, as seguintes ações serão adotadas a fim de mitigar os riscos associados 
    às mudanças climáticas e, dessa forma, garantir a quantidade e a qualidade da produção de vinho para a exportação e comercialização interna: 
    
    1. Seleção de variedades de uva mais adaptadas às condições climáticas futuras, levando em conta fatores como resistência ao calor, seca e doenças fúngicas, para que sejam utilizadas como porta-enxerto para variedades de uvas que são mais sensíveis à doenças, como por exemplo a Vitis Vinifera L.
    
    2. Implementação de sistemas de irrigação eficientes para garantir o suprimento adequado de água durante o período de seca, que corresponde aos meses de março à maio. 
    
    3. Adoção de práticas de manejo do solo que melhorem a drenagem e reduzam o risco de encharcamento durante os períodos de chuvas intensas.

    4. Monitoramento e controle rigorosos de doenças fúngicas, nos períodos de alta umidade relativa do ar associado à altas temperaturas, considerando estes períodos de maior incidência dessas doenças.
    
    5. Investimento em tecnologias e práticas de manejo que ajudem a mitigar os efeitos do estresse térmico nas vinhas, como a proteção contra radiação solar excessiva.
    
    
    É importante ressaltar que o monitoramento dos dados climáticos e as ações para a gestão adequada dos riscos associados à produção de vinho serão contínuos, uma vez que fenômenos como o aquecimento global e o El Niño podem influenciar drasticamente as previsões climáticas de longo prazo.   
    
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
    
    Foi definido como base principal a Embrapa e analisados os dados de vitivinicultura disponíveis em:
    
    http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_01
    
    O foco é o mercado externo, então as análises foram feitas em cimas do dataset de exportação. Foram filtrados os dados entre 2007 e 2021. Além disso, devido a grande variedade de países disponíveis, a análise concentrou-se nos Top X País Importadores, isto é, o Top 10 países por quantidade e o Top 10 países por valor.
    
    ### Estatísticas Descritivas
    
    Inicialmente, analisou-se as estatísticas descritivas dos dados, com destaque para algumas métricas por ano e por país.
    
    #### Ano
    '''
    is_exibir_desc_stats_ano = st.checkbox('Estatísticas Descritivas - Ano')
    if is_exibir_desc_stats_ano:
        st.table(desc_stats_ano)
        csv = desc_stats_ano.to_csv(index=False)
        st.download_button(label='Download (CSV)', data=csv, file_name='desc_stats_ano.csv', mime='text/csv')
    
    
    '''
    #### País
    '''
    is_exibir_desc_stats_pais = st.checkbox('Estatísticas Descritivas - País')
    if is_exibir_desc_stats_pais:
        st.table(desc_stats_pais)
        csv = desc_stats_pais.to_csv(index=False)
        st.download_button(label='Download (CSV)', data=csv, file_name='desc_stats_pais.csv', mime='text/csv')
    
    
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
    
    Alguns outros países como Espanha e China também tiveram picos de compra em quantidades, contudo, os demais países seguem uma certa tendência. 
    '''
    
    
with tab5:
    fontes_markdown = '''
        ## Fontes

        **Dados da Vitivinicultura**  
        http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_01
        
        **Dados Demográficos**  
        https://population.un.org/wpp/
        
        **Dados Econômicos**  
        https://data.worldbank.org/indicator/NY.GDP.MKTP.CD

        **INMET: Instituto Nacional de Meteorologia**  
        https://portal.inmet.gov.br/  
        Para esta análise, foram utilizados dados no período entre 01/01/2007 até 31/12/2021, provenientes das estações: BAGE, BOM JESUS, CAXIAS DO SUL, CRUZ ALTA, LAGOA VERMELHA, PASSO FUNDO, PELOTAS, PORTO ALEGRE, SANTA MARIA, SANTA VITORIA DO PALMAR e SAO LUIZ GONZAGA. 

        **Atlas Climático - Rio Grande do Sul**  
        https://www.agricultura.rs.gov.br/upload/arquivos/202005/13110034-atlas-climatico-rs.pdf

        **O Cultivo e o Mercado da Uva**  
        https://sebrae.com.br/sites/PortalSebrae/artigos/o-cultivo-e-o-mercado-da-uva,ae8da5d3902e2410VgnVCM100000b272010aRCRD

        **Sistema de Produção - Cultivo da Videira**  
        http://www.cpatsa.embrapa.br:8080/sistema_producao/spuva/clima.html
        
    '''
    
    st.markdown(fontes_markdown)