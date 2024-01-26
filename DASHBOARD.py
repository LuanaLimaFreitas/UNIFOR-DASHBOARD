import pandas as pd 
import numpy as np 
import plotly.express as px 
import streamlit as st
import datetime

#### CARREGAR O DADO ####
df_hapvida = pd.read_csv('RECLAMEAQUI_HAPVIDA.csv')
df_ibyte = pd.read_csv('RECLAMEAQUI_IBYTE.csv')
df_nagem = pd.read_csv('RECLAMEAQUI_NAGEM.csv')

empresas = ['Hapvida', 'Ibyte', 'Nagem']
df_hapvida['empresa'] = 'Hapvida'
df_ibyte['empresa'] = 'Ibyte'
df_nagem['empresa'] = 'Nagem'
df = pd.concat([df_hapvida, df_ibyte, df_nagem])

## DATETIME ####
df['TEMPO'] = pd.to_datetime(df['TEMPO'])
df['UF'] = df['LOCAL'].str.extract(r'([A-Z]{2})')

#### CALCULO DE FORTALEZA ###


#### STREAMLIT###
st.title('ANALISE COVID')

st.write('Esse dashboard é para a turma 4, 5 e 6')

col1, col2 = st.columns(2)

with col1:
    empresa = st.selectbox(
        'EMPRESA',
        df['empresa'].unique())

with col2:
    uf = st.multiselect(
        'UF', 
        df['UF'].unique())

col3, col4 = st.columns(2)

with col3:
    status = st.multiselect(
        'STATUS', 
        df['STATUS'].unique())

with col4:
    texto = st.slider(
        'Tamanho do texto ',
        0.0, 100.0, (25.0, 75.0))
    #st.write('Values:', texto)

col1, col2, col3 = st.columns(3)
col1.metric("Reclamações", "70 °F")
col2.metric("Respondidas", "9 mph")
col3.metric("% Respondidas", "86%")

contagem_uf = df['UF'].value_counts()
contagem_uf = contagem_uf.sort_values(ascending=True)
st.bar_chart(contagem_uf)

#serie_temporal = df.groupby([df['TEMPO']]).size().reset_index(name='reclamacoes')
#st.line_chart(serie_temporal)
