"""
DESCRIÇÃO:
Script 'cadastro2.py' - Gestão de Vendas com Carrinho e PDF.
Organizado em 5 etapas: Configuração, Suporte PDF, Cadastro Cliente, 
Cadastro Produto e Ponto de Venda (PDV).

LÓGICA DE BANCO:
Segue estritamente a estrutura relacional de 4 tabelas.
Garante que um pedido só seja finalizado se houver itens no carrinho.
"""

import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import base64

# ==========================================
# 1. CONFIGURAÇÕES E CONEXÃO
# ==========================================
st.set_page_config(page_title="Sistema de Gestão v2", page_icon="🛍️", layout="wide")

def conectar_db():
    return sqlite3.connect("vendas.db")

# Inicializa o carrinho se não existir
if 'carrinho' not in st.session_state:
    st.session_state.carrinho = []

# ==========================================
# 2. FUNÇÕES DE SUPORTE (PDF E RECIBO)
# ==========================================
def gerar_recibo_pdf(id_pedido, nome_cliente, itens, total):
    pdf = FPDF()
    pdf.add_page()
    
    # Cabeçalho
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "RECIBO DE VENDA", ln=True, align="C")
    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 10, f"Pedido ID: {id_pedido} | Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align="C")
    pdf.ln(10)
    
    # Dados do Cliente
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"Cliente: {nome_cliente}", ln=True)
    pdf.ln(5)
    
    # Tabela de Itens
    pdf.set_fill_color(200, 200, 200)
    pdf.cell(80, 10, "Produto", 1, 0, "C", True)
    pdf.cell(30, 10, "Qtd", 1, 0, "C", True)
    pdf.cell(40, 10, "Unitário", 1, 0, "C", True)
    pdf.cell(40, 10, "Subtotal", 1, 1, "C", True)
    
    pdf.set_font("Arial", "", 12)
    for item in itens:
        pdf.cell(80, 10, item['nome'], 1)
        pdf.cell(30, 10, str(item['qtd']), 1, 0, "C")
        pdf.cell(40, 10, f"R$ {item['preco']:.2f}", 1, 0, "C")
        pdf.cell(40, 10, f"R$ {item['subtotal']:.2f}", 1, 1, "C")
    
    # Total
    pdf.ln(5)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"TOTAL: R$ {total:.2f}", ln=True, align="R")
    
    return pdf.output(dest="S").encode("latin-1")

def link_download_pdf(bin_file, filename):
    b64 = base64.b64encode(bin_file).decode()
    return f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">📥 Baixar Recibo PDF</a>'

# ==========================================
# 3. INTERFACE - CADASTRO DE CLIENTES
# ==========================================
st.title("🛍️ Sistema de Gestão e Vendas v2.0")

aba1, aba2, aba3 = st.tabs(["👤 Novo Cliente", "📦 Novo Produto", "🛒 Registrar Venda"])

with aba1:
    st.header("Cadastro de Cliente")
    with st.form("form_cliente", clear_on_submit=True):
        nome = st.text_input("Nome do Cliente")
        email = st.text_input("E-mail")
        if st.form_submit_button("Cadastrar Cliente"):
            if nome and email:
                try:
                    conn = conectar_db()
                    conn.execute("INSERT INTO clientes (nome, email) VALUES (?, ?)", (nome, email))
                    conn.commit()
                    st.success(f"Cliente {nome} cadastrado!")
                except sqlite3.IntegrityError:
                    st.error("Erro: Este e-mail já está cadastrado.")
                finally: conn.close()

# ==========================================
# 4. INTERFACE - CADASTRO DE PRODUTOS
# ==========================================
with aba2:
    st.header("Cadastro de Produto")
    with st.form("form_produto", clear_on_submit=True):
        nome_p = st.text_input("Nome do Produto")
        preco_p = st.number_input("Preço", min_value=0.0, step=0.01)
        if st.form_submit_button("Cadastrar Produto"):
            if nome_p and preco_p > 0:
                conn = conectar_db()
                conn.execute("INSERT INTO produtos (nome, preco) VALUES (?, ?)", (nome_p, preco_p))
                conn.commit()
                conn.close()
                st.success(f"Produto {nome_p} cadastrado!")

# ==========================================
# 5. INTERFACE - VENDA E CARRINHO
# ==========================================
with aba3:
    st.header("Ponto de Venda (Multi-Itens)")
    
    conn = conectar_db()
    clientes = pd.read_sql("SELECT * FROM clientes", conn)
    produtos = pd.read_sql("SELECT * FROM produtos", conn)
    conn.close()

    if clientes.empty or produtos.empty:
        st.warning("Cadastre clientes e produtos antes de vender.")
    else:
        col_input, col_carrinho = st.columns([1, 1.5])

        with col_input:
            sel_cliente = st.selectbox("Cliente", options=clientes['id'].tolist(), 
                                       format_func=lambda x: clientes[clientes['id']==x]['nome'].values[0])
            
            sel_produto = st.selectbox("Produto", options=produtos['id'].tolist(),
                                       format_func=lambda x: f"{produtos[produtos['id']==x]['nome'].values[0]} - R$ {produtos[produtos['id']==x]['preco'].values[0]:.2f}")
            
            qtd = st.number_input("Quantidade", min_value=1, step=1)
            
            if st.button("➕ Adicionar Item"):
                p_info = produtos[produtos['id'] == sel_produto].iloc[0]
                st.session_state.carrinho.append({
                    "id": sel_produto, "nome": p_info['nome'], 
                    "preco": p_info['preco'], "qtd": qtd, "subtotal": p_info['preco'] * qtd
                })
                st.rerun()

        with col_carrinho:
            if st.session_state.carrinho:
                df_c = pd.DataFrame(st.session_state.carrinho)
                st.table(df_c[['nome', 'qtd', 'subtotal']])
                total = df_c['subtotal'].sum()
                st.subheader(f"Total: R$ {total:.2f}")

                if st.button("🗑️ Limpar"):
                    st.session_state.carrinho = []; st.rerun()

                if st.button("🏁 Finalizar Venda e Gerar Recibo"):
                    conn = conectar_db()
                    cursor = conn.cursor()
                    
                    # Salva Pedido
                    cursor.execute("INSERT INTO pedidos (cliente_id, data) VALUES (?, ?)", 
                                   (sel_cliente, datetime.now().strftime('%Y-%m-%d')))
                    id_pedido = cursor.lastrowid
                    
                    # Salva Itens
                    for item in st.session_state.carrinho:
                        cursor.execute("INSERT INTO itens_pedido (pedido_id, produto_id, quantidade) VALUES (?, ?, ?)",
                                       (id_pedido, item['id'], item['qtd']))
                    
                    conn.commit()
                    
                    # Geração do PDF
                    nome_cliente = clientes[clientes['id'] == sel_cliente]['nome'].values[0]
                    pdf_bytes = gerar_recibo_pdf(id_pedido, nome_cliente, st.session_state.carrinho, total)
                    
                    st.success("Venda salva com sucesso!")
                    st.markdown(link_download_pdf(pdf_bytes, f"recibo_pedido_{id_pedido}.pdf"), unsafe_allow_html=True)
                    
                    st.session_state.carrinho = []
                    conn.close()
            else:
                st.info("Carrinho vazio.")