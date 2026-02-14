import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime

# 1. Configurações da Página
st.set_page_config(page_title="Analytics AI & Curva ABC", layout="wide", page_icon="📈")

# Função para formatar moeda no padrão BR
def format_brl(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def get_connection():
    return sqlite3.connect("vendas.db")

# Coordenadas para o Mapa
coords = {
    "São Paulo - SP": [-23.55, -46.63], "Rio de Janeiro - RJ": [-22.90, -43.17],
    "Belo Horizonte - MG": [-19.91, -43.93], "Curitiba - PR": [-25.42, -49.27],
    "Porto Alegre - RS": [-30.03, -51.21], "Salvador - BA": [-12.97, -38.50],
    "Fortaleza - CE": [-3.71, -38.54], "Brasília - DF": [-15.78, -47.92],
    "Manaus - AM": [-3.11, -60.02], "Recife - PE": [-8.05, -34.88],
    "Goiânia - GO": [-16.68, -49.25], "Belém - PA": [-1.45, -48.50],
    "Florianópolis - SC": [-27.59, -48.54], "Vitória - ES": [-20.31, -40.31],
    "Natal - RN": [-5.79, -35.20]
}

conn = get_connection()

# --- SIDEBAR FILTROS ---
st.sidebar.header("⚙️ Configurações de Filtro")
df_dates = pd.read_sql("SELECT MIN(data) as min, MAX(data) as max FROM pedidos", conn)
sel_data = st.sidebar.date_input("Período", [pd.to_datetime(df_dates['min'][0]), pd.to_datetime(df_dates['max'][0])])

cidades_db = pd.read_sql("SELECT DISTINCT localidade FROM clientes WHERE localidade IS NOT NULL", conn)
sel_cidade = st.sidebar.multiselect("Localidades", options=cidades_db['localidade'].tolist(), default=cidades_db['localidade'].tolist())

if len(sel_data) == 2 and sel_cidade:
    dt_inicio, dt_fim = sel_data[0].strftime('%Y-%m-%d'), sel_data[1].strftime('%Y-%m-%d')
    cidades_str = "('" + "','".join(sel_cidade) + "')"
    
    # Query Principal
    query = f"""
    SELECT p.data, p.id as pedido_id, c.nome as cliente, c.localidade, 
           pr.nome as produto, (ip.quantidade * pr.preco) as total_item, ip.quantidade
    FROM pedidos p
    JOIN clientes c ON p.cliente_id = c.id
    JOIN itens_pedido ip ON p.id = ip.pedido_id
    JOIN produtos pr ON ip.produto_id = pr.id
    WHERE p.data BETWEEN '{dt_inicio}' AND '{dt_fim}' AND c.localidade IN {cidades_str}
    """
    df = pd.read_sql(query, conn)
    df['data'] = pd.to_datetime(df['data'])
    df['uf'] = df['localidade'].str.split(' - ').str[-1]

    # --- CABEÇALHO ---
    st.title("🚀 Inteligência Analítica de Vendas")
    st.info(f"📍 Exibindo dados de **{dt_inicio}** até **{dt_fim}**")

    # KPIs
    m1, m2, m3, m4 = st.columns(4)
    total_faturamento = df['total_item'].sum()
    qtd_pedidos = df['pedido_id'].nunique()
    
    m1.metric("Faturamento Total", format_brl(total_faturamento))
    m2.metric("Qtd Pedidos", qtd_pedidos)
    m3.metric("Ticket Médio", format_brl(total_faturamento / qtd_pedidos if qtd_pedidos > 0 else 0))
    m4.metric("Itens Vendidos", int(df['quantidade'].sum()))

    st.divider()

    # --- GRÁFICOS DE LINHA E PIZZA ---
    c_line, c_pie = st.columns([2, 1])
    with c_line:
        st.subheader("📈 Faturamento")
        df_diario = df.groupby('data')['total_item'].sum().reset_index()
        fig_line = px.line(df_diario, x='data', y='total_item', markers=True)
        fig_line.update_traces(line_color='#00d1b2')
        st.plotly_chart(fig_line, use_container_width=True)

    with c_pie:
        st.subheader("🍕 Participação por Estado")
        fig_pizza = px.pie(df, values='total_item', names='uf', hole=0.4)
        st.plotly_chart(fig_pizza, use_container_width=True)

    # --- GEOLOCALIZAÇÃO ---
    st.subheader("📍 Distribuição Geográfica")
    df_mapa = df.groupby('localidade').size().reset_index(name='vendas')
    df_mapa['lat'] = df_mapa['localidade'].map(lambda x: coords.get(x, [0,0])[0])
    df_mapa['lon'] = df_mapa['localidade'].map(lambda x: coords.get(x, [0,0])[1])
    st.map(df_mapa)

    st.divider()

    # --- TOP 3 PRODUTOS NOS 3 MELHORES ESTADOS ---
    st.subheader("🏆 Top 3 Produtos por Valor (Top 3 Estados)")
    top_3_ufs = df.groupby('uf')['total_item'].sum().nlargest(3).index.tolist()
    df_top_ufs = df[df['uf'].isin(top_3_ufs)]
    
    resumo_top_prod = df_top_ufs.groupby(['uf', 'produto'])['total_item'].sum().reset_index()
    resumo_top_prod = resumo_top_prod.sort_values(['uf', 'total_item'], ascending=[True, False])
    resumo_formatado = resumo_top_prod.groupby('uf').head(3)
    resumo_formatado['total_item'] = resumo_formatado['total_item'].apply(format_brl)
    st.table(resumo_formatado)

    # --- MELHORES CLIENTES ---
    st.subheader("👤 Melhores Clientes")
    df_clientes = df.groupby('cliente')['total_item'].sum().sort_values(ascending=False).head(10).reset_index()
    fig_cli = px.bar(df_clientes, x='total_item', y='cliente', orientation='h', text_auto=True)
    fig_cli.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_cli, use_container_width=True)

    # --- CURVA ABC ---
    st.subheader("📊 Produtos em Destaque (Curva ABC)")
    df_abc = df.groupby('produto')['total_item'].sum().sort_values(ascending=False).reset_index()
    df_abc['perc_total'] = (df_abc['total_item'] / total_faturamento) * 100
    df_abc['perc_acumulado'] = df_abc['perc_total'].cumsum()

    def categorizar_abc(perc):
        if perc <= 80: return 'Classe A (Altamente Lucrativo)'
        elif perc <= 95: return 'Classe B (Intermediário)'
        else: return 'Classe C (Baixo Impacto)'

    df_abc['Categoria'] = df_abc['perc_acumulado'].apply(categorizar_abc)
    
    fig_abc = px.bar(df_abc, x='produto', y='total_item', color='Categoria',
                     title="Distribuição ABC por Faturamento",
                     color_discrete_map={'Classe A (Altamente Lucrativo)': '#1f77b4', 
                                         'Classe B (Intermediário)': '#ff7f0e', 
                                         'Classe C (Baixo Impacto)': '#2ca02c'})
    st.plotly_chart(fig_abc, use_container_width=True)

    # --- MACHINE LEARNING (PREDIÇÃO) ---
    st.divider()
    st.subheader("🤖 Tendência para a Próxima Semana")
    
    df_ml = df_diario.copy()
    df_ml['data_ordinal'] = df_ml['data'].map(datetime.toordinal)
    X = df_ml[['data_ordinal']].values
    y = df_ml['total_item'].values
    
    if len(X) > 1:
        modelo = LinearRegression().fit(X, y)
        futuro = np.array([df_ml['data_ordinal'].max() + i for i in range(1, 8)]).reshape(-1, 1)
        previsao = modelo.predict(futuro)
        st.write(f"🔮 Previsão média diária para os próximos 7 dias: **{format_brl(previsao.mean())}**")
    
conn.close()