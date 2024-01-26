import pandas as pd 
import numpy as np 
import plotly.express as px 
import streamlit as st
import datetime

#### CARREGAR O DADO ####
df_hapvida = pd.read_csv('dado/RECLAMEAQUI_HAPVIDA.csv')
df_ibyte = pd.read_csv('dado/RECLAMEAQUI_IBYTE.csv')
df_nagem = pd.read_csv('dado/RECLAMEAQUI_NAGEM.csv')

empresas = ['Hapvida', 'Ibyte', 'Nagem']
df_hapvida['empresa'] = 'Hapvida'
df_ibyte['empresa'] = 'Ibyte'
df_nagem['empresa'] = 'Nagem'
df = pd.concat([df_hapvida, df_ibyte, df_nagem])

## DATETIME ####
df['TEMPO'] = pd.to_datetime(df['TEMPO'])
df['UF'] = df['LOCAL'].str.extract(r'([A-Z]{2})')
df['reclamacoes'] = 1

max_elements = df['CATEGORIA'].str.count('<->').max() + 1
df[['c{}'.format(i+1) for i in range(max_elements)]] = df['CATEGORIA'].str.split('<->', expand=True)

#### STREAMLIT###
with st.sidebar:
    empresa = st.selectbox(
        'EMPRESA',
        df['empresa'].unique())
    uf = st.multiselect(
        'UF', 
        df['UF'].unique())
    status = st.multiselect(
        'STATUS', 
        df['STATUS'].unique())

#### FILTRO ###
df_local1=df[df['empresa'] == empresa]

df_local2=df_local1
if len(uf) > 0:
    df_local2=df_local1[df_local1['UF'].isin(uf)]

if len(status) == 0:
    df_local=df_local2
else:
    df_local=df_local2[df_local2['STATUS'].isin(status)]

#### CABECALHO###
st.markdown('## Dashboard Gerencial')

col1, col2 = st.columns([1, 4])
with col1:
    if empresa=='Hapvida': 
        st.image("images/logo_hapvida.png")
    if empresa=='Ibyte':       
        st.image("images/logo_ibyte.png")
    if empresa=='Nagem':       
        st.image("images/logo_nagem.png")
 

reclamacoes_local=df_local['reclamacoes'].sum()
df_respondidas = df_local[(df_local['STATUS'] == 'Resolvido') | (df_local['STATUS'] == 'Respondida') | (df_local['STATUS'] == 'Não resolvido')]
respondidas_local=df_respondidas['reclamacoes'].sum()
percentagem = respondidas_local / reclamacoes_local * 100
with col2:
    if empresa=='Hapvida': 
        st.markdown('### Hapvida') 
    if empresa=='Ibyte':       
        st.markdown('### Ibyte') 
    if empresa=='Nagem':       
        st.markdown('### Nagem') 

    col21, col22, col23 = st.columns(3)
    col21.metric("Reclamações", reclamacoes_local)
    col22.metric("Respondidas", respondidas_local)
    col23.metric("% Respondidas", "{:.1f}%".format(percentagem))
    
# Divider
st.divider()

def limitar_string(texto, limite=20):
    if len(texto) > limite:
        return texto[:limite] + "..."
    else:
        return texto

opcoes = df_local['c1'].unique()
categorias = st.multiselect('CATEGORIAS:', opcoes)


df_local3=df_local
if len(categorias) > 0:
    df_local3=df_local1[df_local1['c1'].isin(categorias)]

st.markdown('')
st.markdown('')
st.markdown('##### Lista de reclamações:')
#st.caption('A lista tem no máximo os 20 primeiros registros.')
linhas = df_local3.shape[0]
st.caption(f'{linhas} reclamações.')

for index, row in df_local3.head(20).iterrows():
    local = row['LOCAL']
    descricao = row['DESCRICAO']
    categoria = row['c1']
    status = row['STATUS']
    url = row['URL']
    tempo = row['TEMPO']
    titulo = limitar_string(descricao, limite=100)
    with st.expander(titulo):
        st.write(tempo)
        st.caption("LOCAL: " + local)
        st.caption("STATUS: " + status)
        st.caption("CATEGORIA: " + categoria)
        st.write(descricao)
        st.write(url)
        
