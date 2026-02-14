"""
Script de Automação e População de Dados:
Gera e insere em massa 40 clientes, 18 produtos e 30 pedidos aleatórios.
Utiliza 'INSERT OR IGNORE' para evitar erros de duplicidade de IDs.
"""


#%%
import sqlite3
import random
from datetime import datetime, timedelta

conn = sqlite3.connect("vendas.db")
cur = conn.cursor()

print("Gerando 20 novos pedidos...")

# Vamos começar o ID do pedido a partir do 2 (já que o 1 você já criou)
for i in range(2, 22):
    # 1. Gerar uma data aleatória em 2026
    dia = random.randint(1, 45) # espalha pelos primeiros 45 dias do ano
    data_fake = (datetime(2026, 1, 1) + timedelta(days=dia)).strftime('%Y-%m-%d')
    
    # 2. Inserir na tabela 'pedidos' (id_pedido, id_cliente, data)
    # Usamos o cliente ID 1 que você já cadastrou
    cur.execute("INSERT INTO pedidos VALUES (?, ?, ?)", (i, 1, data_fake))
    
    # 3. Inserir na tabela 'itens_pedido' (id_pedido, id_produto, quantidade)
    # Usamos o produto ID 1 (Notebook) e uma quantidade aleatória entre 1 e 3
    qtd = random.randint(1, 3)
    cur.execute("INSERT INTO itens_pedido VALUES (?, ?, ?)", (i, 1, qtd))

conn.commit()
conn.close()

print("Concluído! 20 pedidos e seus itens foram inseridos com sucesso.")

#%%


conn = sqlite3.connect("vendas.db")
cur = conn.cursor()

# --- 1. Inserir 40 Clientes (IDs de 2 a 41) ---
nomes = ["Lucas", "Marcos", "Julia", "Fernanda", "Roberto", "Patrícia", "Gabriel", "Aline"]
sobrenomes = ["Silva", "Costa", "Santos", "Oliveira", "Souza", "Pereira", "Martins"]

for i in range(2, 42):
    nome = f"{random.choice(nomes)} {random.choice(sobrenomes)}"
    email = f"{nome.lower().replace(' ', '_')}@email.com"
    cur.execute("INSERT INTO clientes VALUES (?, ?, ?)", (i, nome, email))

# --- 2. Inserir 18 Produtos (IDs de 2 a 19) ---
categorias = ["Monitor", "Teclado", "Mouse", "Cadeira", "Headset", "Webcam", "Smartphone"]
for i in range(2, 20):
    nome_prod = f"{random.choice(categorias)} Pro {i}"
    preco = round(random.uniform(100, 2800), 2)
    cur.execute("INSERT INTO produtos VALUES (?, ?, ?)", (i, nome_prod, preco))

# --- 3. Inserir 30 Pedidos (IDs de 22 a 51) ---
for i in range(22, 52):
    id_cliente = random.randint(1, 41) # Usa qualquer cliente (os novos ou o primeiro)
    id_produto = random.randint(1, 19) # Usa qualquer produto (os novos ou o primeiro)
    quantidade = random.randint(1, 5)
    
    # Datas espalhadas pelos primeiros 3 meses de 2026
    data_fake = (datetime(2026, 1, 1) + timedelta(days=random.randint(0, 90))).strftime('%Y-%m-%d')
    
    cur.execute("INSERT INTO pedidos VALUES (?, ?, ?)", (i, id_cliente, data_fake))
    cur.execute("INSERT INTO itens_pedido VALUES (?, ?, ?)", (i, id_produto, quantidade))

conn.commit()
conn.close()
print("Sucesso! 40 clientes, 18 produtos e 30 pedidos adicionados.")


#%%
# PARTE NOVA: Testando se os dados estão lá
import sqlite3
conn = sqlite3.connect("vendas.db")
cur = conn.cursor()

cur.execute("SELECT * FROM pedidos LIMIT 50")
print(cur.fetchall())

conn.close()


# %%

conn = sqlite3.connect("vendas.db")
cur = conn.cursor()

# --- 1. Inserir 40 Clientes (IDs de 2 a 41) ---
nomes = ["Lucas", "Marcos", "Julia", "Fernanda", "Roberto", "Patrícia", "Gabriel", "Aline"]
sobrenomes = ["Silva", "Costa", "Santos", "Oliveira", "Souza", "Pereira", "Martins"]

for i in range(2, 42):
    nome = f"{random.choice(nomes)} {random.choice(sobrenomes)}"
    email = f"{nome.lower().replace(' ', '_')}@email.com"
    cur.execute("INSERT INTO clientes VALUES (?, ?, ?)", (i, nome, email))

# --- 2. Inserir 18 Produtos (IDs de 2 a 19) ---
categorias = ["Monitor", "Teclado", "Mouse", "Cadeira", "Headset", "Webcam", "Smartphone"]
for i in range(2, 20):
    nome_prod = f"{random.choice(categorias)} Pro {i}"
    preco = round(random.uniform(100, 2800), 2)
    cur.execute("INSERT INTO produtos VALUES (?, ?, ?)", (i, nome_prod, preco))

