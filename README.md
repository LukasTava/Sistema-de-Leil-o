# Sistema de Leilão

Este projeto é um sistema de leilão desenvolvido em Python usando a biblioteca Tkinter para a interface gráfica e SQLite para o banco de dados. O sistema permite gerenciar produtos, usuários e lances, além de gerar relatórios em PDF dos leilões realizados.

## Funcionalidades

- **Cadastro de Produtos:** Permite cadastrar novos produtos que serão leiloados, incluindo nome e preço inicial.
- **Cadastro de Usuários:** Permite cadastrar novos usuários que poderão participar dos leilões.
- **Gestão de Lances:** Permite registrar novos lances para os produtos, visualizar os detalhes dos produtos, e excluir lances.
- **Relatório em PDF:** Gera um relatório detalhado dos lances e vencedores dos leilões em formato PDF.

## Estrutura do Projeto

- `main.py`: Script principal para iniciar a aplicação.
- `database.py`: Módulo para gerenciamento do banco de dados SQLite.
- `report.py`: Módulo para geração de relatórios em PDF usando a biblioteca FPDF.
- `interfaces/`: Diretório contendo os módulos da interface gráfica:
  - `interface.py`: Interface principal do sistema.
  - `produto_interface.py`: Interface para gestão de produtos.
  - `usuario_interface.py`: Interface para gestão de usuários.
  - `lance_interface.py`: Interface para gestão de lances.
  - `log_interface.py`: Interface para exibição de logs de eventos.
- `models.py`: Módulo contendo as classes de modelo (`Produto`, `Usuario`, `Lance`).

## Pré-requisitos

Certifique-se de ter o Python instalado em sua máquina. Este projeto foi desenvolvido usando Python 3.

## Bibliotecas Necessárias

- `tkinter`: Biblioteca padrão para interfaces gráficas em Python.
- `fpdf`: Biblioteca para geração de arquivos PDF.

## Instalando Dependências

1. Clone o repositório para a sua máquina local:
   ```sh
   git clone https://github.com/LukasTava/SistemaLeilao.git
   cd SistemaLeilao
2. Crie e ative um ambiente virtual:

   ```sh
   python -m venv venv
   source venv/bin/activate   # No Windows, use: venv\Scripts\activate
3. Instale as dependências necessárias:

```sh
pip install fpdf

## Como Iniciar o Programa

1. Certifique-se de que o ambiente virtual esteja ativado.
2. Execute o script principal para iniciar a aplicação:

```sh
python main.py


## Utilização

**Editar Produtos:** Clique no botão "Editar Produtos" para adicionar, editar ou excluir produtos do leilão.

**Editar Usuários:** Clique no botão "Editar Usuários" para adicionar, editar ou excluir usuários.

**Registrar Lances:** Selecione um produto na lista de itens do leilão e registre novos lances.

**Gerar Relatório:** Clique no botão "Gerar Relatório em PDF" para gerar um relatório detalhado dos leilões realizados.
