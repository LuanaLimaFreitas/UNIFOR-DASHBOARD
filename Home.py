import pandas as pd 
import numpy as np 
import plotly.express as px 
import streamlit as st
import datetime

st.set_page_config(page_title='Luana L F', page_icon=':bar_chart:', layout='wide')

#### CARREGAR O DADO ####
df_hapvida = pd.read_csv('dado/RECLAMEAQUI_HAPVIDA.csv')
df_ibyte = pd.read_csv('dado/RECLAMEAQUI_IBYTE.csv')
df_nagem = pd.read_csv('dado/RECLAMEAQUI_NAGEM.csv')

empresas = ['Hapvida', 'Ibyte', 'Nagem']
df_hapvida['empresa'] = 'Hapvida'
df_ibyte['empresa'] = 'Ibyte'
df_nagem['empresa'] = 'Nagem'
df = pd.concat([df_hapvida, df_ibyte, df_nagem])

df['TEMPO'] = pd.to_datetime(df['TEMPO'])
df['UF'] = df['LOCAL'].str.extract(r'([A-Z]{2})')
df['reclamacoes'] = 1

# Title
st.title('MBA CIÊNCIA DE DADOS - TURMA6')
st.write(
    """
    ### Dashboards Bibliotecas R/Phyton
    Professor: Jorge Luiz

    Aluno: Luana Lima Freitas

    ### Exercícios 2
    Utilize os arquivos do **RECLAME AQUI** e crie um dashboard com algumas caracteristicas. 
    """
)

# Logo
c1, c2, c3, c4, c5, c6, c7, c8, c9 = st.columns(9)
c3.image("images/logo_hapvida.png")
c5.image("images/logo_ibyte.png")
c7.image("images/logo_nagem.png")

# Introduction
st.write(
    """
    O painel deve conter tais informações: 
    1. Série temporal do número de reclamações. 
    2. Frequência de reclamações por estado. 
    3. Frequência de cada tipo de **STATUS**
    4. Distribuição do tamanho do texto (coluna **DESCRIÇÃO**) 

    Alguns botões devem ser implementados no painel para operar filtros dinâmicos. Alguns exemplos:: 
    1. Seletor da empresa para ser analisada. 
    2. Seletor do estado. 
    3. Seletor por **STATUS**
    4. Seletor de tamanho do texto 

    Faça o deploy da aplicação. Dicas: 
    https://www.youtube.com/watch?v=vw0I8i7QJRk&list=PLRFQn2r6xhgcDMhp9NCWMqDYGfeeYsn5m&index=16&t=252s
    https://www.youtube.com/watch?v=HKoOBiAaHGg&t=515s

    Exemplo do github
    https://github.com/jlb-gmail/streamlit_teste
    """
)
