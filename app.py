import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go 
from plotly.subplots import make_subplots

df_dados_exportacao = pd.read_csv('./dados/tabela_final.csv')

st.title('FIAPWine')

tab0, tab1, tab2, tab3, tab4 = st.tabs(["Dados de Exportação", "Dados Demográficos", "Dados Econômicos", "Dados Climáticos", "Dados de Avaliações de Vinhos"])

with tab0:
    '''
    ## Dados de Exportação
    '''
    df = pd.DataFrame(df_dados_exportacao)
    st.dataframe(df, use_container_width=True)
    
    
with tab1:
    '''
    ## Dados Demográficos
    '''
    
    
with tab2:
    '''
    ## Dados Econômicos
    '''
    
with tab3:
    '''
    ## Dados Climáticos
    '''
    
with tab4:
    '''
    ## Dados de Avaliações de Vinhos
    '''