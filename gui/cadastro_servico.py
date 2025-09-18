from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QCompleter, QComboBox
from utils.db_utils import inserir_servico, listar_clientes
import re

class CadastroServico(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Cadastro de Serviço')
        self.setGeometry(200, 200, 350, 300)
        layout = QVBoxLayout()
        clientes = [c[1] for c in listar_clientes()]
        self.cliente = QLineEdit()
        self.cliente.setPlaceholderText('Buscar cliente pelo nome')
        completer = QCompleter(clientes)
        completer.setCaseSensitivity(False)
        self.cliente.setCompleter(completer)
        self.servico = QLineEdit()
        self.servico.setPlaceholderText('Nome do serviço')
        self.custo = QLineEdit()
        self.custo.setPlaceholderText('Valor do serviço')
        self.desconto = QLineEdit()
        self.desconto.setPlaceholderText('Desconto aplicado')
        self.status = QComboBox()
        self.status.addItems(['Em andamento', 'Concluido'])
        self.valor_final = QLineEdit()
        self.valor_final.setReadOnly(True)
        self.valor_final.setPlaceholderText('Valor final')
        layout.addWidget(QLabel('Cliente'))
        layout.addWidget(self.cliente)
        layout.addWidget(QLabel('Serviço'))
        layout.addWidget(self.servico)
        layout.addWidget(QLabel('Custo do Serviço'))
        layout.addWidget(self.custo)
        layout.addWidget(QLabel('Desconto'))
        layout.addWidget(self.desconto)
        layout.addWidget(QLabel('Valor Final'))
        layout.addWidget(self.valor_final)
        layout.addWidget(QLabel('Status'))
        layout.addWidget(self.status)
        btn_salvar = QPushButton('Salvar')
        btn_salvar.clicked.connect(self.salvar_servico)
        layout.addWidget(btn_salvar)
        self.setLayout(layout)

        # Enter para próximo campo
        self.cliente.returnPressed.connect(self.servico.setFocus)
        self.servico.returnPressed.connect(self.custo.setFocus)
        self.custo.returnPressed.connect(self.desconto.setFocus)
        self.desconto.returnPressed.connect(lambda: self.status.setFocus())
        self.status.currentIndexChanged.connect(lambda: btn_salvar.setFocus())

        # Validação monetária e cálculo automático
        self.custo.textChanged.connect(self.atualizar_valor_final)
        self.desconto.textChanged.connect(self.atualizar_valor_final)

    def atualizar_valor_final(self):
        try:
            custo = float(self.custo.text().replace(',', '.')) if self.custo.text() else 0.0
        except ValueError:
            custo = 0.0
        try:
            desconto = float(self.desconto.text().replace(',', '.')) if self.desconto.text() else 0.0
        except ValueError:
            desconto = 0.0
        valor_final = max(0.0, custo - desconto)
        self.valor_final.setText(f'{valor_final:.2f}')

    def salvar_servico(self):
        import datetime
        cliente = self.cliente.text().strip()
        servico = self.servico.text().strip()
        custo_txt = self.custo.text().replace(',', '.').strip()
        desconto_txt = self.desconto.text().replace(',', '.').strip()
        if not servico:
            QMessageBox.warning(self, 'Erro', 'Preencha o nome do serviço.')
            return
        if not re.match(r'^\d+(\.\d{1,2})?$', custo_txt):
            QMessageBox.warning(self, 'Erro', 'Custo deve ser um valor monetário válido.')
            return
        if desconto_txt and not re.match(r'^\d+(\.\d{1,2})?$', desconto_txt):
            QMessageBox.warning(self, 'Erro', 'Desconto deve ser um valor monetário válido.')
            return
        custo = float(custo_txt)
        desconto = float(desconto_txt) if desconto_txt else 0.0
        valor_final = custo - desconto
        if valor_final < 0:
            QMessageBox.warning(self, 'Erro', 'O valor final do serviço não pode ser negativo.')
            return
        status = self.status.currentText()
        data_inicio = datetime.datetime.now().strftime('%d/%m/%Y')
        data_conclusao = None
        if status.lower() == 'concluido':
            data_conclusao = data_inicio
        if cliente and servico:
            inserir_servico(cliente, servico, f'{custo:.2f}', f'{desconto:.2f}', status, data_inicio, data_conclusao)
            QMessageBox.information(self, 'Sucesso', f'Serviço cadastrado! Valor final: R$ {valor_final:.2f}\nData de início: {data_inicio}')
            self.close()
        else:
            QMessageBox.warning(self, 'Erro', 'Preencha os campos obrigatórios.')

    def keyPressEvent(self, event):
        from PyQt5.QtCore import Qt
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            widget = self.focusWidget()
            if widget == self.servico:
                self.custo.setFocus()
            elif widget == self.custo:
                self.desconto.setFocus()
            elif widget == self.desconto:
                self.status.setFocus()
            elif widget == self.status:
                for btn in self.findChildren(QPushButton):
                    if btn.text().lower() == 'salvar':
                        btn.setFocus()
                        break
        else:
            super().keyPressEvent(event)
