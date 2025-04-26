
from qfluentwidgets import (
    FluentWindow, CardWidget, StrongBodyLabel, SubtitleLabel,
    PrimaryPushButton, InfoBar, InfoBarPosition, HyperlinkLabel
)
from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel, QCheckBox, QFrame
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from core.path_manager import ico_light_theme
import sys
import webbrowser


class AboutUsPage(FluentWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("关于我们 | About Us")
        self.resize(880, 680)

        self.init_ui()

    def init_ui(self):
        self.central = QWidget(self)
        self.setCentralWidget(self.central)

        self.layout = QVBoxLayout(self.central)
        self.layout.setContentsMargins(20, 20, 20, 20)

        # 顶部Logo
        self.logo_label = QLabel(self)
        pixmap = QPixmap(str(ico_light_theme))
        self.logo_label.setPixmap(pixmap.scaled(800, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.logo_label)

        # 主标题
        self.title_label = StrongBodyLabel("XDFBoom Toolkit Open Source Project")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        self.add_separator()

        # 信息部分
        info_card = CardWidget("提示信息")
        info_layout = QVBoxLayout()
        info_card.setLayout(info_layout)

        warning_label = StrongBodyLabel("⚠️ Warning")
        tip_label = StrongBodyLabel("💡 Tip")
        important_label = StrongBodyLabel("⚠️ Important")

        warning_content = SubtitleLabel("如果您的程序出现了类似闪退的情况，请发送issue\n此程序暂时不支持V1.2.7及其以上版本的学习机")
        tip_content = SubtitleLabel("提示：打包请使用Auto-py-to-exe")
        important_content = SubtitleLabel("最低系统要求：Windows 10 x64")

        info_layout.addWidget(warning_label)
        info_layout.addWidget(warning_content)
        info_layout.addWidget(tip_label)
        info_layout.addWidget(tip_content)
        info_layout.addWidget(important_label)
        info_layout.addWidget(important_content)

        self.layout.addWidget(info_card)

        self.add_separator()

        # 使用方式
        usage_card = CardWidget("使用方式")
        usage_layout = QVBoxLayout()
        usage_card.setLayout(usage_layout)

        usage_layout.addWidget(StrongBodyLabel("开袋即食"))
        self.layout.addWidget(usage_card)

        self.add_separator()

        # WILLTODO
        todo_card = CardWidget("WILLTODO")
        todo_layout = QVBoxLayout()
        todo_card.setLayout(todo_layout)

        todo_layout.addWidget(QCheckBox("编写GUI完全界面"))
        todo_layout.addWidget(QCheckBox("更严格的日志分析"))
        todo_layout.addWidget(QCheckBox("适配V1.2.7及其以上版本"))

        self.layout.addWidget(todo_card)

        self.add_separator()

        # 下载链接
        link_card = CardWidget("下载链接")
        link_layout = QVBoxLayout()
        link_card.setLayout(link_layout)

        github_link = HyperlinkLabel("访问 GitHub 开源界面", self)
        github_link.setUrl("https://github.com/Folralorwns/XDFBoom_Toolkit")
        blog_link = HyperlinkLabel("访问 XDFBoom 小站发布地址", self)
        blog_link.setUrl("https://blog.xdfboom.com")

        link_layout.addWidget(github_link)
        link_layout.addWidget(blog_link)

        self.layout.addWidget(link_card)

    def add_separator(self):
        """添加分隔线"""
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(line)
