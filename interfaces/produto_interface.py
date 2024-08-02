import tkinter as tk
from database import adicionar_produto, listar_produtos, atualizar_produto, excluir_produto

class ProdutoInterface:
    def __init__(self, root, atualizar_comboboxes_callback, log_evento):
        self.root = root
        self.atualizar_comboboxes_callback = atualizar_comboboxes_callback
        self.log_evento = log_evento

        self.frame_produto = tk.LabelFrame(self.root, text="Cadastro de Produto")
        self.frame_produto.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        tk.Label(self.frame_produto, text="Nome:").grid(row=0, column=0, sticky="e")
        self.entry_produto_nome = tk.Entry(self.frame_produto, width=30)
        self.entry_produto_nome.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(self.frame_produto, text="Preço Inicial:").grid(row=1, column=0, sticky="e")
        self.entry_produto_preco = tk.Entry(self.frame_produto, width=30)
        self.entry_produto_preco.grid(row=1, column=1, padx=5, pady=2)

        self.btn_cadastrar_produto = tk.Button(self.frame_produto, text="Cadastrar Produto", command=self.cadastrar_produto)
        self.btn_cadastrar_produto.grid(row=2, columnspan=2, pady=5)

        self.frame_produtos_registrados = tk.LabelFrame(self.root, text="Produtos Registrados")
        self.frame_produtos_registrados.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        self.listbox_produtos = tk.Listbox(self.frame_produtos_registrados, selectmode=tk.SINGLE, width=50, height=5)
        self.listbox_produtos.grid(row=0, column=0, padx=10, pady=5)

        self.btn_excluir_produto = tk.Button(self.frame_produtos_registrados, text="Excluir Produto", command=self.excluir_produto)
        self.btn_excluir_produto.grid(row=1, column=0, pady=5)

    def cadastrar_produto(self):
        nome = self.entry_produto_nome.get()
        preco_inicial = self.entry_produto_preco.get().replace(',', '.')

        if not nome or not preco_inicial:
            self.log_evento("Aviso: Por favor, preencha todos os campos.")
            return

        try:
            preco_inicial = float(preco_inicial)
        except ValueError:
            self.log_evento("Aviso: Preço inicial deve ser um número.")
            return

        adicionar_produto(nome, preco_inicial)
        self.atualizar_comboboxes_callback()
        self.entry_produto_nome.delete(0, tk.END)
        self.entry_produto_preco.delete(0, tk.END)
        self.atualizar_lista_produtos()
        self.log_evento(f"Sucesso: Produto '{nome}' cadastrado com sucesso!")

    def editar_produtos(self):
        self.editar_produtos_janela = tk.Toplevel(self.root)
        self.editar_produtos_janela.title("Editar Produtos")

        produtos = listar_produtos()
        self.listbox_editar_produtos = tk.Listbox(self.editar_produtos_janela, selectmode=tk.SINGLE, width=50)
        self.listbox_editar_produtos.pack(padx=10, pady=10)

        for produto in produtos:
            self.listbox_editar_produtos.insert(tk.END, f"{produto.id} - {produto.nome} - {produto.preco_inicial:.2f} R$")

        self.btn_editar_produto = tk.Button(self.editar_produtos_janela, text="Editar Produto", command=self.abrir_editar_produto)
        self.btn_editar_produto.pack(pady=5)

    def abrir_editar_produto(self):
        try:
            selected_produto = self.listbox_editar_produtos.get(self.listbox_editar_produtos.curselection())
            produto_id, nome, preco_inicial = selected_produto.split(' - ')
            produto_id = int(produto_id)
            preco_inicial = float(preco_inicial.replace(',', '.'))

            self.editar_produto_janela = tk.Toplevel(self.editar_produtos_janela)
            self.editar_produto_janela.title("Editar Produto")

            tk.Label(self.editar_produto_janela, text="Nome:").grid(row=0, column=0, sticky="e")
            self.entry_editar_produto_nome = tk.Entry(self.editar_produto_janela)
            self.entry_editar_produto_nome.grid(row=0, column=1, padx=5, pady=2)
            self.entry_editar_produto_nome.insert(0, nome)

            tk.Label(self.editar_produto_janela, text="Preço Inicial:").grid(row=1, column=0, sticky="e")
            self.entry_editar_produto_preco = tk.Entry(self.editar_produto_janela)
            self.entry_editar_produto_preco.grid(row=1, column=1, padx=5, pady=2)
            self.entry_editar_produto_preco.insert(0, preco_inicial)

            self.btn_salvar_produto = tk.Button(self.editar_produto_janela, text="Salvar", command=lambda: self.salvar_editar_produto(produto_id))
            self.btn_salvar_produto.grid(row=2, columnspan=2, pady=5)

        except (ValueError, IndexError):
            self.log_evento("Aviso: Selecione um produto válido para editar.")

    def salvar_editar_produto(self, produto_id):
        nome = self.entry_editar_produto_nome.get()
        preco_inicial = self.entry_editar_produto_preco.get().replace(',', '.')

        if not nome or not preco_inicial:
            self.log_evento("Aviso: Por favor, preencha todos os campos.")
            return

        try:
            preco_inicial = float(preco_inicial)
        except ValueError:
            self.log_evento("Aviso: Preço inicial deve ser um número.")
            return

        atualizar_produto(produto_id, nome, preco_inicial)
        self.log_evento(f"Sucesso: Produto '{nome}' atualizado com sucesso!")
        self.editar_produto_janela.destroy()
        self.editar_produtos_janela.destroy()
        self.editar_produtos()
        self.atualizar_comboboxes_callback()

    def excluir_produto(self):
        try:
            selected_produto = self.listbox_produtos.get(self.listbox_produtos.curselection())
            produto_id, nome, preco_inicial = selected_produto.split(' - ')
            produto_id = int(produto_id)
            excluir_produto(produto_id)
            self.atualizar_lista_produtos()
            self.atualizar_comboboxes_callback()
            self.log_evento(f"Sucesso: Produto '{nome}' excluído com sucesso!")
        except (ValueError, IndexError):
            self.log_evento("Aviso: Selecione um produto válido para excluir.")

    def atualizar_lista_produtos(self):
        self.listbox_produtos.delete(0, tk.END)
        produtos = listar_produtos()
        for produto in produtos:
            valor_formatado = "{:,.2f}".format(produto.preco_inicial).replace('.', ',')
            self.listbox_produtos.insert(tk.END, f"{produto.id} - {produto.nome} - {valor_formatado} R$")

    def atualizar_comboboxes(self):
        self.atualizar_lista_produtos()
