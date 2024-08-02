import sqlite3
from datetime import datetime

def conectar():
    conn = sqlite3.connect('leilao.db')
    return conn

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        preco_inicial REAL NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cpf TEXT NOT NULL UNIQUE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS lances (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_id INTEGER,
        usuario_id INTEGER,
        valor REAL,
        data TEXT,
        FOREIGN KEY (produto_id) REFERENCES produtos(id),
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
    )
    ''')

    conn.commit()
    conn.close()

def adicionar_produto(nome, preco_inicial):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO produtos (nome, preco_inicial) VALUES (?, ?)', (nome, preco_inicial))
    conn.commit()
    conn.close()

def listar_produtos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM produtos')
    produtos = cursor.fetchall()
    conn.close()
    return [Produto(*produto) for produto in produtos]

def atualizar_produto(id, nome, preco_inicial):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('UPDATE produtos SET nome = ?, preco_inicial = ? WHERE id = ?', (nome, preco_inicial, id))
    conn.commit()
    conn.close()

def excluir_produto(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM produtos WHERE id = ?', (id,))
    conn.commit()
    conn.close()

def adicionar_usuario(nome, cpf):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO usuarios (nome, cpf) VALUES (?, ?)', (nome, cpf))
    conn.commit()
    conn.close()

def listar_usuarios():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios')
    usuarios = cursor.fetchall()
    conn.close()
    return [Usuario(*usuario) for usuario in usuarios]

def atualizar_usuario(id, nome, cpf):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('UPDATE usuarios SET nome = ?, cpf = ? WHERE id = ?', (nome, cpf, id))
    conn.commit()
    conn.close()

def excluir_usuario(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM usuarios WHERE id = ?', (id,))
    conn.commit()
    conn.close()

def registrar_lance(produto_id, usuario_id, valor):
    conn = conectar()
    cursor = conn.cursor()
    data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('INSERT INTO lances (produto_id, usuario_id, valor, data) VALUES (?, ?, ?, ?)',
                   (produto_id, usuario_id, valor, data))
    conn.commit()
    conn.close()

def listar_lances():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM lances')
    lances = cursor.fetchall()
    conn.close()
    return [Lance(*lance) for lance in lances]

def excluir_lance(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM lances WHERE id = ?', (id,))
    conn.commit()
    conn.close()

def obter_produto_por_id(produto_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM produtos WHERE id = ?', (produto_id,))
    produto = cursor.fetchone()
    conn.close()
    return Produto(*produto)

def obter_vencedor_por_produto(produto_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT usuarios.nome, lances.valor FROM lances JOIN usuarios ON lances.usuario_id = usuarios.id WHERE lances.produto_id = ? ORDER BY lances.valor DESC LIMIT 1', (produto_id,))
    vencedor = cursor.fetchone()
    conn.close()
    if vencedor:
        return {'usuario_nome': vencedor[0], 'valor': vencedor[1]}
    return None

class Produto:
    def __init__(self, id, nome, preco_inicial):
        self.id = id
        self.nome = nome
        self.preco_inicial = preco_inicial

class Usuario:
    def __init__(self, id, nome, cpf):
        self.id = id
        self.nome = nome
        self.cpf = cpf

class Lance:
    def __init__(self, id, produto_id, usuario_id, valor, data):
        self.id = id
        self.produto_id = produto_id
        self.usuario_id = usuario_id
        self.valor = valor
        self.data = data

# Cria as tabelas ao inicializar o módulo
criar_tabelas()
