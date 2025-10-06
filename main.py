import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame, QStyle
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize
from gui.cadastro_cliente import CadastroCliente
from gui.cadastro_servico import CadastroServico
from utils.db_utils import criar_tabelas

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Sistema de Cadastro')
        self.setGeometry(100, 100, 500, 350)
        # Define the app/window icon (uses existing icon.png at project root)
        self.setWindowIcon(QIcon('icon.png'))
        # Garante que as tabelas existam ao iniciar a aplicação
        try:
            criar_tabelas()
        except Exception:
            pass
        self.setStyleSheet("""
            QMainWindow { background: #0b0f14; }
            QWidget { color: #e5e7eb; }
            QPushButton {
                background: #111827;
                color: #e5e7eb;
                border: 1px solid #1f2937;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: 600;
                margin: 8px 0;
            }
            QPushButton:hover { background: #1f2937; }
            QLabel#titulo {
                font-size: 28px;
                font-weight: bold;
                color: #93c5fd;
                margin-bottom: 18px;
            }
            QLabel#subtitulo { font-size: 16px; color: #9ca3af; margin-bottom: 18px; }
            QFrame { background: #0f172a; border: 1px solid #1f2937; border-radius: 12px; padding: 24px; }
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(18)

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

        # Helper to obtain themed icons with safe fallbacks
        def themed_icon(primary_name: str, fallback_standard: QStyle.StandardPixmap) -> QIcon:
            icon = QIcon.fromTheme(primary_name)
            if icon.isNull():
                icon = self.style().standardIcon(fallback_standard)
            return icon

        btn_painel = QPushButton('Painel de Controle')
        btn_painel.setIcon(themed_icon('view-dashboard', QStyle.SP_DesktopIcon))
        btn_painel.setIconSize(QSize(24, 24))
        btn_painel.clicked.connect(self.abrir_painel_controle)
        frame_layout.addWidget(btn_painel)

        btn_cliente = QPushButton('Cadastro de Cliente')
        # Try common user/contacts icons from themes, fallback to a generic file icon
        ic_cliente = QIcon.fromTheme('user-group')
        if ic_cliente.isNull():
            ic_cliente = QIcon.fromTheme('contact-new')
        if ic_cliente.isNull():
            ic_cliente = self.style().standardIcon(QStyle.SP_FileIcon)
        btn_cliente.setIcon(ic_cliente)
        btn_cliente.setIconSize(QSize(24, 24))
        btn_cliente.clicked.connect(self.abrir_cadastro_cliente)
        frame_layout.addWidget(btn_cliente)

        btn_servico = QPushButton('Cadastro de Serviço')
        btn_servico.setIcon(themed_icon('document-new', QStyle.SP_DialogOpenButton))
        btn_servico.setIconSize(QSize(24, 24))
        btn_servico.clicked.connect(self.abrir_cadastro_servico)
        frame_layout.addWidget(btn_servico)

        btn_gerenciar = QPushButton('Gerenciar Serviços')
        btn_gerenciar.setIcon(themed_icon('view-list', QStyle.SP_FileDialogListView))
        btn_gerenciar.setIconSize(QSize(24, 24))
        btn_gerenciar.clicked.connect(self.abrir_gerenciamento_servicos)
        frame_layout.addWidget(btn_gerenciar)

        main_layout.addWidget(frame)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def abrir_painel_controle(self):
        from gui.painel_controle import PainelControle
        self.painel_controle = PainelControle()
        self.painel_controle.show()

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
