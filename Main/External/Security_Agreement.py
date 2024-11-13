import sys
import os
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QTabBar, QScrollArea, QStackedWidget
from PySide6.QtCore import Qt, QPoint, QPropertyAnimation
from PySide6.QtGui import QFont, QIcon
from Path_Dict import ico_path,Agreement_Path_User,Agreement_Path_Open_Source

# 定义版本号和工具包版本
MAIN_VERSION = "V6.0.5"
TOOLKIT_VERSION = "V6.0.5"

class AgreementWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.user_agreed = False  # 用于存储用户是否同意协议
        self.offset = None  # 用于存储窗口的偏移量

    def initUI(self):
        self.setWindowTitle('用户协议')
        self.setFixedSize(720, 700)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet("background-color: white;")
        self.setWindowIcon(QIcon(str(ico_path)))  # 确保路径是字符串类型

        # 创建 QTabBar 和 QStackedWidget
        self.tab_bar = QTabBar(self)
        self.tab_bar.setShape(QTabBar.Shape.RoundedNorth)
        self.tab_bar.setTabsClosable(False)
        self.tab_bar.currentChanged.connect(self.animate_tab_switch)

        # 自定义 QTabBar 样式
        self.tab_bar.setStyleSheet("""
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
            QTabBar::tab:selected:hover {
                background: #218838;
                color: white;
            }
            QTabBar::tab:!selected {
                background: #d0d0d0;
                color: #555;
            }
        """)

        self.stacked_widget = QStackedWidget(self)
        self.load_agreements()

        # 同意按钮
        self.agree_button = QPushButton('同意', self)
        self.agree_button.clicked.connect(self.agree)
        self.agree_button.setEnabled(True)
        self.agree_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                font-size: 16px;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
        """)

        # 不同意按钮
        self.disagree_button = QPushButton('不同意', self)
        self.disagree_button.clicked.connect(self.disagree)
        self.disagree_button.setEnabled(True)
        self.disagree_button.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                font-size: 16px;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
            QPushButton:pressed {
                background-color: #bd2130;
            }
        """)

        # 布局
        vbox = QVBoxLayout()
        vbox.addWidget(self.tab_bar)
        vbox.addWidget(self.stacked_widget)
        vbox.addWidget(self.agree_button)
        vbox.addWidget(self.disagree_button)
        self.setLayout(vbox)

    def load_agreements(self):
        """
        加载多个协议文件并显示在选项卡中
        """
        agreement_files = [Agreement_Path_Open_Source,Agreement_Path_User]  # 协议文件列表
        for idx, file_path in enumerate(agreement_files):
            agreement_text = self.get_agreement_text_from_file(file_path)
            tab_label = f"协议 {idx + 1}"

            # 创建滚动区域
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)

            # 自定义滚动条样式
            scroll_area.setStyleSheet("""
                QScrollBar:vertical {
                    background: #f0f0f0;
                    width: 12px;
                    margin: 0px 0px 0px 0px;
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
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                    background: none;
                }
                QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                    background: #f0f0f0;
                    border-radius: 6px;
                }
                QScrollBar:horizontal {
                    background: #f0f0f0;
                    height: 12px;
                    margin: 0px 0px 0px 0px;
                    border-radius: 6px;
                }
                QScrollBar::handle:horizontal {
                    background: #c4c4c4;
                    min-width: 20px;
                    border-radius: 6px;
                }
                QScrollBar::handle:horizontal:hover {
                    background: #a0a0a0;
                }
                QScrollBar::handle:horizontal:pressed {
                    background: #888888;
                }
                QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                    background: none;
                }
                QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                    background: #f0f0f0;
                    border-radius: 6px;
                }
            """)

            # 创建协议文本标签
            label = QLabel(agreement_text)
            label.setAlignment(Qt.AlignmentFlag.AlignTop)
            label.setWordWrap(True)
            label.setStyleSheet("color: black; font-size: 16px;")
            label.setFont(QFont("Microsoft YaHei", 12))

            # 将标签添加到滚动区域中
            scroll_area.setWidget(label)
            self.stacked_widget.addWidget(scroll_area)
            self.tab_bar.addTab(tab_label)

    def animate_tab_switch(self, index):
        """
        切换选项卡时添加动画效果
        """
        current_widget = self.stacked_widget.currentWidget()
        next_widget = self.stacked_widget.widget(index)

        # 创建动画，从当前位置滑动到新的位置
        animation = QPropertyAnimation(self.stacked_widget, b"geometry")
        animation.setDuration(300)
        animation.setStartValue(self.stacked_widget.geometry())
        animation.setEndValue(self.stacked_widget.geometry().translated(0, 0))
        animation.start()

        # 设置当前显示的页面
        self.stacked_widget.setCurrentIndex(index)

    def get_agreement_text_from_file(self, file_path):
        """
        从指定文件路径读取协议文本
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            return f"协议文件 '{file_path}' 未找到。请确保文件存在。"

    def agree(self):
        try:
            with open('C:/N1/Logs/Agreed', 'w+') as f:
                pass
            self.user_agreed = True
            QMessageBox.information(self, '信息', '您已同意协议')
            self.close()
        except Exception as e:
            QMessageBox.critical(self, '错误', f'无法创建协议文件：{e}')
            sys.exit(1)

    def disagree(self):
        QMessageBox.warning(self, '不同意', '您不同意协议，程序将退出')
        self.user_agreed = False
        self.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.offset is not None and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)

def main():
    app = QApplication(sys.argv)
    ex = AgreementWindow()
    ex.show()
    app.exec()

def agreement_check():
    if os.path.exists('C:/N1/Logs/Agreed'):
        pass
    else:
        main()

agreement_check()
