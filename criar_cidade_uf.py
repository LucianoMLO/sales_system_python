"""
Script de Enriquecimento de Dados Geográficos:
Este script atualiza a tabela 'clientes' no banco de dados 'vendas.db', 
adicionando uma nova coluna chamada 'localidade' e preenchendo-a com 
combinações aleatórias de cidades e estados brasileiros.
"""

import sqlite3
import random

# Lista de cidades e estados para sorteio
locais = [
    ("São Paulo", "SP"), ("Rio de Janeiro", "RJ"), ("Belo Horizonte", "MG"),
    ("Curitiba", "PR"), ("Porto Alegre", "RS"), ("Salvador", "BA"),
    ("Fortaleza", "CE"), ("Brasília", "DF"), ("Manaus", "AM"),
    ("Recife", "PE"), ("Goiânia", "GO"), ("Belém", "PA"),
    ("Florianópolis", "SC"), ("Vitória", "ES"), ("Natal", "RN")
]

def atualizar_clientes():
    conn = sqlite3.connect("vendas.db")
    cur = conn.cursor()

    try:
        # 1. Adicionar a coluna 'localidade' (Cidade/UF)
        # Usamos try/except pois se a coluna já existir, o SQLite daria erro
        print("Adicionando coluna 'localidade'...")
        cur.execute("ALTER TABLE clientes ADD COLUMN localidade TEXT")
    except sqlite3.OperationalError:
        print("A coluna 'localidade' já existe. Atualizando dados...")

    # 2. Buscar todos os IDs de clientes cadastrados
    cur.execute("SELECT id FROM clientes")
    clientes = cur.fetchall()

    # 3. Atualizar cada cliente com um local aleatório
    for cliente in clientes:
        id_cliente = cliente[0]
        cidade, uf = random.choice(locais)
        local_string = f"{cidade} - {uf}"
        
        cur.execute("UPDATE clientes SET localidade = ? WHERE id = ?", (local_string, id_cliente))

    conn.commit()
    print(f"Sucesso! {len(clientes)} clientes atualizados com novas localidades.")
    conn.close()

if __name__ == "__main__":
    atualizar_clientes()