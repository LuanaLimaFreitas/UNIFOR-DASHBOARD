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

df['TEMPO'] = pd.to_datetime(df['TEMPO'])
df['UF'] = df['LOCAL'].str.extract(r'([A-Z]{2})')
df['reclamacoes'] = 1


#### STREAMLIT ###
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

st.warning("""
    O número de reclamações respondidas que é informado acima, corresponde 
    a todas as reclamações que estão com o STATUS de ‘Respondida’, ‘Resolvido’ 
    e ‘Não resolvido’.
""")

# Divider
st.divider()

st.markdown('##### Frequência de cada tipo de STATUS')
status_unicos = df_local['STATUS'].value_counts()
colunas = st.columns(len(status_unicos))
for i, (valor, contagem) in enumerate(status_unicos.items()):
    coluna = colunas[i]
    percentagem = contagem / reclamacoes_local * 100
    coluna.metric(valor, contagem, "{:.1f}%".format(percentagem))  

st.markdown('##### Frequência de reclamações por estado')
contagem_uf = df_local['UF'].value_counts()
contagem_uf = contagem_uf.sort_values(ascending=True)
st.bar_chart(contagem_uf)

st.markdown('##### Série temporal do número de reclamações')
tab1, tab2, tab3 = st.tabs(["DIA", "MES", "ANO"])

with tab1:
    contagem_por_dia = df_local['TEMPO'].dt.date.value_counts().sort_index()
    chart_data = pd.DataFrame({'TEMPO': contagem_por_dia.index, 'contagem': contagem_por_dia.values})
    chart_data['TEMPO'] = pd.to_datetime(chart_data['TEMPO'])
    st.line_chart(chart_data.set_index('TEMPO'))

with tab2:
    contagem_por_mes = df_local.groupby(df_local['TEMPO'].dt.to_period("M")).size().reset_index(name='contagem')
    contagem_por_mes['TEMPO'] = contagem_por_mes['TEMPO'].dt.to_timestamp()
    st.line_chart(contagem_por_mes.set_index('TEMPO'))

with tab3:
    contagem_por_ano = df_local.groupby(df_local['TEMPO'].dt.to_period("Y")).size().reset_index(name='contagem')
    contagem_por_ano['TEMPO'] = contagem_por_ano['TEMPO'].dt.to_timestamp()
    st.line_chart(contagem_por_ano.set_index('TEMPO'))



