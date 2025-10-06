from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFormLayout, QFrame
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from utils.db_utils import inserir_cliente
import re

class CadastroCliente(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Cadastro de Cliente')
        self.setGeometry(150, 150, 400, 320)
        self.setWindowIcon(QIcon())
        self.setStyleSheet("""
            QWidget {
                background: #f7f7f7;
            }
            QLineEdit {
                padding: 6px;
                border-radius: 4px;
                border: 1px solid #bdbdbd;
                font-size: 14px;
            }
            QLabel {
                font-size: 15px;
                color: #333;
            }
            QPushButton {
                background: #1976d2;
                color: white;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 15px;
            }
            QPushButton:hover {
                background: #1565c0;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(18)

        title = QLabel('Cadastro de Cliente')
        title.setFont(QFont('Arial', 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignRight)
        form_layout.setFormAlignment(Qt.AlignHCenter | Qt.AlignTop)
        form_layout.setSpacing(12)

        self.nome = QLineEdit()
        self.nome.setPlaceholderText('Nome completo')
        form_layout.addRow('Nome:', self.nome)

        self.email = QLineEdit()
        self.email.setPlaceholderText('exemplo@email.com')
        form_layout.addRow('E-mail:', self.email)

        self.telefone = QLineEdit()
        self.telefone.setPlaceholderText('(DDD) 00000-0000')
        form_layout.addRow('Telefone:', self.telefone)

        self.endereco = QLineEdit()
        self.endereco.setPlaceholderText('Endereço completo')
        form_layout.addRow('Endereço:', self.endereco)

        main_layout.addLayout(form_layout)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self.btn_salvar = QPushButton('Salvar')
        self.btn_salvar.setIcon(QIcon())
        self.btn_salvar.clicked.connect(self.salvar_cliente)
        btn_layout.addWidget(self.btn_salvar)
        btn_layout.addStretch()
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

        self.nome.editingFinished.connect(self.email.setFocus)
        self.email.editingFinished.connect(self.telefone.setFocus)
        self.telefone.editingFinished.connect(self.endereco.setFocus)
        self.endereco.editingFinished.connect(lambda: self.btn_salvar.setFocus())

    def salvar_cliente(self):
        nome = self.nome.text().strip()
        email = self.email.text().strip()
        telefone = self.telefone.text().strip()
        endereco = self.endereco.text().strip()

        if not nome:
            QMessageBox.warning(self, 'Erro', 'Preencha o nome do cliente.')
            self.nome.setFocus()
            return
        if email and not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            QMessageBox.warning(self, 'Erro', 'E-mail inválido.')
            self.email.setFocus()
            return
        # Aceita formatos flexíveis: (DDD) NNNNN-NNNN, DDD NNNNNNNNN, DDDNNNNNNNNN, etc.
        if telefone and not re.match(r'^(\(\d{2,3}\)[ ]?\d{4,5}-?\d{4}|\d{2,3}[ ]?\d{4,5}-?\d{4})$', telefone):
            QMessageBox.warning(self, 'Erro', 'Telefone inválido. Use DDD e número, com ou sem espaços/traço.')
            self.telefone.setFocus()
            return
        inserir_cliente(nome, email, telefone, endereco)
        QMessageBox.information(self, 'Sucesso', 'Cliente cadastrado com sucesso!')
        self.close()
