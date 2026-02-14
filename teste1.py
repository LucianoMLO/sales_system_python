"""
Script de Diagnóstico:
Teste rápido de integridade para verificar se o Streamlit e a conexão 
com o banco de dados 'vendas.db' estão operacionais.
"""

import streamlit as st
import pandas as pd

st.title("Teste de Conexão")
st.write("Se você está vendo isso, o Streamlit está funcionando!")

try:
    import sqlite3
    conn = sqlite3.connect("vendas.db")
    df = pd.read_sql("SELECT * FROM clientes LIMIT 5", conn)
    st.write("Dados do Banco:")
    st.dataframe(df)
    conn.close()
except Exception as e:
    st.error(f"Erro ao acessar o banco: {e}")