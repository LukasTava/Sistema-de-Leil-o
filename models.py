from datetime import datetime

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
    def __init__(self, produto_id, usuario_id, valor):
        self.produto_id = produto_id
        self.usuario_id = usuario_id
        self.valor = valor
        self.data = datetime.now()
