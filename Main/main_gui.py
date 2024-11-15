from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFrame
from PySide6.QtCore import Qt
from qfluentwidgets import (
    NavigationInterface, NavigationItemPosition,
    InfoCard, is_dark_theme, set_theme, FluentLabel, HyperlinkButton,
    PrimaryPushButton, CheckBox, ComboBox
)
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("XDFBoom Toolkit")
        self.resize(1000, 600)

        # 设置 Fluent 主题
        set_theme(is_dark_theme())

        # 创建主布局
        main_layout = QHBoxLayout()
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # 侧边栏导航
        self.navigation = NavigationInterface()
        self.init_navigation()
        main_layout.addWidget(self.navigation)

        # 主内容区域
        self.main_content = QVBoxLayout()
        content_widget = QWidget()
        content_widget.setLayout(self.main_content)
        main_layout.addWidget(content_widget, 1)

        # 信息卡片
        self.add_info_cards()

        # 基础控件示例
        self.add_basic_input_samples()

    def init_navigation(self):
        """初始化侧边栏导航"""
        self.navigation.addItem(
            routeKey="home", icon="home", text="主页", onClick=self.show_home
        )
        self.navigation.addItem(
            routeKey="github", icon="github", text="GitHub Repo", onClick=self.show_github
        )
        self.navigation.addItem(
            routeKey="samples", icon="code", text="示例代码", onClick=self.show_samples
        )
        self.navigation.addItem(
            routeKey="feedback", icon="message", text="反馈", onClick=self.show_feedback
        )

        # 添加分隔
        self.navigation.addSeparator()

        # 底部设置按钮
        self.navigation.addItem(
            routeKey="settings", icon="settings", text="设置", onClick=self.show_settings,
            position=NavigationItemPosition.BOTTOM
        )

    def add_info_cards(self):
        """添加信息卡片"""
        # 信息卡片布局
        info_card_layout = QHBoxLayout()
        
        # “开始”信息卡片
        start_card = InfoCard(
            title="开始使用", content="提供应用开发选项和示例的概述。"
        )
        info_card_layout.addWidget(start_card)
        
        # “GitHub”信息卡片
        github_card = InfoCard(
            title="GitHub Repo", content="最新的流畅设计控件和样式库。"
        )
        info_card_layout.addWidget(github_card)
        
        # “代码示例”信息卡片
        code_samples_card = InfoCard(
            title="代码示例", content="包含特定任务、功能和 API 的示例代码。"
        )
        info_card_layout.addWidget(code_samples_card)
        
        # “发送反馈”信息卡片
        feedback_card = InfoCard(
            title="发送反馈", content="通过提供反馈帮助我们改进 PyQt-Fluent-Widgets。"
        )
        info_card_layout.addWidget(feedback_card)

        # 将信息卡片添加到主内容布局
        self.main_content.addLayout(info_card_layout)

    def add_basic_input_samples(self):
        """添加基础输入控件示例"""
        # 基础控件标签
        label = FluentLabel("基础控件示例", self)
        label.setAlignment(Qt.AlignLeft)
        label.setStyleSheet("font-size: 20px; font-weight: bold; margin-top: 20px;")
        self.main_content.addWidget(label)

        # 控件布局
        controls_layout = QHBoxLayout()

        # 添加按钮示例
        button = PrimaryPushButton("按钮")
        controls_layout.addWidget(button)

        # 添加复选框示例
        checkbox = CheckBox("复选框")
        controls_layout.addWidget(checkbox)

        # 添加超链接按钮示例
        hyperlink_button = HyperlinkButton("超链接按钮")
        controls_layout.addWidget(hyperlink_button)

        # 添加下拉框示例
        combo_box = ComboBox()
        combo_box.addItems(["选项 1", "选项 2", "选项 3"])
        controls_layout.addWidget(combo_box)

        # 将控件布局添加到主内容布局
        self.main_content.addLayout(controls_layout)

    # 侧边栏按钮点击事件
    def show_home(self):
        print("主页按钮被点击")

    def show_github(self):
        print("GitHub 按钮被点击")

    def show_samples(self):
        print("示例代码按钮被点击")

    def show_feedback(self):
        print("反馈按钮被点击")

    def show_settings(self):
        print("设置按钮被点击")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
