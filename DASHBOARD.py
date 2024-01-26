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
df['reclamacoes'] = 1


#### STREAMLIT###
with st.sidebar:
    #empresa = st.selectbox(
    empresa = st.radio(
        'EMPRESA',
        df['empresa'].unique())

df_local1=df[df['empresa'] == empresa]

col1, col2 = st.columns([1, 5])

with col1:
    if empresa=='Hapvida': 
        st.image("logo_hapvida-saude_8GHR9a.PNG")
    if empresa=='Ibyte':       
        st.image("logo_ibyte-loja-fisica_SO0yli.PNG")
    if empresa=='Nagem':       
        st.image("logo_nagem-loja-virtual_GFaJZ0.PNG")

with col2:
    st.title('ReclameAQUI')    

col3, col4 = st.columns(2)

with col3:
    uf = st.multiselect(
        'UF', 
        df_local1['UF'].unique())
    
with col4:
    status = st.multiselect(
        'STATUS', 
        df_local1['STATUS'].unique())

df_local2=df_local1
if len(uf) > 0:
    df_local2=df_local1[df_local1['UF'].isin(uf)]

if len(status) == 0:
    df_local=df_local2
else:
    df_local=df_local2[df_local2['STATUS'].isin(status)]


reclamacoes_local=df_local['reclamacoes'].sum()
df_respondidas = df_local[(df_local['STATUS'] == 'Resolvido') | (df_local['STATUS'] == 'Respondida')]
respondidas_local=df_respondidas['reclamacoes'].sum()
percentagem = respondidas_local / reclamacoes_local * 100

col1, col2, col3 = st.columns(3)
col1.metric("Reclamações", reclamacoes_local)
col2.metric("Respondidas", respondidas_local)
col3.metric("% Respondidas", "{:.2f}%".format(percentagem))


status_unicos = df_local['STATUS'].value_counts()
colunas = st.columns(len(status_unicos))
for i, (valor, contagem) in enumerate(status_unicos.items()):
    coluna = colunas[i]
    coluna.metric(valor, contagem)  

contagem_uf = df_local['UF'].value_counts()
contagem_uf = contagem_uf.sort_values(ascending=True)
st.bar_chart(contagem_uf)

#contagem_por_dia = df_local['TEMPO'].dt.date.value_counts().sort_index()
#chart_data = pd.DataFrame({'TEMPO': contagem_por_dia.index, 'contagem': contagem_por_dia.values})
#chart_data['TEMPO'] = pd.to_datetime(chart_data['TEMPO'])
#st.line_chart(chart_data.set_index('TEMPO'))

contagem_por_mes = df_local.groupby(df_local['TEMPO'].dt.to_period("M")).size().reset_index(name='contagem')
contagem_por_mes['TEMPO'] = contagem_por_mes['TEMPO'].dt.to_timestamp()
st.line_chart(contagem_por_mes.set_index('TEMPO'))
