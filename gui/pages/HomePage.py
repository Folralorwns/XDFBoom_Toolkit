
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from qfluentwidgets import (
    CardWidget, StrongBodyLabel, SubtitleLabel, PrimaryPushButton, FluentIcon
)
from PySide6.QtCore import Qt


class HomePage(QWidget):
    def __init__(self, parent=None, switch_callback=None):
        super().__init__(parent)
        self.switch_callback = switch_callback  # 切换到其他页面的回调函数

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)

        # 顶部大标题
        self.title_label = StrongBodyLabel("欢迎来到 XDFBoom Toolkit")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title_label)

        # 卡片区
        self.card_container = QHBoxLayout()
        self.layout.addLayout(self.card_container)

        # 加入各个功能卡片
        self.add_card(
            icon=FluentIcon.UPDATE,
            title="刷机工具",
            description="快速刷机与脚本管理",
            target_route='flashMain'
        )

        self.add_card(
            icon=FluentIcon.CODE,
            title="ADB工具",
            description="管理ADB与Fastboot指令",
            target_route='adbMain'
        )

        self.add_card(
            icon=FluentIcon.SETTING,
            title="设置",
            description="应用更新与通用设置",
            target_route='settingsMain'
        )

    def add_card(self, icon, title, description, target_route):
        card = CardWidget(title, description)
        card_layout = QVBoxLayout()
        card.setLayout(card_layout)

        title_label = StrongBodyLabel(title)
        subtitle_label = SubtitleLabel(description)

        button = PrimaryPushButton(f"前往 {title}")
        button.setIcon(icon)
        button.clicked.connect(lambda: self.jump_to(target_route))

        card_layout.addWidget(title_label)
        card_layout.addWidget(subtitle_label)
        card_layout.addWidget(button)

        self.card_container.addWidget(card)

    def jump_to(self, route_key):
        if self.switch_callback:
            self.switch_callback(route_key)
