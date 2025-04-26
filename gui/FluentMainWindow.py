
from PySide6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QHBoxLayout
from qfluentwidgets import (
    FluentWindow, NavigationInterface, NavigationItemPosition,
    StrongBodyLabel, FluentIcon, AvatarWidget, setTheme, isDarkTheme, Theme
)
from gui.pages.home_page import HomePage
from gui.pages.mtk_flash_page import MTKFlashPage
from gui.pages.adb_page import ADBPage
from gui.pages.settings_page import SettingsPage
from core.logging_config import logger


class FluentMainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("XDFBoom Toolkit")
        self.resize(1200, 800)

        self.init_ui()
        self.init_navigation()
        self.theme_switcher()  # 可选

    def init_ui(self):
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QHBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.nav_interface = NavigationInterface(self)
        self.nav_interface.setMinimumWidth(65)
        self.nav_interface.setMaximumWidth(300)
        self.nav_interface.setResizeEnabled(True)
        self.nav_interface.setAutoResize(True)
        self.nav_interface.expandSetting = False

        self.stack = QStackedWidget(self)
        self.layout.addWidget(self.nav_interface)
        self.layout.addWidget(self.stack)

    def init_navigation(self):
        # 注册首页
        self.home_page = HomePage()
        self.stack.addWidget(self.home_page)
        self.nav_interface.addItem(
            routeKey='home',
            icon=FluentIcon.HOME,
            text='首页',
            onClick=lambda: self.stack.setCurrentWidget(self.home_page)
        )

        # 注册刷机工具父项
        self.nav_interface.addItem(
            routeKey='flashParent',
            icon=FluentIcon.UPDATE,
            text='刷机工具'
        )
        # 注册刷机子项
        self.flash_page = MTKFlashPage()
        self.stack.addWidget(self.flash_page)
        self.nav_interface.addSubInterface(
            parentRouteKey='flashParent',
            routeKey='flashMain',
            text='刷脚本',
            onClick=lambda: self.stack.setCurrentWidget(self.flash_page)
        )

        # 注册 ADB工具父项
        self.nav_interface.addItem(
            routeKey='adbParent',
            icon=FluentIcon.CODE,
            text='ADB工具'
        )
        # 注册 ADB 子项
        self.adb_page = ADBPage()
        self.stack.addWidget(self.adb_page)
        self.nav_interface.addSubInterface(
            parentRouteKey='adbParent',
            routeKey='adbMain',
            text='ADB & Fastboot工具',
            onClick=lambda: self.stack.setCurrentWidget(self.adb_page)
        )

        # 注册设置父项
        self.nav_interface.addItem(
            routeKey='settingsParent',
            icon=FluentIcon.SETTING,
            text='设置'
        )
        # 注册设置子项
        self.settings_page = SettingsPage()
        self.stack.addWidget(self.settings_page)
        self.nav_interface.addSubInterface(
            parentRouteKey='settingsParent',
            routeKey='settingsMain',
            text='通用设置',
            onClick=lambda: self.stack.setCurrentWidget(self.settings_page)
        )

        # Avatar底部按钮
        self.avatar = AvatarWidget('XDFBoom', 'https://avatars.githubusercontent.com/u/5803001?v=4', '切换主题')
        self.avatar.clicked.connect(self.toggle_theme)

        self.nav_interface.addWidget(
            routeKey='avatar',
            widget=self.avatar,
            position=NavigationItemPosition.BOTTOM
        )

        self.nav_interface.setCurrentItem('home')

    def toggle_theme(self):
        # 切换明暗模式
        if isDarkTheme():
            setTheme(Theme.LIGHT)
        else:
            setTheme(Theme.DARK)

    def enterEvent(self, event):
        try:
            if not self.nav_interface.isExpanded():
                self.nav_interface.expand()
        except Exception as e:
            logger.error(f"导航展开异常: {e}")

    def leaveEvent(self, event):
        try:
            if self.nav_interface.isExpanded():
                self.nav_interface.collapse()
        except Exception as e:
            logger.error(f"导航收缩异常: {e}")
