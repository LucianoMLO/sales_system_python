# 📊 Sistema de Gestão de Vendas (sales_system_python)

Este ecossistema integrado utiliza **Python**, **SQLite 3** e **Streamlit** para oferecer uma solução completa de Business Intelligence (BI) e Gestão Operacional. O projeto transforma dados brutos em insights estratégicos, permitindo o acompanhamento de métricas e o registro de vendas em tempo real.

## 🗄️ Estrutura do Banco de Dados (`vendas.db`)

O banco de dados utiliza uma arquitetura relacional composta por quatro tabelas principais:

* **`clientes`**: Armazena ID, nome, e-mail (chave única) e localidade (Cidade/UF).
* **`produtos`**: Catálogo contendo o nome do item e seu preço unitário.
* **`pedidos`**: Registro do cabeçalho da venda, vinculando a data ao ID do cliente.
* **`itens_pedido`**: Detalhamento técnico que vincula pedido, produto e quantidade.

## 🚀 Guia de Execução (Sequência Lógica)

Para garantir que todos os recursos (mapas e previsões) funcionem, execute os scripts nesta ordem:

1. **`python p1.py`**: Cria a estrutura inicial e insere registros básicos.
2. **`python p2.py`**: Popula o banco com 40 clientes, 18 produtos e 30 pedidos aleatórios.
3. **`python p3.py`**: Expande a base para 100 clientes e gera relatórios de conferência.
4. **`python criar_cidade_uf.py`**: Normaliza e enriquece os dados geográficos para os mapas.
5. **`streamlit run cadastro2.py`**: Abre a interface de vendas e emissão de recibos.
6. **`streamlit run painel_master3.py`**: Abre o dashboard de analytics com IA.

## 📦 Opção de Projeto Simplificado

Para uma versão funcional mínima (Essential Core) sem scripts de teste repetitivos, utilize apenas:

* **`p1.py`**: Setup do banco de dados.
* **`criar_cidade_uf.py`**: Preparação geográfica dos dados.
* **`cadastro2.py`**: Ponto de Venda (PDV) e geração de PDFs.
* **`painel_master3.py`**: Dashboard Master com Curva ABC e IA.
* **`requirements.txt`**: Lista de dependências para instalação.

## ⚠️ Limitações do Sistema

* **Persistência na Nuvem**: No Streamlit Cloud, os dados são efêmeros. Novos cadastros não são salvos permanentemente no GitHub.
* **Concorrência SQLite**: O banco pode travar (`database is locked`) se muitos usuários gravarem dados simultaneamente.
* **Escalabilidade**: Ideal para pequenos volumes; grandes datasets exigem migração para bancos cliente-servidor.

## 💡 Sugestões de Evolução

* **Banco de Dados Cloud**: Migrar para PostgreSQL (Supabase ou Neon) para persistência real de dados.
* **Sistema de Login**: Implementar autenticação para proteger o acesso aos dados sensíveis do dashboard.
* **Controle de Estoque**: Adicionar funcionalidade para baixa automática de produtos no inventário após a venda.
* **API de CEP**: Integrar busca automática de endereço para evitar erros de digitação no cadastro.

## 🛠️ Tecnologias e Links

* **Tecnologias**: Python, Streamlit, Pandas, SQLite3, Scikit-Learn (IA), FPDF (Recibos PDF).
* **Sistema de Vendas/PDV**: [https://sales-system-python-cadastro.streamlit.app/](https://www.google.com/search?q=https://sales-system-python-cadastro.streamlit.app/)
* **Dashboard de Analytics**: [https://sales-system-python-analytics.streamlit.app/](https://www.google.com/search?q=https://sales-system-python-analytics.streamlit.app/)
* **Repositório GitHub**: [https://github.com/seu-usuario/sales_system_python](https://www.google.com/search?q=https://github.com/seu-usuario/sales_system_python)

---

# 📊 Sales Management System (sales_system_python)

This integrated ecosystem uses **Python**, **SQLite 3**, and **Streamlit** to provide a complete Business Intelligence (BI) and Operational Management solution. The project transforms raw data into strategic insights, allowing for metric tracking and real-time sales recording.

## 🗄️ Database Structure (`vendas.db`)

The database uses a relational architecture composed of four main tables:

* **`clientes`**: Stores ID, name, email (unique key), and location (City/State).
* **`produtos`**: Catalog containing item names and unit prices.
* **`pedidos`**: Sales header record, linking the date to the customer ID.
* **`itens_pedido`**: Technical details linking orders, products, and quantities.

## 🚀 Execution Guide (Logical Sequence)

To ensure all features (maps and predictions) work correctly, run the scripts in this order:

1. **`python p1.py`**: Creates the initial structure and inserts basic records.
2. **`python p2.py`**: Populates the DB with 40 customers, 18 products, and 30 random orders.
3. **`python p3.py`**: Expands the base to 100 customers and generates verification reports.
4. **`python criar_cidade_uf.py`**: Normalizes and enriches geographic data for maps.
5. **`streamlit run cadastro2.py`**: Opens the sales interface and receipt issuance.
6. **`streamlit run painel_master3.py`**: Opens the analytics dashboard with AI.

## 📦 Simplified Project Option

For a minimal functional version (Essential Core) without repetitive test scripts, use only:

* **`p1.py`**: Database setup.
* **`criar_cidade_uf.py`**: Geographic data preparation.
* **`cadastro2.py`**: Point of Sale (POS) and PDF generation.
* **`painel_master3.py`**: Master Dashboard with ABC Curve and AI.
* **`requirements.txt`**: List of dependencies for installation.

## ⚠️ System Limitations

* **Cloud Persistence**: On Streamlit Cloud, data is ephemeral. New records are not permanently saved to GitHub.
* **SQLite Concurrency**: The database may lock (`database is locked`) if many users write data simultaneously.
* **Scalability**: Ideal for small volumes; large datasets require migration to client-server databases.

## 💡 Evolution Suggestions

* **Cloud Database**: Migrate to PostgreSQL (Supabase or Neon) for real data persistence.
* **Login System**: Implement authentication to protect access to sensitive dashboard data.
* **Inventory Control**: Add functionality for automatic stock deduction after a sale.
* **ZIP Code API**: Integrate automatic address lookup to prevent typing errors during registration.

## 🛠️ Technologies and Links

* **Technologies**: Python, Streamlit, Pandas, SQLite3, Scikit-Learn (AI), FPDF (PDF Receipts).
* **Sales/POS System**: [https://sales-system-python-cadastro.streamlit.app/](https://www.google.com/search?q=https://sales-system-python-cadastro.streamlit.app/)
* **Analytics Dashboard**: [https://sales-system-python-analytics.streamlit.app/](https://www.google.com/search?q=https://sales-system-python-analytics.streamlit.app/)
* **GitHub Repository**: [https://github.com/your-user/sales_system_python](https://www.google.com/search?q=https://github.com/your-user/sales_system_python)

---

**Gostaria que eu gerasse o arquivo `requirements.txt` com as versões exatas das bibliotecas para garantir que tudo funcione de primeira?**
