
import sys
import requests
import webbrowser
from PySide6.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import (
    FluentWindow, CardWidget, StrongBodyLabel, SubtitleLabel,
    TextEdit, PrimaryPushButton, InfoBar, InfoBarPosition
)


UPDATE_JSON_URL = "https://raw.githubusercontent.com/Folralorwns/XDFBoom_Toolkit/main/version.json"
DOWNLOAD_URL = "https://github.com/Folralorwns/XDFBoom_Toolkit/releases"
CURRENT_VERSION = "V6.0.5"


class UpdatePopup(FluentWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("检查更新 | XDFBoom Toolkit")
        self.resize(680, 500)
        self.update_info = {}

        self.init_ui()
        self.check_update()

    def init_ui(self):
        self.central = QWidget(self)
        self.setCentralWidget(self.central)

        self.layout = QVBoxLayout(self.central)
        self.layout.setContentsMargins(20, 20, 20, 20)

        # 卡片
        self.card = CardWidget("发现新版本", "请及时更新以获得更好的体验")
        self.layout.addWidget(self.card)

        self.card_layout = QVBoxLayout()
        self.card.setLayout(self.card_layout)

        self.version_label = StrongBodyLabel(f"当前版本：{CURRENT_VERSION}")
        self.card_layout.addWidget(self.version_label)

        self.latest_version_label = StrongBodyLabel("最新版本：--")
        self.card_layout.addWidget(self.latest_version_label)

        self.changelog_text = TextEdit()
        self.changelog_text.setPlaceholderText("正在获取更新日志...")
        self.changelog_text.setReadOnly(True)
        self.changelog_text.setFixedHeight(250)
        self.card_layout.addWidget(self.changelog_text)

        # 按钮组
        self.download_button = PrimaryPushButton("立即前往下载")
        self.download_button.clicked.connect(self.open_download_page)
        self.download_button.setEnabled(False)

        self.skip_button = PrimaryPushButton("以后再说")
        self.skip_button.clicked.connect(self.close)

        self.layout.addWidget(self.download_button)
        self.layout.addWidget(self.skip_button)

    def check_update(self):
        try:
            resp = requests.get(UPDATE_JSON_URL, timeout=5)
            if resp.status_code == 200:
                self.update_info = resp.json()
                latest_version = self.update_info.get("latest", "--")
                changelog = self.update_info.get("changelog", "无更新内容")

                self.latest_version_label.setText(f"最新版本：{latest_version}")
                self.changelog_text.setPlainText(changelog)

                if self.compare_version(CURRENT_VERSION, latest_version) < 0:
                    InfoBar.success(
                        title="发现新版本",
                        content=f"检测到新版本 {latest_version}",
                        parent=self,
                        position=InfoBarPosition.TOP
                    )
                    self.download_button.setEnabled(True)
                else:
                    InfoBar.success(
                        title="已是最新版本",
                        content="当前版本已经是最新，无需更新",
                        parent=self,
                        position=InfoBarPosition.TOP
                    )
                    self.download_button.setEnabled(False)

            else:
                raise Exception(f"HTTP错误: {resp.status_code}")

        except Exception as e:
            InfoBar.error(
                title="检查更新失败",
                content=str(e),
                parent=self,
                position=InfoBarPosition.TOP
            )

    def compare_version(self, v1, v2):
        # 版本比较函数
        v1_parts = [int(x) for x in v1.strip('Vv').split('.')]
        v2_parts = [int(x) for x in v2.strip('Vv').split('.')]
        for p1, p2 in zip(v1_parts, v2_parts):
            if p1 != p2:
                return p1 - p2
        return len(v1_parts) - len(v2_parts)

    def open_download_page(self):
        try:
            webbrowser.open(DOWNLOAD_URL)
            InfoBar.success(
                title="正在打开下载页",
                content="请稍候...",
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