# --- 3. Inserir 30 Pedidos (IDs de 22 a 51) ---
for i in range(22, 52):
    id_cliente = random.randint(1, 41) # Usa qualquer cliente (os novos ou o primeiro)
    id_produto = random.randint(1, 19) # Usa qualquer produto (os novos ou o primeiro)
    quantidade = random.randint(1, 5)
    
    # Datas espalhadas pelos primeiros 3 meses de 2026
    data_fake = (datetime(2026, 1, 1) + timedelta(days=random.randint(0, 90))).strftime('%Y-%m-%d')
    
    cur.execute("INSERT INTO pedidos VALUES (?, ?, ?)", (i, id_cliente, data_fake))
    cur.execute("INSERT INTO itens_pedido VALUES (?, ?, ?)", (i, id_produto, quantidade))

conn.commit()
conn.close()
print("Sucesso! 40 clientes, 18 produtos e 30 pedidos adicionados.")


# %%

import sqlite3
import random
from datetime import datetime, timedelta

conn = sqlite3.connect("vendas.db")
cur = conn.cursor()

# --- 1. Inserir 40 Clientes (IDs de 2 a 41) ---
nomes = ["Lucas", "Marcos", "Julia", "Fernanda", "Roberto", "Patrícia", "Gabriel", "Aline"]
sobrenomes = ["Silva", "Costa", "Santos", "Oliveira", "Souza", "Pereira", "Martins"]

for i in range(2, 42):
    nome = f"{random.choice(nomes)} {random.choice(sobrenomes)}"
    email = f"{nome.lower().replace(' ', '_')}@email.com"
    cur.execute("INSERT INTO clientes VALUES (?, ?, ?)", (i, nome, email))

# --- 2. Inserir 18 Produtos (IDs de 2 a 19) ---
categorias = ["Monitor", "Teclado", "Mouse", "Cadeira", "Headset", "Webcam", "Smartphone"]
for i in range(2, 20):
    nome_prod = f"{random.choice(categorias)} Pro {i}"
    preco = round(random.uniform(100, 2800), 2)
    cur.execute("INSERT INTO produtos VALUES (?, ?, ?)", (i, nome_prod, preco))

# --- 3. Inserir 30 Pedidos (IDs de 22 a 51) ---
for i in range(22, 52):
    id_cliente = random.randint(1, 41) # Usa qualquer cliente (os novos ou o primeiro)
    id_produto = random.randint(1, 19) # Usa qualquer produto (os novos ou o primeiro)
    quantidade = random.randint(1, 5)
    
    # Datas espalhadas pelos primeiros 3 meses de 2026
    data_fake = (datetime(2026, 1, 1) + timedelta(days=random.randint(0, 90))).strftime('%Y-%m-%d')
    
    cur.execute("INSERT INTO pedidos VALUES (?, ?, ?)", (i, id_cliente, data_fake))
    cur.execute("INSERT INTO itens_pedido VALUES (?, ?, ?)", (i, id_produto, quantidade))

conn.commit()
conn.close()
print("Sucesso! 40 clientes, 18 produtos e 30 pedidos adicionados.")


# %%
# %%
import sqlite3
import random
from datetime import datetime, timedelta

conn = sqlite3.connect("vendas.db")
cur = conn.cursor()

# 1. Clientes (IDs 2 a 41) - INSERT OR IGNORE evita o erro de duplicidade
nomes = ["Lucas", "Marcos", "Julia", "Fernanda", "Roberto", "Patrícia", "Gabriel", "Aline"]
sobrenomes = ["Silva", "Costa", "Santos", "Oliveira", "Souza", "Pereira", "Martins"]

for i in range(2, 42):
    nome = f"{random.choice(nomes)} {random.choice(sobrenomes)}"
    email = f"{nome.lower().replace(' ', '_')}@email.com"
    # Mudança aqui: OR IGNORE
    cur.execute("INSERT OR IGNORE INTO clientes VALUES (?, ?, ?)", (i, nome, email))

# 2. Produtos (IDs 2 a 19)
categorias = ["Monitor", "Teclado", "Mouse", "Cadeira", "Headset", "Webcam", "Smartphone"]
for i in range(2, 20):
    nome_prod = f"{random.choice(categorias)} Pro {i}"
    preco = round(random.uniform(100, 2800), 2)
    # Mudança aqui: OR IGNORE
    cur.execute("INSERT OR IGNORE INTO produtos VALUES (?, ?, ?)", (i, nome_prod, preco))

# 3. Pedidos (IDs 22 a 51)
for i in range(22, 52):
    id_cliente = random.randint(1, 41)
    id_produto = random.randint(1, 19)
    quantidade = random.randint(1, 5)
    data_fake = (datetime(2026, 1, 1) + timedelta(days=random.randint(0, 90))).strftime('%Y-%m-%d')
    
    # Mudança aqui: OR IGNORE em ambas as tabelas
    cur.execute("INSERT OR IGNORE INTO pedidos VALUES (?, ?, ?)", (i, id_cliente, data_fake))
    cur.execute("INSERT OR IGNORE INTO itens_pedido VALUES (?, ?, ?)", (i, id_produto, quantidade))

conn.commit()
conn.close()
print("Processo concluído! Dados inseridos (novos) ou pulados (se já existentes).")
# %%
# %%
conn = sqlite3.connect("vendas.db")
cur = conn.cursor()

for tabela in ['clientes', 'produtos', 'pedidos', 'itens_pedido']:
    count = cur.execute(f"SELECT COUNT(*) FROM {tabela}").fetchone()[0]
    print(f"Total em {tabela}: {count}")

conn.close()


