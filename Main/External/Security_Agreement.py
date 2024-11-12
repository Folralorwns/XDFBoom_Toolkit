import sys
import os
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from pathlib import Path

# 假设ico_path是图标路径
from .Path_Dict import ico_path,Now_Path  # ico_path 假设是Path对象

# 定义版本号和工具包版本
MAIN_VERSION = "V6.0.5"
TOOLKIT_VERSION = "V6.0.5"

class AgreementWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.user_agreed = False  # 用户是否同意协议
        self.current_protocol_index = 0  # 当前显示的协议文件索引
        self.protocol_files = []  # 存储协议文件路径

        # 加载协议文件
        self.load_agreement_files()

    def initUI(self):
        self.setWindowTitle('用户协议')
        self.setFixedSize(720, 700)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet("background-color: white;")

        # 设置窗口图标
        self.setWindowIcon(QIcon(str(ico_path)))  # 确保ico_path为字符串类型

        # 布局管理器
        layout = QVBoxLayout()

        # 显示协议内容的文本框
        self.protocol_text_edit = QTextEdit(self)
        self.protocol_text_edit.setReadOnly(True)  # 设置为只读模式
        layout.addWidget(self.protocol_text_edit)

        # 按钮控制显示下一个协议
        self.next_button = QPushButton('下一个协议', self)
        self.next_button.clicked.connect(self.load_next_protocol)
        layout.addWidget(self.next_button)

        self.setLayout(layout)

        # 加载第一个协议文件
        if self.protocol_files:
            self.display_protocol(self.protocol_files[self.current_protocol_index])

    def load_agreement_files(self):
        # 获取当前目录下的所有协议文件（假设协议文件存储在“agreements/”目录下）
        agreements_dir = Now_Path / 'agreements'
        
        # 如果协议文件夹存在，读取所有txt文件
        if agreements_dir.exists() and agreements_dir.is_dir():
            self.protocol_files = sorted(agreements_dir.glob("*.txt"))
        else:
            print("协议文件夹不存在或为空")
    
    def display_protocol(self, protocol_file):
        """加载并显示协议文件内容"""
        if protocol_file.exists():
            with open(protocol_file, 'r', encoding='utf-8') as file:
                content = file.read()
                self.protocol_text_edit.setPlainText(content)
        else:
            self.protocol_text_edit.setPlainText("无法加载协议文件。")

    def load_next_protocol(self):
        """加载下一个协议文件"""
        if self.protocol_files:
            self.current_protocol_index += 1
            if self.current_protocol_index < len(self.protocol_files):
                self.display_protocol(self.protocol_files[self.current_protocol_index])
            else:
                # 如果已加载完所有协议文件，显示完成信息
                self.protocol_text_edit.setPlainText("所有协议文件已显示完毕。")
                self.next_button.setDisabled(True)  # 禁用“下一个协议”按钮

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AgreementWindow()
    window.show()
    sys.exit(app.exec())
