import sys
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox,
    QTabBar, QScrollArea, QStackedWidget, QApplication
)
from PySide6.QtCore import Qt, QPropertyAnimation, QRect
from PySide6.QtGui import QFont, QIcon
from core.path_manager import get_icon_path, AGREEMENT_USER, AGREEMENT_OPEN
from config.global_state import USER_AGREEMENT_LOG_PATH


class AgreementWindow(QWidget):
    def __init__(self, embed=False):
        super().__init__()
        self.user_agreed = False
        self.offset = None
        self.embed = embed

        if not self.embed:
            self.setWindowTitle("用户协议")
            self.setFixedSize(720, 700)
            self.setWindowFlags(Qt.FramelessWindowHint)
            self.setWindowIcon(QIcon(str(get_icon_path())))
            self.setStyleSheet("background-color: white;")

        self.init_ui()

    def init_ui(self):
        self.tab_bar = QTabBar(self)
        self.tab_bar.setShape(QTabBar.RoundedNorth)
        self.tab_bar.setTabsClosable(False)
        self.tab_bar.currentChanged.connect(self.animate_tab_switch)
        self.tab_bar.setStyleSheet(self.tab_style())

        self.stacked_widget = QStackedWidget(self)
        self.load_agreements()

        self.agree_button = QPushButton("同意")
        self.agree_button.clicked.connect(self.agree)
        self.agree_button.setStyleSheet(self.button_style("green"))

        self.disagree_button = QPushButton("不同意")
        self.disagree_button.clicked.connect(self.disagree)
        self.disagree_button.setStyleSheet(self.button_style("red"))

        layout = QVBoxLayout()
        layout.addWidget(self.tab_bar)
        layout.addWidget(self.stacked_widget)

        if not self.embed:
            layout.addWidget(self.agree_button)
            layout.addWidget(self.disagree_button)

        self.setLayout(layout)

    def load_agreements(self):
        for idx, file_path in enumerate([AGREEMENT_OPEN, AGREEMENT_USER]):
            content = self.read_text(file_path)

            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_area.setStyleSheet(self.scroll_style())

            label = QLabel(content)
            label.setWordWrap(True)
            label.setAlignment(Qt.AlignTop)
            label.setFont(QFont("Microsoft YaHei", 12))
            label.setStyleSheet("color: black; font-size: 16px;")

            scroll_area.setWidget(label)
            self.stacked_widget.addWidget(scroll_area)
            self.tab_bar.addTab(f"协议 {idx + 1}")

    def animate_tab_switch(self, index):
        animation = QPropertyAnimation(self.stacked_widget, b"geometry")
        animation.setDuration(300)
        animation.setStartValue(self.stacked_widget.geometry())
        animation.setEndValue(self.stacked_widget.geometry().translated(0, 0))
        animation.start()
        self.stacked_widget.setCurrentIndex(index)

    def read_text(self, file_path: Path):
        try:
            return file_path.read_text(encoding='utf-8')
        except FileNotFoundError:
            return f"协议文件未找到：{file_path}"

    def agree(self):
        try:
            USER_AGREEMENT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
            USER_AGREEMENT_LOG_PATH.touch(exist_ok=True)
            self.user_agreed = True
            QMessageBox.information(self, "信息", "您已同意协议")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"无法保存协议状态：{e}")
            sys.exit(1)

    def disagree(self):
        QMessageBox.warning(self, "不同意", "您不同意协议，程序将退出")
        self.user_agreed = False
        self.close()

    def mousePressEvent(self, event):
        if not self.embed and event.button() == Qt.LeftButton:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if not self.embed and self.offset and event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)

    def tab_style(self):
        return """
            QTabBar::tab {
                background: #e0e0e0;
                color: #333;
                padding: 4px;
                margin-right: 8px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-size: 14px;
                min-width: 80px;
            }
            QTabBar::tab:selected {
                background: #28a745;
                color: white;
                font-weight: bold;
            }
            QTabBar::tab:hover {
                background: #34c759;
                color: white;
            }
            QTabBar::tab:!selected {
                background: #d0d0d0;
                color: #555;
            }
        """

    def button_style(self, color: str):
        return f"""
            QPushButton {{
                background-color: {"#28a745" if color == "green" else "#dc3545"};
                color: white;
                font-size: 16px;
                border-radius: 10px;
                padding: 10px;
            }}
            QPushButton:hover {{
                background-color: {"#218838" if color == "green" else "#c82333"};
            }}
            QPushButton:pressed {{
                background-color: {"#1e7e34" if color == "green" else "#bd2130"};
            }}
        """

    def scroll_style(self):
        return """
            QScrollBar:vertical {
                background: #f0f0f0;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #c4c4c4;
                min-height: 20px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical:hover {
                background: #a0a0a0;
            }
            QScrollBar::handle:vertical:pressed {
                background: #888888;
            }
        """


# 外部调用（独立运行）
def main():
    app = QApplication(sys.argv)
    win = AgreementWindow()
    win.show()
    app.exec()


# 主程序前的协议检查（如未同意则阻止进入）
def agreement_check():
    if not USER_AGREEMENT_LOG_PATH.exists():
        main()
