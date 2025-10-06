from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView, QComboBox, QTextEdit, QPushButton, QFrame, QSizePolicy, QStyle
)
from PyQt5.QtGui import QColor, QFont, QIcon
from PyQt5.QtCore import Qt
from utils.db_utils import listar_servicos, atualizar_status_servico

class GerenciamentoServicos(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Gerenciamento de Serviços')
        self.setGeometry(250, 250, 1000, 560)
        self.setWindowIcon(QIcon('icon.png'))
        self.setStyleSheet("""
            QWidget { background: #0b0f14; color: #e5e7eb; }
            QFrame[card="true"] { background: #0f172a; border: 1px solid #1f2937; border-radius: 12px; padding: 16px; }
            QLabel[title="true"] { font-size: 20px; font-weight: 800; color: #f9fafb; }
            QLabel[muted="true"] { color: #9ca3af; }
            QLineEdit, QTextEdit { background: #111827; color: #e5e7eb; border: 1px solid #1f2937; border-radius: 8px; padding: 10px; }
            QComboBox { background: #111827; color: #e5e7eb; border: 1px solid #1f2937; border-radius: 8px; padding: 8px; }
            QComboBox QAbstractItemView { background: #111827; color: #e5e7eb; selection-background-color: #374151; selection-color: #e5e7eb; }
            QPushButton { background: #111827; color: #e5e7eb; border: 1px solid #1f2937; border-radius: 8px; padding: 10px 16px; font-weight: 600; }
            QPushButton:hover { background: #1f2937; }
            QTableWidget { background: #0f172a; color: #e5e7eb; border: 1px solid #1f2937; border-radius: 8px; font-size: 14px; gridline-color: #1f2937; }
            QHeaderView::section { background-color: #111827; color: #e5e7eb; padding: 8px; border: none; border-right: 1px solid #1f2937; }
            QTableWidget::item:selected { background: #374151; }
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(18)

        header = QFrame()
        header.setProperty('card', True)
        h = QHBoxLayout(header)
        title = QLabel('Gerenciamento de Serviços')
        title.setProperty('title', True)
        h.addWidget(title)
        h.addStretch(1)
        main_layout.addWidget(header)

        search_card = QFrame()
        search_card.setProperty('card', True)
        search_row = QHBoxLayout(search_card)
        self.busca = QLineEdit()
        self.busca.setPlaceholderText('Buscar serviço, cliente...')
        self.busca.textChanged.connect(self.filtrar)
        search_row.addWidget(self.busca)
        main_layout.addWidget(search_card)

        self.tabela = QTableWidget()
        self.tabela.setColumnCount(9)
        self.tabela.setHorizontalHeaderLabels([
            'Cliente', 'Serviço', 'Custo', 'Desconto', 'Valor Final', 'Status', 'Início', 'Conclusão', 'Descrição'
        ])
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabela.setAlternatingRowColors(False)
        main_layout.addWidget(self.tabela)
        self.tabela.cellClicked.connect(self.selecionar_linha)

        # Remove campo descrição fixo, agora será modal
        self.setLayout(main_layout)
        self.carregar_tabela()
        self.linha_selecionada = -1
    def selecionar_linha(self, row, column):
        """Abre um QDialog para editar a descrição do serviço selecionado"""
        self.linha_selecionada = row
        item = self.tabela.item(row, 8)
        descricao_atual = item.text() if item else ''
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton
        dialog = QDialog(self)
        dialog.setWindowTitle('Editar Descrição do Serviço')
        dialog.setMinimumWidth(400)
        layout = QVBoxLayout(dialog)
        txt = QTextEdit()
        txt.setPlainText(descricao_atual)
        txt.setPlaceholderText('Digite a descrição do serviço...')
        layout.addWidget(txt)
        btn_salvar = QPushButton('Salvar')
        layout.addWidget(btn_salvar)
        def salvar():
            nova_desc = txt.toPlainText()
            self.tabela.setItem(row, 8, QTableWidgetItem(nova_desc))
            dialog.accept()
            # Aqui você pode adicionar código para salvar no banco de dados se necessário
        btn_salvar.clicked.connect(salvar)
        dialog.exec_()
    
    # Removido método salvar_descricao, agora é feito no modal

    def carregar_tabela(self):
        servicos = listar_servicos()
        self.tabela.setRowCount(len(servicos))
        for i, s in enumerate(servicos):
            self.tabela.setItem(i, 0, QTableWidgetItem(s[1])) # cliente
            self.tabela.setItem(i, 1, QTableWidgetItem(s[2])) # servico
            custo = max(0.0, float(s[3])) if s[3] else 0.0
            desconto = max(0.0, float(s[4])) if s[4] else 0.0
            self.tabela.setItem(i, 2, QTableWidgetItem(f'{custo:.2f}')) # custo
            self.tabela.setItem(i, 3, QTableWidgetItem(f'{desconto:.2f}')) # desconto
            valor_final = max(0.0, custo - desconto)
            self.tabela.setItem(i, 4, QTableWidgetItem(f'{valor_final:.2f}'))
            combo = QComboBox()
            combo.addItems(['Em andamento', 'Concluido'])
            combo.setCurrentText(s[5])
            combo.currentTextChanged.connect(lambda status, row=i: self.atualizar_status(row, status))
            self.tabela.setCellWidget(i, 5, combo)
            self.tabela.setItem(i, 6, QTableWidgetItem(s[6] if s[6] else '')) # início
            self.tabela.setItem(i, 7, QTableWidgetItem(s[7] if s[7] else '')) # conclusão
            self.tabela.setItem(i, 8, QTableWidgetItem(s[8] if len(s) > 8 and s[8] else '')) # descrição

    def atualizar_status(self, row, novo_status):
        # id_servico agora é obtido por busca na base, pois não está mais na tabela
        cliente = self.tabela.item(row, 0).text()
        servico = self.tabela.item(row, 1).text()
        from utils.db_utils import listar_servicos, atualizar_status_servico
        for s in listar_servicos():
            if s[1] == cliente and s[2] == servico:
                id_servico = s[0]
                atualizar_status_servico(id_servico, novo_status)
                break
        # Atualiza data de conclusão na tabela
        if novo_status.lower() == 'concluido':
            from datetime import datetime
            data_conclusao = datetime.now().strftime('%d/%m/%Y')
            self.tabela.setItem(row, 7, QTableWidgetItem(data_conclusao))
        else:
            self.tabela.setItem(row, 7, QTableWidgetItem(''))

    def filtrar(self):
        texto = self.busca.text().lower()
        for i in range(self.tabela.rowCount()):
            mostrar = False
            for j in range(self.tabela.columnCount()):
                item = self.tabela.item(i, j)
                if item and texto in item.text().lower():
                    mostrar = True
            self.tabela.setRowHidden(i, not mostrar)
