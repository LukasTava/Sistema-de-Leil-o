import tkinter as tk
from database import adicionar_usuario, listar_usuarios, atualizar_usuario, excluir_usuario

class UsuarioInterface:
    def __init__(self, root, atualizar_comboboxes_callback, log_evento):
        self.root = root
        self.atualizar_comboboxes_callback = atualizar_comboboxes_callback
        self.log_evento = log_evento

        self.frame_usuario = tk.LabelFrame(self.root, text="Cadastro de Usuário")
        self.frame_usuario.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

        tk.Label(self.frame_usuario, text="Nome:").grid(row=0, column=0, sticky="e")
        self.entry_usuario_nome = tk.Entry(self.frame_usuario, width=30)
        self.entry_usuario_nome.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(self.frame_usuario, text="CPF:").grid(row=1, column=0, sticky="e")
        self.entry_usuario_cpf = tk.Entry(self.frame_usuario, width=30)
        self.entry_usuario_cpf.grid(row=1, column=1, padx=5, pady=2)

        self.btn_cadastrar_usuario = tk.Button(self.frame_usuario, text="Cadastrar Usuário", command=self.cadastrar_usuario)
        self.btn_cadastrar_usuario.grid(row=2, columnspan=2, pady=5)

        self.frame_usuarios_registrados = tk.LabelFrame(self.root, text="Usuários Registrados")
        self.frame_usuarios_registrados.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")

        self.listbox_usuarios = tk.Listbox(self.frame_usuarios_registrados, selectmode=tk.SINGLE, width=50, height=5)
        self.listbox_usuarios.grid(row=0, column=0, padx=10, pady=5)

        self.btn_excluir_usuario = tk.Button(self.frame_usuarios_registrados, text="Excluir Usuário", command=self.excluir_usuario)
        self.btn_excluir_usuario.grid(row=1, column=0, pady=5)

    def cadastrar_usuario(self):
        nome = self.entry_usuario_nome.get()
        cpf = self.entry_usuario_cpf.get()

        if not nome or not cpf:
            self.log_evento("Aviso: Por favor, preencha todos os campos.")
            return

        adicionar_usuario(nome, cpf)
        self.atualizar_comboboxes_callback()
        self.entry_usuario_nome.delete(0, tk.END)
        self.entry_usuario_cpf.delete(0, tk.END)
        self.atualizar_lista_usuarios()
        self.log_evento(f"Sucesso: Usuário '{nome}' cadastrado com sucesso!")

    def editar_usuarios(self):
        self.editar_usuarios_janela = tk.Toplevel(self.root)
        self.editar_usuarios_janela.title("Editar Usuários")

        usuarios = listar_usuarios()
        self.listbox_editar_usuarios = tk.Listbox(self.editar_usuarios_janela, selectmode=tk.SINGLE, width=50)
        self.listbox_editar_usuarios.pack(padx=10, pady=10)

        for usuario in usuarios:
            self.listbox_editar_usuarios.insert(tk.END, f"{usuario.id} - {usuario.nome} - {usuario.cpf}")

        self.btn_editar_usuario = tk.Button(self.editar_usuarios_janela, text="Editar Usuário", command=self.abrir_editar_usuario)
        self.btn_editar_usuario.pack(pady=5)

    def abrir_editar_usuario(self):
        try:
            selected_usuario = self.listbox_editar_usuarios.get(self.listbox_editar_usuarios.curselection())
            usuario_id, nome, cpf = selected_usuario.split(' - ')
            usuario_id = int(usuario_id)

            self.editar_usuario_janela = tk.Toplevel(self.editar_usuarios_janela)
            self.editar_usuario_janela.title("Editar Usuário")

            tk.Label(self.editar_usuario_janela, text="Nome:").grid(row=0, column=0, sticky="e")
            self.entry_editar_usuario_nome = tk.Entry(self.editar_usuario_janela)
            self.entry_editar_usuario_nome.grid(row=0, column=1, padx=5, pady=2)
            self.entry_editar_usuario_nome.insert(0, nome)

            tk.Label(self.editar_usuario_janela, text="CPF:").grid(row=1, column=0, sticky="e")
            self.entry_editar_usuario_cpf = tk.Entry(self.editar_usuario_janela)
            self.entry_editar_usuario_cpf.grid(row=1, column=1, padx=5, pady=2)
            self.entry_editar_usuario_cpf.insert(0, cpf)

            self.btn_salvar_usuario = tk.Button(self.editar_usuario_janela, text="Salvar", command=lambda: self.salvar_editar_usuario(usuario_id))
            self.btn_salvar_usuario.grid(row=2, columnspan=2, pady=5)

        except (ValueError, IndexError):
            self.log_evento("Aviso: Selecione um usuário válido para editar.")

    def salvar_editar_usuario(self, usuario_id):
        nome = self.entry_editar_usuario_nome.get()
        cpf = self.entry_editar_usuario_cpf.get()

        if not nome or not cpf:
            self.log_evento("Aviso: Por favor, preencha todos os campos.")
            return

        atualizar_usuario(usuario_id, nome, cpf)
        self.log_evento(f"Sucesso: Usuário '{nome}' atualizado com sucesso!")
        self.editar_usuario_janela.destroy()
        self.editar_usuarios_janela.destroy()
        self.editar_usuarios()
        self.atualizar_comboboxes_callback()

    def excluir_usuario(self):
        try:
            selected_usuario = self.listbox_usuarios.get(self.listbox_usuarios.curselection())
            usuario_id, nome, cpf = selected_usuario.split(' - ')
            usuario_id = int(usuario_id)
            excluir_usuario(usuario_id)
            self.atualizar_lista_usuarios()
            self.atualizar_comboboxes_callback()
            self.log_evento(f"Sucesso: Usuário '{nome}' excluído com sucesso!")
        except (ValueError, IndexError):
            self.log_evento("Aviso: Selecione um usuário válido para excluir.")

    def atualizar_lista_usuarios(self):
        self.listbox_usuarios.delete(0, tk.END)
        usuarios = listar_usuarios()
        for usuario in usuarios:
            self.listbox_usuarios.insert(tk.END, f"{usuario.id} - {usuario.nome} - {usuario.cpf}")

    def atualizar_comboboxes(self):
        self.atualizar_lista_usuarios()
