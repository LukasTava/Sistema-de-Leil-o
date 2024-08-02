import tkinter as tk
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from interfaces.produto_interface import ProdutoInterface
from interfaces.usuario_interface import UsuarioInterface
from interfaces.lance_interface import LanceInterface
from database import listar_produtos, obter_vencedor_por_produto
from report import gerar_relatorio_pdf

class Interface:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Leilão")

        self.produto_interface = ProdutoInterface(self.root, self.atualizar_comboboxes, self.log_evento)
        self.usuario_interface = UsuarioInterface(self.root, self.atualizar_comboboxes, self.log_evento)
        self.lance_interface = LanceInterface(self.root)

        self._setup_widgets()
        self.atualizar_comboboxes()
        self.atualizar_lista_itens()

    def _setup_widgets(self):
        # Frame de Itens do Leilão
        self.frame_itens = tk.LabelFrame(self.root, text="Itens do Leilão")
        self.frame_itens.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

        self.listbox_itens = tk.Listbox(self.frame_itens, selectmode=tk.SINGLE, width=80, height=10)
        self.listbox_itens.grid(row=0, column=0, padx=10, pady=5)
        self.listbox_itens.bind('<<ListboxSelect>>', self.exibir_detalhes_item)

        # Botões
        self.btn_editar_produtos = tk.Button(self.root, text="Editar Produtos", command=self.produto_interface.editar_produtos)
        self.btn_editar_produtos.grid(row=3, column=0, pady=5)

        self.btn_editar_usuarios = tk.Button(self.root, text="Editar Usuários", command=self.usuario_interface.editar_usuarios)
        self.btn_editar_usuarios.grid(row=3, column=1, pady=5)

        self.btn_gerar_relatorio = tk.Button(self.root, text="Gerar Relatório em PDF", command=self.gerar_relatorio)
        self.btn_gerar_relatorio.grid(row=4, column=0, columnspan=2, pady=5)

        # Frame de Log de Eventos
        self.frame_log = tk.LabelFrame(self.root, text="Log de Eventos")
        self.frame_log.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

        self.text_log = tk.Text(self.frame_log, width=100, height=10, state=tk.DISABLED)
        self.text_log.grid(row=0, column=0, padx=10, pady=5)

    def atualizar_comboboxes(self):
        self.produto_interface.atualizar_comboboxes()
        self.usuario_interface.atualizar_comboboxes()
        self.lance_interface.atualizar_comboboxes()
        self.atualizar_lista_itens()

    def atualizar_lista_itens(self):
        self.listbox_itens.delete(0, tk.END)
        produtos = listar_produtos()
        for produto in produtos:
            vencedor = obter_vencedor_por_produto(produto.id)
            valor_vencedor = vencedor['valor'] if vencedor else produto.preco_inicial
            self.listbox_itens.insert(tk.END, f"{produto.id} - {produto.nome} - {valor_vencedor:.2f} R$")

    def exibir_detalhes_item(self, event):
        try:
            selecionado = self.listbox_itens.curselection()
            if not selecionado:
                return

            produto_id = int(self.listbox_itens.get(selecionado[0]).split(' - ')[0])
            self.lance_interface.exibir_detalhes_produto(produto_id, self.atualizar_lista_itens)
        except Exception as e:
            self.log_evento(f"Erro ao exibir os detalhes do item: {e}")

    def log_evento(self, mensagem):
        self.text_log.config(state=tk.NORMAL)
        self.text_log.insert(tk.END, mensagem + "\n")
        self.text_log.config(state=tk.DISABLED)
        self.text_log.yview(tk.END)

    def gerar_relatorio(self):
        try:
            pdf_file_path = gerar_relatorio_pdf()
            self.log_evento(f"Sucesso: Relatório gerado em {pdf_file_path}")
        except Exception as e:
            self.log_evento(f"Erro ao gerar relatório: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Interface(root)
    root.mainloop()
