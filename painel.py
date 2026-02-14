"""
Dashboard Streamlit V1:
Painel básico para visualização de faturamento total, gráfico de evolução 
de vendas e ranking dos Top 10 Clientes em interface web.
"""

## Top 10 Clientes, o Top 5 Produtos e o gráfico de faturamento diário
import streamlit as st
import pandas as pd
import sqlite3

# Configuração da página (Deve ser a primeira linha de comando do Streamlit)
st.set_page_config(page_title="Gestão de Vendas", layout="wide")

def get_connection():
    return sqlite3.connect("vendas.db")

st.title("📊 Painel de Vendas")

try:
    conn = get_connection()

    # 1. Query de Faturamento Diário
    # Note: Usando p.id conforme seu CREATE TABLE pedidos
    query_vendas = """
    SELECT p.data, SUM(ip.quantidade * pr.preco) AS faturamento
    FROM pedidos p
    JOIN itens_pedido ip ON p.id = ip.pedido_id
    JOIN produtos pr ON ip.produto_id = pr.id
    GROUP BY p.data
    ORDER BY p.data
    """
    df_vendas = pd.read_sql(query_vendas, conn)

    # 2. Query de Top Clientes
    query_clientes = """
    SELECT c.nome, SUM(ip.quantidade * pr.preco) AS total_gasto
    FROM clientes c
    JOIN pedidos p ON c.id = p.cliente_id
    JOIN itens_pedido ip ON p.id = ip.pedido_id
    JOIN produtos pr ON ip.produto_id = pr.id
    GROUP BY c.nome
    ORDER BY total_gasto DESC
    LIMIT 10
    """
    df_top_clientes = pd.read_sql(query_clientes, conn)

    # --- EXIBIÇÃO ---

    # Métricas no topo
    if not df_vendas.empty:
        total = df_vendas['faturamento'].sum()
        st.metric("Faturamento Total", f"R$ {total:,.2f}")

        # Gráfico
        st.subheader("📈 Evolução das Vendas")
        df_vendas['data'] = pd.to_datetime(df_vendas['data'])
        st.line_chart(df_vendas.set_index('data'))
    
    # Tabela de Clientes
    st.subheader("🏆 Top 10 Clientes")
    st.dataframe(df_top_clientes, use_container_width=True)

    conn.close()

except Exception as e:
    st.error(f"Ocorreu um erro no processamento: {e}")