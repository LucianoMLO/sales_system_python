"""
Relatório Geral e Expansão de Inventário:
Consulta e exibe via Pandas o estado atual de todas as tabelas e realiza 
uma nova carga de 60 clientes e 40 produtos com múltiplos itens por pedido.
"""

#%%
## CONSULTANDO OS REGISTROS DO BD
import sqlite3
import pandas as pd

# Conectar ao banco
conn = sqlite3.connect("vendas.db")

# Lista das tabelas que queremos consultar
tabelas = ["clientes", "produtos", "pedidos", "itens_pedido"]

print("--- RELATÓRIO GERAL DO BANCO DE DADOS ---\n")

for tabela in tabelas:
    print(f"TABELA: {tabela.upper()}")
    # Lendo a tabela via Pandas
    try:
        df = pd.read_sql(f"SELECT * FROM {tabela}", conn)
        
        if df.empty:
            print("  (Tabela vazia)")
        else:
            # Mostra as primeiras linhas de forma tabular
            print(df.to_string(index=False))
            
    except Exception as e:
        print(f"  Erro ao ler {tabela}: {e}")
    
    print("-" * 40)

conn.close()

# %%
## CRIANDO RESGISTROS NAS TABELAS

import sqlite3
import random
from datetime import datetime, timedelta

conn = sqlite3.connect("vendas.db")
cur = conn.cursor()

# --- 1. Gerar 60 Clientes (IDs 2 a 61) ---
nomes_base = ["Ricardo", "Beatriz", "Thiago", "Carla", "André", "Vanessa", "Felipe", "Renata", "Diego", "Monica"]
sobrenomes_base = ["Mendes", "Rocha", "Barbosa", "Cardoso", "Teixeira", "Borges", "Nunes"]

print("Inserindo 60 clientes...")
for i in range(2, 62):
    nome = f"{random.choice(nomes_base)} {random.choice(sobrenomes_base)}"
    email = f"{nome.lower().replace(' ', '.')}{i}@email.com" # 'i' garante que o email seja UNIQUE
    cur.execute("INSERT INTO clientes (id, nome, email) VALUES (?, ?, ?)", (i, nome, email))

# --- 2. Gerar 40 Produtos (IDs 2 a 41) ---
itens_loja = ["Placa de Vídeo", "Processador", "Memória RAM", "SSD 1TB", "Fonte 600W", "Gabinete ATX", "Cooler RGB", "Placa-Mãe"]
print("Inserindo 40 produtos...")
for i in range(2, 42):
    nome_prod = f"{random.choice(itens_loja)} Mod-{i*7}"
    preco = round(random.uniform(150.0, 4500.0), 2)
    cur.execute("INSERT INTO produtos (id, nome, preco) VALUES (?, ?, ?)", (i, nome_prod, preco))

# --- 3. Gerar 50 Pedidos (IDs 2 a 51) com 1 a 8 itens cada ---
print("Inserindo 50 pedidos com múltiplos itens...")
for i in range(2, 52):
    # Escolhe um cliente aleatório (entre o ID 1 e o 61)
    id_cliente = random.randint(1, 61)
    
    # Gera data aleatória nos últimos 6 meses
    data_fake = (datetime.now() - timedelta(days=random.randint(0, 180))).strftime('%Y-%m-%d')
    
    # Insere o Pedido
    cur.execute("INSERT INTO pedidos (id, cliente_id, data) VALUES (?, ?, ?)", (i, id_cliente, data_fake))
    
    # Determina quantos itens (produtos diferentes) terá este pedido (1 a 8)
    num_itens = random.randint(1, 8)
    # Sorteia quais produtos (IDs 1 a 41) sem repetir no mesmo pedido
    produtos_selecionados = random.sample(range(1, 42), num_itens)
    
    for id_prod in produtos_selecionados:
        qtd = random.randint(1, 3)
        cur.execute("INSERT INTO itens_pedido (pedido_id, produto_id, quantidade) VALUES (?, ?, ?)", (i, id_prod, qtd))

conn.commit()
conn.close()
print("\nSucesso! Banco de dados populado com 50 novos pedidos e múltiplos itens.")

