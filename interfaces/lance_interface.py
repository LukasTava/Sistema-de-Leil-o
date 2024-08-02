import sys
import os
import tkinter as tk
from tkinter import ttk
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import registrar_lance, listar_lances, excluir_lance, obter_produto_por_id, obter_vencedor_por_produto, listar_usuarios

class LanceInterface:
    def __init__(self, root):
        self.root = root

    def atualizar_comboboxes(self):
        pass  # Placeholder, pode ser removido ou usado se necessário.

    def exibir_detalhes_produto(self, produto_id, atualizar_lista_itens_callback):
        self.produto_id = produto_id
        self.atualizar_lista_itens_callback = atualizar_lista_itens_callback

        produto = obter_produto_por_id(produto_id)
        vencedor = obter_vencedor_por_produto(produto_id)
        if vencedor:
            vencedor_nome = vencedor['usuario_nome']
            valor_vencedor = vencedor['valor']
        else:
            vencedor_nome = "Sem lance"
            valor_vencedor = produto.preco_inicial

        self.detalhes_produto_janela = tk.Toplevel(self.root)
        self.detalhes_produto_janela.title(f"Detalhes do Produto: {produto.nome}")

        detalhes_produto_frame = tk.LabelFrame(self.detalhes_produto_janela, text="Detalhes do Produto")
        detalhes_produto_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.detalhes_label = tk.Label(detalhes_produto_frame, text=f"Nome: {produto.nome}\nAtual Vencedor: {vencedor_nome}\nValor do Lance do Atual Vencedor: {valor_vencedor:.2f} R$")
        self.detalhes_label.grid(row=0, column=0, padx=10, pady=10)

        tk.Label(detalhes_produto_frame, text="Usuário:").grid(row=1, column=0)
        self.combo_novo_usuario = ttk.Combobox(detalhes_produto_frame, state="readonly")
        self.combo_novo_usuario['values'] = ["{} - {}".format(u.id, u.nome) for u in listar_usuarios()]
        self.combo_novo_usuario.grid(row=1, column=1)

        tk.Label(detalhes_produto_frame, text="Novo Lance:").grid(row=2, column=0)
        self.entry_novo_lance_valor = tk.Entry(detalhes_produto_frame)
        self.entry_novo_lance_valor.grid(row=2, column=1)

        self.btn_novo_lance = tk.Button(detalhes_produto_frame, text="Ofertar Lance", command=self.novo_lance)
        self.btn_novo_lance.grid(row=3, columnspan=2, pady=10)

        self.log_text = tk.Text(detalhes_produto_frame, width=50, height=10)
        self.log_text.grid(row=4, columnspan=2, padx=10, pady=10)

        self.listbox_lances = tk.Listbox(detalhes_produto_frame, selectmode=tk.SINGLE, width=50, height=10)
        self.listbox_lances.grid(row=5, columnspan=2, padx=10, pady=5)

        self.btn_excluir_lance = tk.Button(detalhes_produto_frame, text="Excluir Lance", command=self.excluir_lance)
        self.btn_excluir_lance.grid(row=6, columnspan=2, pady=10)

        self.btn_finalizar = tk.Button(detalhes_produto_frame, text="Finalizar", command=self.finalizar)
        self.btn_finalizar.grid(row=7, columnspan=2, pady=10)

        self.atualizar_detalhes_produto()
        self.atualizar_lista_lances()

    def atualizar_detalhes_produto(self):
        produto = obter_produto_por_id(self.produto_id)
        vencedor = obter_vencedor_por_produto(self.produto_id)
        if vencedor:
            vencedor_nome = vencedor['usuario_nome']
            valor_vencedor = vencedor['valor']
        else:
            vencedor_nome = "Sem lance"
            valor_vencedor = produto.preco_inicial

        self.detalhes_label.config(text=f"Nome: {produto.nome}\nAtual Vencedor: {vencedor_nome}\nValor do Lance do Atual Vencedor: {valor_vencedor:.2f} R$")

    def atualizar_lista_lances(self):
        self.listbox_lances.delete(0, tk.END)
        lances = listar_lances()
        for lance in lances:
            if lance.produto_id == self.produto_id:
                usuario = next((u for u in listar_usuarios() if u.id == lance.usuario_id), None)
                if usuario:
                    valor_formatado = "{:,.2f}".format(lance.valor).replace('.', ',')
                    self.listbox_lances.insert(tk.END, f"{lance.id} - {usuario.nome} - {valor_formatado} R$ - {lance.data}")

    def novo_lance(self):
        try:
            usuario = self.combo_novo_usuario.get()
            valor = self.entry_novo_lance_valor.get().replace(',', '.')

            if not usuario or not valor:
                self.log_evento("Aviso: Por favor, preencha todos os campos.")
                return

            try:
                valor = float(valor)
            except ValueError:
                self.log_evento("Aviso: O valor do lance deve ser um número.")
                return

            usuario_id = int(usuario.split()[0])
            produto_info = obter_produto_por_id(self.produto_id)
            vencedor = obter_vencedor_por_produto(self.produto_id)

            valor_atual = vencedor['valor'] if vencedor else produto_info.preco_inicial

            if valor <= valor_atual:
                self.log_evento(f"Aviso: O valor do lance deve ser maior do que o lance atual de {valor_atual:.2f} R$.")
                return

            registrar_lance(self.produto_id, usuario_id, valor)
            self.log_evento(f"Sucesso: Lance de {valor:.2f} R$ registrado!")
            self.entry_novo_lance_valor.delete(0, tk.END)
            self.log_text.insert(tk.END, f"Lance de {valor:.2f} R$ registrado pelo usuário {usuario}!\n")
            self.atualizar_detalhes_produto()
            self.atualizar_lista_lances()
            self.atualizar_lista_itens_callback()
        except Exception as e:
            self.log_evento(f"Erro ao registrar lance: {e}")

    def excluir_lance(self):
        try:
            selected_lance = self.listbox_lances.get(self.listbox_lances.curselection())
            lance_id = int(selected_lance.split(' - ')[0])
            excluir_lance(lance_id)
            self.log_evento(f"Sucesso: Lance excluído!")
            self.atualizar_lista_lances()
            self.atualizar_detalhes_produto()
            self.atualizar_lista_itens_callback()
        except Exception as e:
            self.log_evento(f"Erro ao excluir lance: {e}")

    def finalizar(self):
        self.detalhes_produto_janela.destroy()

    def log_evento(self, mensagem):
        self.log_text.insert(tk.END, mensagem + "\n")
        self.log_text.yview(tk.END)
