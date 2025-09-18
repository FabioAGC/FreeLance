from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView, QComboBox, QTextEdit, QPushButton
from PyQt5.QtGui import QColor
from utils.db_utils import listar_servicos, atualizar_status_servico

class GerenciamentoServicos(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Gerenciamento de Serviços')
        self.setGeometry(250, 250, 800, 400)
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Gerenciamento de Serviços'))
        self.busca = QLineEdit()
        self.busca.setPlaceholderText('Buscar')
        self.busca.textChanged.connect(self.filtrar)
        layout.addWidget(self.busca)
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(9)
        self.tabela.setHorizontalHeaderLabels(['Cliente', 'Serviço', 'Custo', 'Desconto', 'Valor Final', 'Status', 'Início', 'Conclusão', 'Descrição'])
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.tabela)
        self.tabela.cellClicked.connect(self.selecionar_linha)
        
        # Seção de descrição abaixo da tabela
        desc_layout = QHBoxLayout()
        desc_layout.addWidget(QLabel('Descrição:'))
        self.descricao_input = QTextEdit()
        self.descricao_input.setMaximumHeight(100)
        self.descricao_input.setPlaceholderText('Digite a descrição do serviço...')
        desc_layout.addWidget(self.descricao_input)
        
        # Botão para salvar descrição
        self.btn_salvar_desc = QPushButton('Salvar Descrição')
        self.btn_salvar_desc.clicked.connect(self.salvar_descricao)
        desc_layout.addWidget(self.btn_salvar_desc)
        
        layout.addLayout(desc_layout)
        self.setLayout(layout)
        self.carregar_tabela()
        self.linha_selecionada = -1
    def selecionar_linha(self, row, column):
        """Seleciona uma linha da tabela e carrega sua descrição no campo de texto"""
        self.linha_selecionada = row
        # Carrega a descrição atual da linha selecionada
        item = self.tabela.item(row, 8)  # Coluna de descrição
        if item:
            self.descricao_input.setPlainText(item.text())
        else:
            self.descricao_input.setPlainText('')
    
    def salvar_descricao(self):
        """Salva a descrição na linha selecionada"""
        if self.linha_selecionada >= 0:
            descricao = self.descricao_input.toPlainText()
            # Atualiza na tabela
            item = QTableWidgetItem(descricao)
            self.tabela.setItem(self.linha_selecionada, 8, item)
            
            # Limpa o campo de descrição após salvar
            self.descricao_input.clear()
            self.linha_selecionada = -1
            
            # Aqui você pode adicionar código para salvar no banco de dados se necessário
            # Por exemplo, atualizar a descrição no banco usando o ID do serviço

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
