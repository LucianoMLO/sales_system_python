"""
Analytics & AI (Machine Learning):
Painel com integração de modelos preditivos (Scikit-Learn) para tendência de 
faturamento e análise de participação por estado com gráficos Plotly.
"""

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np
from datetime import datetime  # <-- Adicione esta linha se não tiver

st.set_page_config(page_title="Analytics & AI 2026", layout="wide")

# Função para formatar moeda no padrão BR
def format_brl(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def get_connection():
    return sqlite3.connect("vendas.db")

conn = get_connection()

# --- FILTROS LATERAIS ---
st.sidebar.title("Configurações")
df_dates = pd.read_sql("SELECT MIN(data) as min, MAX(data) as max FROM pedidos", conn)
sel_data = st.sidebar.date_input("Período", [pd.to_datetime(df_dates['min'][0]), pd.to_datetime(df_dates['max'][0])])

cidades_db = pd.read_sql("SELECT DISTINCT localidade FROM clientes WHERE localidade IS NOT NULL", conn)
sel_cidade = st.sidebar.multiselect("Localidades", options=cidades_db['localidade'].tolist(), default=cidades_db['localidade'].tolist())

if len(sel_data) == 2 and sel_cidade:
    dt_inicio, dt_fim = sel_data[0].strftime('%Y-%m-%d'), sel_data[1].strftime('%Y-%m-%d')
    cidades_str = "('" + "','".join(sel_cidade) + "')"
    
    query = f"""
    SELECT p.data, c.localidade, pr.nome as produto, (ip.quantidade * pr.preco) as total_item
    FROM pedidos p
    JOIN clientes c ON p.cliente_id = c.id
    JOIN itens_pedido ip ON p.id = ip.pedido_id
    JOIN produtos pr ON ip.produto_id = pr.id
    WHERE p.data BETWEEN '{dt_inicio}' AND '{dt_fim}' AND c.localidade IN {cidades_str}
    """
    df = pd.read_sql(query, conn)
    df['data'] = pd.to_datetime(df['data'])

    # --- MÉTRICAS KPI ---
    st.title("🚀 Inteligência de Vendas & Predição")
    total_faturamento = df['total_item'].sum()
    st.metric("Faturamento Total", format_brl(total_faturamento))

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Faturamento")
        df_fat_diario = df.groupby('data')['total_item'].sum().reset_index()
        # Gráfico de linha sem preenchimento usando Plotly
        fig_linha = px.line(df_fat_diario, x='data', y='total_item', render_mode='svg')
        st.plotly_chart(fig_linha, use_container_width=True)

    with col2:
        st.subheader("🍕 Participação por Estado")
        # Extrair UF da string "Cidade - UF"
        df['uf'] = df['localidade'].str.split(' - ').str[-1]
        fig_pizza = px.pie(df, values='total_item', names='uf', hole=0.3)
        st.plotly_chart(fig_pizza, use_container_width=True)

    st.divider()

    # --- TOP 3 PRODUTOS POR ESTADO ---
    st.subheader("🏆 Top 3 Produtos em Valor por Estado")
    df_uf_prod = df.groupby(['uf', 'produto'])['total_item'].sum().reset_index()
    df_uf_prod = df_uf_prod.sort_values(['uf', 'total_item'], ascending=[True, False])
    top_3_uf = df_uf_prod.groupby('uf').head(3)
    
    # Aplicando formatação brasileira na tabela
    top_3_uf['total_item'] = top_3_uf['total_item'].apply(format_brl)
    st.table(top_3_uf)

    st.divider()

    # --- PREDICÇÃO COM SCIKIT-LEARN ---
    st.subheader("🤖 Previsão de Tendência (Machine Learning)")
    
    # Preparando dados para Regressão Linear
    df_ml = df.groupby('data')['total_item'].sum().reset_index()
    df_ml['data_ordinal'] = df_ml['data'].map(datetime.toordinal)
    
    X = df_ml[['data_ordinal']].values
    y = df_ml['total_item'].values
    
    modelo = LinearRegression()
    modelo.fit(X, y)
    
    # Prever próximos 7 dias
    futuro = np.array([df_ml['data_ordinal'].max() + i for i in range(1, 8)]).reshape(-1, 1)
    previsao = modelo.predict(futuro)
    
    st.write(f"A tendência para a próxima semana é de um faturamento médio diário de: **{format_brl(previsao.mean())}**")
    st.caption("Nota: Este é um modelo de regressão linear simples baseado no histórico filtrado.")

conn.close()