from fpdf import FPDF
from database import listar_produtos, listar_usuarios, listar_lances
from datetime import datetime

def gerar_relatorio_pdf():
    produtos = listar_produtos()
    usuarios = listar_usuarios()
    lances = listar_lances()

    vencedores = {}
    for lance in lances:
        produto_id = lance.produto_id
        valor = lance.valor
        if produto_id not in vencedores or vencedores[produto_id].valor < valor:
            vencedores[produto_id] = lance

    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, 'Relatório de Lances e Vencedores', 0, 1, 'C')
            self.ln(10)

        def chapter_title(self, title):
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, title, 0, 1, 'L')
            self.ln(5)

        def chapter_body(self, body):
            self.set_font('Arial', '', 10)  # Ajustando o tamanho da fonte para 10
            self.multi_cell(0, 10, body)
            self.ln()

        def add_chapter(self, title, body):
            self.add_page()
            self.chapter_title(title)
            self.chapter_body(body)

        def add_table(self, header, data):
            self.set_font('Arial', 'B', 10)  # Ajustando o tamanho da fonte para 10
            col_widths = [70, 50, 30, 50]  # Ajuste das larguras das colunas
            for col_width, col in zip(col_widths, header):
                self.cell(col_width, 10, col, 1, align='C')  # Centralizando o texto nas células
            self.ln()
            self.set_font('Arial', '', 10)  # Ajustando o tamanho da fonte para 10
            for row in data:
                for col_width, item in zip(col_widths, row):
                    self.cell(col_width, 10, str(item), 1, align='C')  # Centralizando o texto nas células
                self.ln()

    pdf = PDF()
    pdf.set_left_margin(5)  # Aumentando as margens da tabela
    pdf.set_right_margin(5)  # Aumentando as margens da tabela

    for produto in produtos:
        produto_id = produto.id
        produto_info = f"Nome: {produto.nome}\nPreço Inicial: {produto.preco_inicial:.2f} R$\n"
        
        lances_produto = [lance for lance in lances if lance.produto_id == produto_id]
        lances_data = []
        for lance in lances_produto:
            usuario = next((u for u in usuarios if u.id == lance.usuario_id), None)
            data_obj = datetime.strptime(lance.data, "%Y-%m-%d %H:%M:%S")
            data_formatada = data_obj.strftime("%Y-%m-%d %H:%M:%S")
            valor_formatado = "{:,.2f}".format(lance.valor).replace('.', ',')
            lances_data.append([usuario.nome, usuario.cpf, f"{valor_formatado} R$", data_formatada])

        vencedor = vencedores.get(produto_id, None)
        if vencedor:
            usuario_vencedor = next((u for u in usuarios if u.id == vencedor.usuario_id), None)
            valor_formatado = "{:,.2f}".format(vencedor.valor).replace('.', ',')
            vencedor_info = f"Vencedor: {usuario_vencedor.nome} ({usuario_vencedor.cpf}) com {valor_formatado} R$\n"
        else:
            vencedor_info = "Nenhum vencedor\n"

        pdf.add_chapter(f"Produto {produto_id}", produto_info)
        pdf.add_table(["Nome", "CPF", "Lance", "Data"], lances_data)
        pdf.chapter_body(vencedor_info)

    pdf_file_path = "relatorio_leilao.pdf"
    pdf.output(pdf_file_path)
    return pdf_file_path
