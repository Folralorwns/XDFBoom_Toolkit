import sys
import os
import datetime
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QTabWidget
from PySide6.QtCore import Qt, QTimer, QPoint
from PySide6.QtGui import QFont, QIcon
from Path_Dict import ico_path

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

        # 当前时间
        nowtime = datetime.datetime.now()
        time_str = f"现在是{nowtime.year}年{nowtime.month}月{nowtime.day}日{nowtime.hour}时{nowtime.minute}分"

        # 协议选项卡
        self.tab_widget = QTabWidget(self)
        self.load_agreements(time_str)

        # 同意按钮
        self.agree_button = QPushButton('同意', self)
        self.agree_button.clicked.connect(self.agree)
        self.agree_button.setEnabled(False)
        self.agree_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                font-size: 16px;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:disabled {
                background-color: #6c757d;
                color: #cccccc;
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
        self.disagree_button.setEnabled(False)
        self.disagree_button.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                font-size: 16px;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:disabled {
                background-color: #6c757d;
                color: #cccccc;
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
        vbox.addWidget(self.tab_widget)
        vbox.addWidget(self.agree_button)
        vbox.addWidget(self.disagree_button)
        self.setLayout(vbox)

        # 倒计时
        self.init_countdown(15)

    def load_agreements(self, time_str):
        """
        加载多个协议文件并显示在选项卡中
        """
        agreement_files = ['AGPLv3.txt', 'XDFBoom软件使用协议.txt']  # 协议文件列表
        for idx, file_path in enumerate(agreement_files):
            agreement_text = time_str + "\n\n" + self.get_agreement_text_from_file(file_path)
            tab_label = f"协议 {idx + 1}"
            label = QLabel(agreement_text)
            label.setAlignment(Qt.AlignmentFlag.AlignTop)
            label.setWordWrap(True)
            label.setStyleSheet("color: black; font-size: 16px;")
            label.setFont(QFont("Microsoft YaHei", 12))
            self.tab_widget.addTab(label, tab_label)

    def init_countdown(self, duration):
        self.countdown = duration
        self.update_countdown()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_countdown)
        self.timer.start(1000)

    def get_agreement_text_from_file(self, file_path):
        """
        从指定文件路径读取协议文本
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            return f"协议文件 '{file_path}' 未找到。请确保文件存在。"

    def update_countdown(self):
        if self.countdown > 0:
            self.agree_button.setText(f"同意 ({self.countdown}秒后可点击)")
            self.disagree_button.setText(f"不同意 ({self.countdown}秒后可点击)")
            self.countdown -= 1
        else:
            self.timer.stop()
            self.agree_button.setEnabled(True)
            self.disagree_button.setEnabled(True)
            self.agree_button.setText("同意")
            self.disagree_button.setText("不同意")

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
