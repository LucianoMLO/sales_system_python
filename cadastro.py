"""
DESCRIÇÃO DO SCRIPT:
Interface de Gerenciamento Completa desenvolvida com Streamlit para o 'vendas.db'.
Este script atua como um mini-ERP, permitindo a manutenção e operação do sistema
sem necessidade de scripts externos ou comandos SQL manuais.

FUNCIONALIDADES ATUALIZADAS:
- Cadastro de Clientes: Nome, e-mail e localização (Cidade/UF).
- Cadastro de Produtos: Nome do item e preço unitário com validação de valor.
- Registro de Vendas (Módulo Dinâmico): 
    * Seleção de clientes e produtos via menus suspensos (dropdowns).
    * Cálculo automático de integridade (vincula ID do pedido ao ID do item).
    * Registro de data e quantidade.
- Visualização de Dados: Checkbox para consulta rápida dos últimos registros inseridos.

USO:
Execute no terminal: streamlit run cadastro.py
"""

import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="Sistema de Gestão - Cadastro", page_icon="📝", layout="wide")

def conectar_db():
    return sqlite3.connect("vendas.db")

st.title("📝 Central de Cadastros e Vendas")
st.markdown("Gerencie clientes, produtos e registre novas vendas diretamente no banco de dados.")

# Criando abas para organizar a interface
aba_cliente, aba_produto, aba_venda = st.tabs(["👤 Clientes", "📦 Produtos", "💰 Registrar Venda"])

# --- ABA DE CLIENTES ---
with aba_cliente:
    st.header("Novo Cliente")
    with st.form("form_cliente", clear_on_submit=True):
        col1, col2 = st.columns(2)
        nome = col1.text_input("Nome Completo")
        email = col2.text_input("E-mail")
        uf = col1.selectbox("Estado (UF)", ["SP", "RJ", "MG", "RS", "PR", "SC", "BA", "CE", "PE", "DF"])
        cidade = col2.text_input("Cidade")
        
        if st.form_submit_button("Salvar Cliente"):
            if nome and email and cidade:
                conn = conectar_db()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO clientes (nome, email, localidade) VALUES (?, ?, ?)", 
                               (nome, email, f"{cidade}/{uf}"))
                conn.commit()
                conn.close()
                st.success(f"Cliente {nome} cadastrado!")
            else:
                st.warning("Preencha todos os campos.")

# --- ABA DE PRODUTOS ---
with aba_produto:
    st.header("Novo Produto")
    with st.form("form_produto", clear_on_submit=True):
        nome_prod = st.text_input("Nome do Produto")
        preco = st.number_input("Preço Unitário", min_value=0.0, step=0.01)
        
        if st.form_submit_button("Salvar Produto"):
            if nome_prod and preco > 0:
                conn = conectar_db()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO produtos (nome, preco) VALUES (?, ?)", (nome_prod, preco))
                conn.commit()
                conn.close()
                st.success(f"Produto '{nome_prod}' cadastrado!")

# --- ABA DE VENDAS (NOVA FUNCIONALIDADE) ---
with aba_venda:
    st.header("Registrar Novo Pedido")
    
    conn = conectar_db()
    # Carregar dados para os menus suspensos
    df_clientes = pd.read_sql_query("SELECT id, nome FROM clientes ORDER BY nome", conn)
    df_produtos = pd.read_sql_query("SELECT id, nome, preco FROM produtos ORDER BY nome", conn)
    conn.close()

    if df_clientes.empty or df_produtos.empty:
        st.error("É necessário ter clientes e produtos cadastrados para realizar uma venda.")
    else:
        with st.form("form_venda", clear_on_submit=True):
            # Seleção de Cliente
            cliente_selecionado = st.selectbox(
                "Selecione o Cliente", 
                options=df_clientes['id'].tolist(),
                format_func=lambda x: df_clientes[df_clientes['id'] == x]['nome'].iloc[0]
            )
            
            # Seleção de Produto
            produto_id = st.selectbox(
                "Selecione o Produto", 
                options=df_produtos['id'].tolist(),
                format_func=lambda x: f"{df_produtos[df_produtos['id'] == x]['nome'].iloc[0]} - R$ {df_produtos[df_produtos['id'] == x]['preco'].iloc[0]:.2f}"
            )
            
            quantidade = st.number_input("Quantidade", min_value=1, step=1)
            data_venda = st.date_input("Data da Venda", datetime.now())
            
            if st.form_submit_button("Finalizar Venda"):
                try:
                    conn = conectar_db()
                    cursor = conn.cursor()
                    
                    # 1. Inserir na tabela pedidos
                    cursor.execute("INSERT INTO pedidos (cliente_id, data) VALUES (?, ?)", 
                                   (cliente_selecionado, data_venda.strftime('%Y-%m-%d')))
                    pedido_id = cursor.lastrowid
                    
                    # 2. Inserir na tabela itens_pedido
                    cursor.execute("INSERT INTO itens_pedido (pedido_id, produto_id, quantidade) VALUES (?, ?, ?)", 
                                   (pedido_id, produto_id, quantidade))
                    
                    conn.commit()
                    conn.close()
                    st.success(f"✅ Pedido #{pedido_id} registrado com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao processar venda: {e}")

# --- VISUALIZAÇÃO DOS DADOS ---
st.divider()
if st.checkbox("🔍 Visualizar Dados Cadastrados"):
    conn = conectar_db()
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("**Últimos Clientes**")
        st.dataframe(pd.read_sql_query("SELECT * FROM clientes ORDER BY id DESC LIMIT 5", conn))
    with col_b:
        st.write("**Últimos Pedidos**")
        st.dataframe(pd.read_sql_query("""
            SELECT p.id, c.nome as cliente, p.data 
            FROM pedidos p 
            JOIN clientes c ON p.cliente_id = c.id 
            ORDER BY p.id DESC LIMIT 5""", conn))
    conn.close()