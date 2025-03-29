from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QListWidget, QListWidgetItem, QStackedWidget
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from .fastboot_page import FastbootPage
from .network_fix_page import NetworkFixPage
from .about_us import AboutUsWindow
from core.path_manager import get_icon_path
from gui.update_popup import show_update_popup
from gui.agreement_window import AgreementWindow

# 占位页面（后续功能会替换这些）
class PlaceholderPage(QWidget):
    def __init__(self, text):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("XDFBoom Toolkit 平台工具箱")
        self.resize(960, 640)
        self.setWindowIcon(QIcon(get_icon_path("light")))
        self.init_ui()
        show_update_popup(self)

    def init_ui(self):
        # 顶部标题栏
        title = QLabel("XDFBoom Toolkit")
        title.setStyleSheet("font-size: 24px; font-weight: bold; padding: 10px; color: #2c3e50;")
        title.setAlignment(Qt.AlignCenter)
        # 左侧功能导航列表
        self.nav = QListWidget()
        self.nav.addItems(["刷机工具", "网络修复", "关于我们"])
        self.nav.setFixedWidth(150)
        self.nav.currentRowChanged.connect(self.switch_page)

        # 页面容器
        self.pages = QStackedWidget()
        self.pages.addWidget(FastbootPage())
        self.pages.addWidget(NetworkFixPage())
        self.pages.addWidget(AboutUsWindow(embed=True))
        self.pages.addWidget(AgreementWindow(embed=True))

        # 主区域布局
        content_layout = QHBoxLayout()
        content_layout.addWidget(self.nav)
        content_layout.addWidget(self.pages)

        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.addWidget(title)
        main_layout.addLayout(content_layout)

        self.setCentralWidget(central_widget)

    def switch_page(self, index):
        self.pages.setCurrentIndex(index)
