from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
from gui.cadastro_cliente import CadastroCliente
from gui.cadastro_servico import CadastroServico
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Sistema de Cadastro')
        self.setGeometry(100, 100, 500, 350)
        self.setWindowIcon(QIcon())
        self.setStyleSheet("""
            QMainWindow {
                background: #f7f7f7;
            }
            QPushButton {
                background: #1976d2;
                color: white;
                border-radius: 6px;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: bold;
                margin: 8px 0;
            }
            QPushButton:hover {
                background: #1565c0;
            }
            QLabel#titulo {
                font-size: 28px;
                font-weight: bold;
                color: #1976d2;
                margin-bottom: 18px;
            }
            QLabel#subtitulo {
                font-size: 16px;
                color: #555;
                margin-bottom: 18px;
            }
            QFrame {
                background: #fff;
                border-radius: 12px;
                padding: 24px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.07);
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(18)

        from PyQt5.QtGui import QPixmap
        icon_label = QLabel()
        pixmap = QPixmap('icon.png')  # Salve o arquivo como 'icon.png' na raiz do projeto
        pixmap = pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon_label.setPixmap(pixmap)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_frame = QFrame()
        icon_layout = QHBoxLayout(icon_frame)
        icon_layout.addStretch()
        icon_layout.addWidget(icon_label)
        icon_layout.addStretch()
        main_layout.addWidget(icon_frame)

        frame = QFrame()
        frame_layout = QVBoxLayout(frame)
        frame_layout.setSpacing(16)

        btn_cliente = QPushButton('Cadastro de Cliente')
        btn_servico = QPushButton('Cadastro de Serviço')
        btn_gerenciar = QPushButton('Gerenciar Serviços')
        btn_cliente.setIcon(QIcon())
        btn_servico.setIcon(QIcon())
        btn_gerenciar.setIcon(QIcon())
        btn_cliente.clicked.connect(self.abrir_cadastro_cliente)
        btn_servico.clicked.connect(self.abrir_cadastro_servico)
        btn_gerenciar.clicked.connect(self.abrir_gerenciamento_servicos)
        frame_layout.addWidget(btn_cliente)
        frame_layout.addWidget(btn_servico)
        frame_layout.addWidget(btn_gerenciar)

        main_layout.addWidget(frame)

        container = QWidget()
        container.setLayout(main_layout)
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
