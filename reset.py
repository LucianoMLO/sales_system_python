"""
DESCRIÇÃO DO SCRIPT:
Este utilitário é responsável por realizar o 'reset' do ambiente de dados.
Ele verifica a existência do arquivo de banco de dados SQLite ('vendas.db')
e o remove fisicamente do diretório. 

MOTIVO DE USO:
- Limpar dados de teste e começar do zero.
- Corrigir inconsistências estruturais após mudanças no esquema das tabelas.
- Garantir que a próxima execução do sistema crie um banco limpo.
"""

import os

# Verifica se o arquivo existe antes de tentar deletar (evita erros)
if os.path.exists("vendas.db"):
    os.remove("vendas.db")
    print("🧹 Sucesso: O banco de dados 'vendas.db' foi removido!")
else:
    print("ℹ️ Aviso: O arquivo 'vendas.db' não foi encontrado (o banco já está limpo).")