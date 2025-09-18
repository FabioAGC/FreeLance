from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout
from gui.cadastro_cliente import CadastroCliente
from gui.cadastro_servico import CadastroServico
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Sistema de Cadastro')
        self.setGeometry(100, 100, 400, 200)
        layout = QVBoxLayout()
        btn_cliente = QPushButton('Cadastro de Cliente')
        btn_servico = QPushButton('Cadastro de Serviço')
        btn_gerenciar = QPushButton('Gerenciar Serviços')
        btn_cliente.clicked.connect(self.abrir_cadastro_cliente)
        btn_servico.clicked.connect(self.abrir_cadastro_servico)
        btn_gerenciar.clicked.connect(self.abrir_gerenciamento_servicos)
        layout.addWidget(btn_cliente)
        layout.addWidget(btn_servico)
        layout.addWidget(btn_gerenciar)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def abrir_cadastro_cliente(self):
        self.cadastro_cliente = CadastroCliente()
        self.cadastro_cliente.show()

    def abrir_cadastro_servico(self):
        self.cadastro_servico = CadastroServico()
        self.cadastro_servico.show()

    def abrir_gerenciamento_servicos(self):
        from gui.gerenciamento_servicos import GerenciamentoServicos
        self.gerenciamento_servicos = GerenciamentoServicos()
        self.gerenciamento_servicos.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
