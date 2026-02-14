"""
BI & Analytics Pro:
Dashboard avançado com filtros de período e localidade, métricas de ticket médio, 
distribuição geográfica em mapa e exportação de dados para CSV.
"""

import streamlit as st
import pandas as pd
import sqlite3

# 1. Configurações da página (Sempre no topo)
st.set_page_config(page_title="Analytics Pro 2026", layout="wide", page_icon="📊")

# 2. Definição da função de conexão
def get_connection():
    return sqlite3.connect("vendas.db")

# 3. Coordenadas para o Mapa
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

# --- INÍCIO DA LÓGICA ---
conn = get_connection()

st.sidebar.title("Filtros Inteligentes")

# 4. BUSCAR DATAS PARA O FILTRO
df_dates = pd.read_sql("SELECT MIN(data) as min, MAX(data) as max FROM pedidos", conn)
d_min = pd.to_datetime(df_dates['min'][0])
d_max = pd.to_datetime(df_dates['max'][0])

sel_data = st.sidebar.date_input(
    "Selecione o Período", 
    [d_min, d_max], 
    min_value=d_min, 
    max_value=d_max
)

# 5. BUSCAR CIDADES PARA O FILTRO
cidades_db = pd.read_sql("SELECT DISTINCT localidade FROM clientes WHERE localidade IS NOT NULL", conn)
opcoes_cidades = cidades_db['localidade'].tolist()

sel_cidade = st.sidebar.multiselect(
    "Cidades/Estados", 
    options=opcoes_cidades, 
    default=opcoes_cidades
)

# --- PROCESSAMENTO DOS DADOS ---
if len(sel_data) == 2 and len(sel_cidade) > 0:
    dt_inicio, dt_fim = sel_data[0].strftime('%Y-%m-%d'), sel_data[1].strftime('%Y-%m-%d')
    cidades_str = "('" + "','".join(sel_cidade) + "')"
    
    query_master = f"""
    SELECT 
        p.data, p.id as pedido_id, c.nome as cliente, c.localidade,
        pr.nome as produto, pr.preco, ip.quantidade,
        (ip.quantidade * pr.preco) as total_item
    FROM pedidos p
    JOIN clientes c ON p.cliente_id = c.id
    JOIN itens_pedido ip ON p.id = ip.pedido_id
    JOIN produtos pr ON ip.produto_id = pr.id
    WHERE p.data BETWEEN '{dt_inicio}' AND '{dt_fim}'
    AND c.localidade IN {cidades_str}
    """
    df_master = pd.read_sql(query_master, conn)

    # --- LAYOUT PRINCIPAL ---
    st.title("🚀 BI & Analytics de Vendas")
    st.markdown(f"Exibindo dados de **{dt_inicio}** até **{dt_fim}**")

    # KPI Cards
    m1, m2, m3, m4 = st.columns(4)
    faturamento_total = df_master['total_item'].sum()
    m1.metric("Faturamento Total", f"R$ {faturamento_total:,.2f}")
    m2.metric("Qtd Pedidos", df_master['pedido_id'].nunique())
    m3.metric("Ticket Médio", f"R$ {(faturamento_total/df_master['pedido_id'].nunique() if faturamento_total > 0 else 0):,.2f}")
    m4.metric("Qtd Itens Vendidos", df_master['quantidade'].sum())

    st.divider()

    # Gráficos
    col_esq, col_dir = st.columns([2, 1])

    with col_esq:
        st.subheader("📈 Tendência de Faturamento")
        df_vendas_dia = df_master.groupby('data')['total_item'].sum()
        st.area_chart(df_vendas_dia)

    with col_dir:
        st.subheader("📍 Distribuição Geográfica")
        df_mapa = df_master.groupby('localidade').size().reset_index(name='vendas')
        df_mapa['lat'] = df_mapa['localidade'].map(lambda x: coords.get(x, [0,0])[0])
        df_mapa['lon'] = df_mapa['localidade'].map(lambda x: coords.get(x, [0,0])[1])
        st.map(df_mapa)

    st.divider()

    # Rankings
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("🏆 Melhores Clientes")
        top_clientes = df_master.groupby('cliente')['total_item'].sum().sort_values(ascending=False).head(10)
        st.bar_chart(top_clientes, horizontal=True)

    with c2:
        st.subheader("📦 Produtos em Destaque")
        st.dataframe(df_master.groupby('produto')['quantidade'].sum().sort_values(ascending=False), use_container_width=True)

    # Exportar
    csv = df_master.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Baixar Dados (CSV)", csv, f"vendas_{dt_inicio}.csv", "text/csv")

else:
    st.warning("Selecione um período válido e ao menos uma cidade.")

conn.close()