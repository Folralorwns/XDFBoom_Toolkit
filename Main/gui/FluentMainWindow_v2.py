
from PySide6.QtWidgets import QMainWindow, QStackedWidget
from qfluentwidgets import (
    NavigationInterface, NavigationItemPosition, FluentIcon,
    Theme, AvatarWidget, PushButton
)
from gui.external.theme_switcher import ThemeSwitcher
from PySide6.QtCore import Qt
from gui.about_us import AboutUsWindow
from gui.mtk_flash_page import MTKFlashPage
# from gui.network_fix_page import NetworkFixPage
# from gui.settings_page import SettingsPage


class FluentMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("XDFBoom Toolkit")
        self.resize(1200, 800)

        # 中央区域：页面堆栈
        self.stack = QStackedWidget(self)
        self.setCentralWidget(self.stack)

        # 左侧导航界面
        self.nav_interface = NavigationInterface(self, showMenuButton=True)
        self.nav_interface.setObjectName("navigationInterface")
        self.nav_interface.setMinimumWidth(280)
        self.nav_interface.setMaximumWidth(300)
        self.nav_interface.setResizeEnabled(False)
        self.nav_interface.setExpanding(True)
        self.nav_interface.setAutoResize(True)

        # 页面注册
        self.register_pages()

        # 设置当前页面为关于我们
        self.nav_interface.setCurrentItem('about')

        # 底部设置按钮 + 明暗切换
        self.init_bottom_layout()

        # 添加导航到窗口左边
        self.addDockWidget(Qt.LeftDockWidgetArea, self.nav_interface)

    def register_pages(self):
        # 关于我们页
        about = AboutUsWindow(embed=True)
        self.stack.addWidget(about)
        self.nav_interface.addItem(
            routeKey='about',
            icon=FluentIcon.INFO,
            text='关于我们',
            onClick=lambda: self.stack.setCurrentWidget(about)
        )

        # 刷机工具页
        flash = MTKFlashPage()
        self.stack.addWidget(flash)
        self.nav_interface.addItem(
            routeKey='flash',
            icon=FluentIcon.UPDATE,
            text='刷机工具',
            onClick=lambda: self.stack.setCurrentWidget(flash)
        )

    def init_bottom_layout(self):
        # 头像 + 设置
        avatar = AvatarWidget(
            'zhiyiYo',
            'https://avatars.githubusercontent.com/u/5803001?v=4',
            'XDFBoom 开发者'
        )
        avatar.setToolTip("点击切换明暗模式")
        avatar.clicked.connect(self.toggle_theme)

        self.nav_interface.addWidget(
            routeKey='avatar',
            widget=avatar,
            position=NavigationItemPosition.BOTTOM
        )

        # 设置按钮（仅示例）
        settings_btn = PushButton("设置")
        settings_btn.clicked.connect(self.toggle_theme)
        self.nav_interface.addWidget(
            routeKey='settings',
            widget=settings_btn,
            position=NavigationItemPosition.BOTTOM
        )

    def toggle_theme(self):
        # 使用过渡动画切换主题
        current = ThemeSwitcher.instance().theme
        target = Theme.DARK if current == Theme.LIGHT else Theme.LIGHT
        ThemeSwitcher.instance().setThemeWithTransition(target)
