from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QCheckBox, QFrame, QPushButton, QScrollArea
)
from PySide6.QtGui import QPixmap, QIcon, QFont
from PySide6.QtCore import Qt
from core.path_manager import get_icon_path

class AboutUsWindow(QWidget):
    def __init__(self, embed=False):
        super().__init__()
        self.init_ui(embed)

    def init_ui(self, embed):
        main_layout = QVBoxLayout(self)

        # 图片 Logo
        label_image = QLabel()
        pixmap = QPixmap(str(get_icon_path()))
        label_image.setPixmap(pixmap.scaled(800, 200, Qt.KeepAspectRatio))
        label_image.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(label_image)

        # 标题
        title_label = QLabel("XDFBoom Toolkit Open Source Project")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 26px; font-weight: bold; color: #333;")
        main_layout.addWidget(title_label)

        self.add_separator(main_layout)

        # 信息区
        info_text = QLabel(
            '<p style="color: #FF8C00; font-weight: bold;">⚠️ Warning</p>'
            '<p style="margin-left: 10px;">如果程序出现闪退，请发送 issue<br>暂不支持 V1.2.7 及以上学习机</p>'
            '<p style="color: #32CD32; font-weight: bold;">💡 Tip</p>'
            '<p style="margin-left: 10px;">打包推荐使用 Nuitka</p>'
            '<p style="color: #6A5ACD; font-weight: bold;">⚠️ Important</p>'
            '<p style="margin-left: 10px;">最低系统要求：Windows 10 x64</p>'
        )
        info_text.setWordWrap(True)
        info_text.setAlignment(Qt.AlignLeft)
        info_text.setStyleSheet("font-size: 14px;")
        main_layout.addWidget(info_text)

        self.add_separator(main_layout)

        # 使用方式
        usage_label = QLabel("使用方式")
        usage_label.setAlignment(Qt.AlignLeft)
        usage_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        main_layout.addWidget(usage_label)

        usage_content = QLabel("开袋即食")
        usage_content.setAlignment(Qt.AlignLeft)
        usage_content.setStyleSheet("font-size: 14px; color: #555; margin-left: 10px;")
        main_layout.addWidget(usage_content)

        self.add_separator(main_layout)

        # TODO 项
        todo_label = QLabel("WILLTODO")
        todo_label.setAlignment(Qt.AlignLeft)
        todo_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        main_layout.addWidget(todo_label)

        todo_layout = QVBoxLayout()
        for text in ["编写GUI完全界面", "更严格的日志分析", "适配V1.2.7及其以上版本"]:
            cb = QCheckBox(text)
            cb.setChecked(False)
            cb.setDisabled(True)
            cb.setStyleSheet("font-size: 14px; color: #555;")
            todo_layout.addWidget(cb)
        main_layout.addLayout(todo_layout)

        self.add_separator(main_layout)

        # 下载链接
        download_label = QLabel("下载链接")
        download_label.setAlignment(Qt.AlignLeft)
        download_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        main_layout.addWidget(download_label)

        link_label = QLabel(
            '<a href="https://github.com/Folralorwns/XDFBoom_Toolkit" '
            'style="color: #1E90FF; text-decoration: none;">开源界面</a> | '
            '<a href="https://blog.xdfboom.com" '
            'style="color: #1E90FF; text-decoration: none;">XDFBoom 小站</a>'
        )
        link_label.setOpenExternalLinks(True)
        link_label.setAlignment(Qt.AlignLeft)
        link_label.setStyleSheet("font-size: 14px; margin-left: 10px;")
        main_layout.addWidget(link_label)

        # 留个位置撑满底部
        main_layout.addStretch()

        # 退出按钮（仅在独立窗口模式显示）
        if not embed:
            exit_btn = QPushButton("退出")
            exit_btn.setStyleSheet("""
                background-color: #1E90FF;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 10px;
                padding: 10px 20px;
            """)
            exit_btn.clicked.connect(self.close)
            main_layout.addWidget(exit_btn)

    def add_separator(self, layout):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("color: #CCCCCC; margin: 15px 0;")
        layout.addWidget(line)
