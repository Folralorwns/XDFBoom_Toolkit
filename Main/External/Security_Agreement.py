import sys
import os
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QMessageBox, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from pathlib import Path

# 假设 ico_path 是图标路径
from Path_Dict import ico_path, Now_Path  # ico_path 假设是 Path 对象

# 定义版本号和工具包版本
MAIN_VERSION = "V6.0.5"
TOOLKIT_VERSION = "V6.0.5"

class AgreementWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.user_agreed = False  # 用户是否同意协议
        self.current_protocol_index = 0  # 当前显示的协议文件索引
        self.protocol_files = []  # 存储协议文件路径

        # 加载协议文件
        self.load_agreement_files()

        self.initUI()  # 初始化界面

    def initUI(self):
        self.setWindowTitle('用户协议')

        # 设置窗口固定大小
        self.setFixedSize(720, 700)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet("background-color: white;")

        # 设置窗口图标
        self.setWindowIcon(QIcon(str(ico_path)))  # 转换为字符串路径

        # 创建布局
        layout = QVBoxLayout()

        # 协议显示区域
        self.protocol_text = QTextEdit(self)
        self.protocol_text.setReadOnly(True)  # 只读模式
        layout.addWidget(self.protocol_text)

        # 协议跳转按钮
        button_layout = QHBoxLayout()
        self.agree_button = QPushButton('同意', self)
        self.agree_button.clicked.connect(self.on_agree)
        button_layout.addWidget(self.agree_button)

        self.next_button = QPushButton('下一协议', self)
        self.next_button.clicked.connect(self.show_next_protocol)
        button_layout.addWidget(self.next_button)

        layout.addLayout(button_layout)

        # 设置布局
        self.setLayout(layout)

        # 显示第一个协议
        self.show_protocol()

    def load_agreement_files(self):
        # 假设协议文件存放在当前目录下的 "agreements" 文件夹
        agreements_dir = Path(Now_Path) / 'agreements'
        if agreements_dir.exists():
            self.protocol_files = list(agreements_dir.glob('*.txt'))  # 读取所有.txt协议文件
        else:
            QMessageBox.warning(self, "警告", "未找到协议文件目录！")
            self.close()

    def show_protocol(self):
        # 显示当前协议内容
        if self.protocol_files:
            with open(self.protocol_files[self.current_protocol_index], 'r', encoding='utf-8') as file:
                protocol_content = file.read()
            self.protocol_text.setPlainText(protocol_content)  # 设置协议内容到 QTextEdit

    def show_next_protocol(self):
        # 切换到下一个协议
        if self.protocol_files:
            self.current_protocol_index += 1
            if self.current_protocol_index < len(self.protocol_files):
                self.show_protocol()
            else:
                QMessageBox.information(self, "提示", "这是最后一份协议。")
                self.close()

    def on_agree(self):
        # 用户同意协议后的动作
        self.user_agreed = True
        QMessageBox.information(self, "提示", "您已同意协议。")
        self.close()

# 启动程序
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AgreementWindow()
    window.show()
    sys.exit(app.exec())
