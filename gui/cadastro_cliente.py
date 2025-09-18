from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from utils.db_utils import inserir_cliente
import re

class CadastroCliente(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Cadastro de Cliente')
        self.setGeometry(150, 150, 300, 250)
        layout = QVBoxLayout()
        self.nome = QLineEdit()
        self.nome.setPlaceholderText('Nome completo')
        self.email = QLineEdit()
        self.email.setPlaceholderText('exemplo@email.com')
        self.telefone = QLineEdit()
        self.telefone.setPlaceholderText('(DDD) 00000-0000')
        self.endereco = QLineEdit()
        self.endereco.setPlaceholderText('Endereço completo')
        layout.addWidget(QLabel('Nome'))
        layout.addWidget(self.nome)
        layout.addWidget(QLabel('E-mail'))
        layout.addWidget(self.email)
        layout.addWidget(QLabel('Telefone'))
        layout.addWidget(self.telefone)
        layout.addWidget(QLabel('Endereço'))
        layout.addWidget(self.endereco)
        btn_salvar = QPushButton('Salvar')
        btn_salvar.clicked.connect(self.salvar_cliente)
        layout.addWidget(btn_salvar)
        self.setLayout(layout)

        self.nome.editingFinished.connect(self.email.setFocus)
        self.email.editingFinished.connect(self.telefone.setFocus)
        self.telefone.editingFinished.connect(self.endereco.setFocus)
        self.endereco.editingFinished.connect(lambda: btn_salvar.setFocus())

    def salvar_cliente(self):
        nome = self.nome.text().strip()
        email = self.email.text().strip()
        telefone = self.telefone.text().strip()
        endereco = self.endereco.text().strip()
        if not nome:
            QMessageBox.warning(self, 'Erro', 'Preencha o nome do cliente.')
            return
        if email and not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            QMessageBox.warning(self, 'Erro', 'E-mail inválido.')
            return
        if telefone and not re.match(r'^\(\d{2,3}\) \d{5}-\d{4}$', telefone):
            QMessageBox.warning(self, 'Erro', 'Telefone deve estar no formato (ddd) NNNNN-NNNN.')
            return
        inserir_cliente(nome, email, telefone, endereco)
        QMessageBox.information(self, 'Sucesso', 'Cliente cadastrado!')
        self.close()
