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

#### CALCULO DE FORTALEZA ###



#### STREAMLIT###
st.title('ANALISE COVID')

st.write('Esse dashboard é para a turma 4, 5 e 6')
