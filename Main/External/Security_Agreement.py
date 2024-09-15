import sys
import os
import datetime
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt6.QtCore import Qt, QTimer, QPoint
from PyQt6.QtGui import QFont, QIcon
from .Env_Packages import ico_path

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

        # 设置窗口固定大小
        self.setFixedSize(720, 700)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # 设置窗口背景为白色
        self.setStyleSheet("background-color: white;")

        # 设置窗口图标
        self.setWindowIcon(QIcon(ico_path))  # 替换为你的图标路径

        # 当前时间
        nowtime = datetime.datetime.now()
        minute = f"{nowtime.minute}分"
        hour = f"{nowtime.hour}时"
        time_str = f"现在是{nowtime.year}年{nowtime.month}月{nowtime.day}日{hour}{minute}"

        # 标签文本
        self.label = QLabel(self)
        self.label.setText(time_str + "\n\n" + self.get_agreement_text())
        self.label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.label.setWordWrap(True)
        self.label.setStyleSheet("color: black; font-size: 16px;")
        self.label.setFont(QFont("Microsoft YaHei", 12))

        # 按钮
        self.agree_button = QPushButton('同意', self)
        self.agree_button.clicked.connect(self.agree)
        self.agree_button.setEnabled(False)  # 初始状态为不可点击
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
        
        self.disagree_button = QPushButton('不同意', self)
        self.disagree_button.clicked.connect(self.disagree)
        self.disagree_button.setEnabled(False)  # 初始状态为不可点击
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
        vbox.addWidget(self.label)
        vbox.addWidget(self.agree_button)
        vbox.addWidget(self.disagree_button)
        self.setLayout(vbox)

        # 初始化倒计时
        self.init_countdown(15)

    def init_countdown(self, duration):
        """
        初始化倒计时
        """
        self.countdown = duration
        self.update_countdown()  # 立即更新显示

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_countdown)
        self.timer.start(1000)  # 每秒触发一次

    def get_agreement_text(self):
        return (
            "{:=^50s}\n".format("关于工具包") +
            "制作团队：XDFBoom Team\n" +
            "作者の联系方式：QQ：757009986\t邮箱：folralorwns@gmail.com/757009986@qq.com\n" +
            "作者温暖のB站小窝：Folralorwns\tUID：631757505\n" +
            f"工具包版本：{MAIN_VERSION}\n" +
            "更新时间：2024/10/1\n" +
            "XDFBoom TeamのQQ群：742186535\n" +
            "工具包更新日志：https://blog.xdfboom.com\n" +
            "如果您转载本人的工具包，请务必保留原作者信息\n" +
            "本工具包遵循CC BY-NC-SA 4.0协议\n" +
            "禁止盗取或盗卖本工具包，违者必究！！！\n" +
            "如果您是付费购买的本工具包，那么恭喜您被骗了\n" +
            "{:=^50s}\n".format("") +
            "{:=^50s}\n".format("免责协议") +
            "协议更新日期：2023年5月13日\n" +
            "1.所有已经刷入类原生的学习机都可以恢复到刷入前之状态。\n" +
            "2.刷入类原生后，学习机可以无限制地安装第三方软件...\n" +
            "3.您对学习机进行刷入类原生之操作属于您的自愿行为...\n" +
            "4.本工具包仅供技术学习交流使用，请于24小时内自行删除!\n" +
            "5.“XDFBoom Team”或“XDFBoom团队“及其工具包与 新东方教育科技集团有限公司 没有任何关系！\n" +
            "6.如果您使用本工具包对学习机进行刷入类原生操作，即默认您同意本《免责声明》。\n" +
            "{:=^50s}".format("")
        )

    def update_countdown(self):
        """
        更新倒计时显示
        """
        if self.countdown > 0:
            self.agree_button.setText(f"同意 ({self.countdown}秒后可点击)")
            self.disagree_button.setText(f"不同意 ({self.countdown}秒后可点击)")
            self.countdown -= 1
        else:
            self.timer.stop()
            self.agree_button.setEnabled(True)  # 倒计时结束后启用按钮
            self.disagree_button.setEnabled(True)
            self.agree_button.setText("同意")
            self.disagree_button.setText("不同意")

    def agree(self):
        try:
            agreement_path = os.path.join('C:', 'N1', 'Logs', 'Agreement')
            os.makedirs(os.path.dirname(agreement_path), exist_ok=True)
            with open(agreement_path, 'w+') as f:
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

    return ex.user_agreed  # 返回用户是否同意协议的结果

def agreement_check():
    user_agreed = main()
    if user_agreed:
        print("用户同意了协议。")
    else:
        print("用户不同意协议，程序退出。")
