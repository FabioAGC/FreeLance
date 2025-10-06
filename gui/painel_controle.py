from utils.dashboard_utils import get_dashboard_metrics
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QSizePolicy, QGridLayout, QStyle, QSpacerItem
)
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize, QTimer

class PainelControle(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Painel de Controle')
        self.setGeometry(120, 120, 820, 520)
        self.setStyleSheet("""
            QWidget { background: #f4f5f7; }
            QFrame[card="true"] {
                background: #fff;
                border-radius: 14px;
                padding: 18px;
            }
            QLabel[metric="true"] {
                font-size: 30px;
                font-weight: 800;
                color: #1f2937;
            }
            QLabel[desc="true"] {
                font-size: 13px;
                color: #6b7280;
            }
            QLabel[muted="true"] { color: #9ca3af; }
            QFrame#header {
                background: transparent;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(18)
        main_layout.setContentsMargins(24, 24, 24, 24)

        # Header
        header = QFrame()
        header.setObjectName('header')
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        titulo = QLabel('Painel de Controle')
        titulo.setFont(QFont('Arial', 22, QFont.Bold))
        header_layout.addWidget(titulo)
        header_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
        main_layout.addWidget(header)

        # Obter métricas do banco
        metrics = get_dashboard_metrics()

        grid = QGridLayout()
        grid.setSpacing(16)

        # Helper to create metric cards
        def themed_icon(name: str, fallback: QStyle.StandardPixmap) -> QIcon:
            icon = QIcon.fromTheme(name)
            if icon.isNull():
                icon = self.style().standardIcon(fallback)
            return icon

        def make_card(title: str, value: str, theme_icon: str, fallback_icon: QStyle.StandardPixmap, accent: str) -> QFrame:
            card = QFrame()
            card.setProperty('card', True)
            layout = QHBoxLayout(card)
            layout.setSpacing(12)

            icon_lbl = QLabel()
            icon = QIcon.fromTheme(theme_icon)
            if icon.isNull():
                icon = self.style().standardIcon(fallback_icon)
            pm = icon.pixmap(36, 36)
            icon_lbl.setPixmap(pm)
            icon_lbl.setStyleSheet(f'background:{accent};border-radius:10px;padding:8px;')
            layout.addWidget(icon_lbl)

            vbox = QVBoxLayout()
            ldesc = QLabel(title)
            ldesc.setProperty('desc', True)
            vbox.addWidget(ldesc)
            lval = QLabel(value)
            lval.setProperty('metric', True)
            vbox.addWidget(lval)
            layout.addLayout(vbox)
            return card

        card1 = make_card('Total de Clientes', str(metrics['total_clientes']), 'user-group', QStyle.SP_DirIcon, '#dbeafe')
        grid.addWidget(card1, 0, 0)

        card2 = make_card('Serviços Ativos', str(metrics['total_ativos']), 'media-playback-start', QStyle.SP_ArrowForward, '#dcfce7')
        grid.addWidget(card2, 0, 1)

        card3 = make_card('Serviços Pendentes', str(metrics['total_pendentes']), 'task-past-due', QStyle.SP_MessageBoxWarning, '#fef3c7')
        grid.addWidget(card3, 1, 0)

        card4 = make_card('Faturamento do Mês', f"R$ {metrics['faturamento']:.2f}", 'wallet', QStyle.SP_DriveHDIcon, '#ede9fe')
        grid.addWidget(card4, 1, 1)

        main_layout.addLayout(grid)

        # Serviços Recentes - Tabela
        from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
        recent_frame = QFrame()
        recent_frame.setProperty('card', True)
        recent_layout = QVBoxLayout(recent_frame)
        recent_title = QLabel('Serviços Recentes')
        recent_title.setFont(QFont('Arial', 16, QFont.Bold))
        recent_layout.addWidget(recent_title)

        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(['', 'Serviço', 'Cliente', 'Valor', 'Início'])
        table.setRowCount(len(metrics['recentes']))
        table.setStyleSheet('font-size:14px;')
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setStretchLastSection(True)
        table.setShowGrid(False)
        if not metrics['recentes']:
            empty = QLabel('Nenhum serviço recente.')
            empty.setProperty('muted', True)
            empty.setAlignment(Qt.AlignCenter)
            recent_layout.addWidget(empty)
        else:
            for i, s in enumerate(metrics['recentes']):
                icon_item = QTableWidgetItem()
                status = (s[5] or '').lower()
                if status == 'em andamento':
                    icon_item.setIcon(themed_icon('media-playback-start', QStyle.SP_ArrowForward))
                elif status == 'pendente':
                    icon_item.setIcon(themed_icon('task-past-due', QStyle.SP_MessageBoxWarning))
                else:
                    icon_item.setIcon(themed_icon('task-complete', QStyle.SP_DialogApplyButton))
                table.setItem(i, 0, icon_item)
                table.setItem(i, 1, QTableWidgetItem(s[2])) # servico
                table.setItem(i, 2, QTableWidgetItem(s[1])) # cliente
                table.setItem(i, 3, QTableWidgetItem(f"R$ {float(s[3]) - float(s[4]):.2f}"))
                table.setItem(i, 4, QTableWidgetItem(s[6] if s[6] else ''))
            recent_layout.addWidget(table)
        main_layout.addWidget(recent_frame)

        # Atualização automática e responsiva
        self._timer = QTimer(self)
        self._timer.setInterval(3000)  # 3s
        self._timer.timeout.connect(self._rebuild)
        self._timer.start()

    def _rebuild(self):
        # Reconstrói o painel para refletir dados atuais
        self.layout().setParent(None)
        self.__init__(self.parent())
