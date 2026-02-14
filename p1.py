"""
Script de Inicialização de Banco de Dados:
Realiza a carga inicial básica no 'vendas.db', inserindo manualmente 
o primeiro registro em cada tabela (cliente, produto e pedido).
"""


import sqlite3

conn = sqlite3.connect("vendas.db")
cur = conn.cursor()

cur.execute("INSERT INTO clientes VALUES (1,'Ana','ana@email.com')")
cur.execute("INSERT INTO produtos VALUES (1,'Notebook',3500)")
cur.execute("INSERT INTO pedidos VALUES (1,1,'2026-01-01')")
cur.execute("INSERT INTO itens_pedido VALUES (1,1,2)")

conn.commit()
