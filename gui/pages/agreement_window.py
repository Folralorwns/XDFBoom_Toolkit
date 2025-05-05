
from PySide6.QtWidgets import QVBoxLayout, QWidget
from qfluentwidgets import (
    FluentWindow, CardWidget, TabInterface, PrimaryPushButton,
    TextEdit, InfoBar, InfoBarPosition
)
from core.path_manager import AGREEMENT_USER, AGREEMENT_OPEN, USER_AGREEMENT_LOG_PATH
import sys


class AgreementWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("用户协议 | User Agreement")
        self.resize(880, 680)
        self.init_ui()

    def init_ui(self):
        self.central = QWidget(self)
        self.setCentralWidget(self.central)

        self.layout = QVBoxLayout(self.central)
        self.layout.setContentsMargins(20, 20, 20, 20)

        self.card = CardWidget("用户协议", "请阅读并同意协议以继续使用")
        self.layout.addWidget(self.card)

        self.card_layout = QVBoxLayout()
        self.card.setLayout(self.card_layout)

        # Tab界面
        self.tab = TabInterface(self)
        self.card_layout.addWidget(self.tab)

        # 加载协议文本
        self.user_agreement_text = self.load_agreement_text(AGREEMENT_USER)
        self.open_agreement_text = self.load_agreement_text(AGREEMENT_OPEN)

        self.user_text = TextEdit()
        self.user_text.setPlainText(self.user_agreement_text)
        self.user_text.setReadOnly(True)

        self.open_text = TextEdit()
        self.open_text.setPlainText(self.open_agreement_text)
        self.open_text.setReadOnly(True)

        self.tab.addTab("用户协议", self.user_text)
        self.tab.addTab("开源协议", self.open_text)

        # 按钮组
        self.agree_btn = PrimaryPushButton("同意", self)
        self.agree_btn.clicked.connect(self.agree)
        self.card_layout.addWidget(self.agree_btn)

        self.disagree_btn = PrimaryPushButton("不同意", self)
        self.disagree_btn.clicked.connect(self.disagree)
        self.card_layout.addWidget(self.disagree_btn)

    def load_agreement_text(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"加载协议失败: {e}"

    def agree(self):
        try:
            USER_AGREEMENT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
            USER_AGREEMENT_LOG_PATH.touch(exist_ok=True)
            InfoBar.success(
                title="感谢您的同意",
                content="已成功保存同意记录",
                parent=self,
                position=InfoBarPosition.TOP,
                duration=3000
            )
            self.close()
        except Exception as e:
            InfoBar.error(
                title="保存失败",
                content=str(e),
                parent=self,
                position=InfoBarPosition.TOP,
                duration=3000
            )
            sys.exit(1)

    def disagree(self):
        InfoBar.error(
            title="不同意协议",
            content="程序即将退出",
            parent=self,
            position=InfoBarPosition.TOP,
            duration=3000
        )
        sys.exit(0)
