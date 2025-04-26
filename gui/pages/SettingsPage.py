
import sys
import os
import webbrowser
from PySide6.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import (
    CardWidget, StrongBodyLabel, SubtitleLabel, PrimaryPushButton, InfoBar, InfoBarPosition,
    setTheme, isDarkTheme, Theme
)
from gui.pages.update_popup import UpdatePopup
from core.path_manager import LOGS_DIR


class SettingsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)

        # 顶部大标题
        self.title_label = StrongBodyLabel("设置中心")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title_label)

        # 主卡片
        self.card = CardWidget("通用设置", "进行应用程序的一些通用设置")
        self.layout.addWidget(self.card)

        self.card_layout = QVBoxLayout()
        self.card.setLayout(self.card_layout)

        # 检查更新按钮
        self.update_btn = PrimaryPushButton("检查更新")
        self.update_btn.clicked.connect(self.check_update)
        self.card_layout.addWidget(self.update_btn)

        # 切换主题按钮
        self.theme_btn = PrimaryPushButton("切换明暗主题")
        self.theme_btn.clicked.connect(self.toggle_theme)
        self.card_layout.addWidget(self.theme_btn)

        # 打开日志目录按钮
        self.open_logs_btn = PrimaryPushButton("打开日志目录")
        self.open_logs_btn.clicked.connect(self.open_logs)
        self.card_layout.addWidget(self.open_logs_btn)

    def check_update(self):
        self.update_popup = UpdatePopup()
        self.update_popup.show()

    def toggle_theme(self):
        if isDarkTheme():
            setTheme(Theme.LIGHT)
            InfoBar.success(
                title="切换成功",
                content="已切换到明亮模式",
                parent=self,
                position=InfoBarPosition.TOP
            )
        else:
            setTheme(Theme.DARK)
            InfoBar.success(
                title="切换成功",
                content="已切换到暗黑模式",
                parent=self,
                position=InfoBarPosition.TOP
            )

    def open_logs(self):
        try:
            path = str(LOGS_DIR.resolve())
            webbrowser.open('file://' + path)
            InfoBar.success(
                title="打开成功",
                content="已打开日志目录",
                parent=self,
                position=InfoBarPosition.TOP
            )
        except Exception as e:
            InfoBar.error(
                title="打开失败",
                content=str(e),
                parent=self,
                position=InfoBarPosition.TOP
            )
