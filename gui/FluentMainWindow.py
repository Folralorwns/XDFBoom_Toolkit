from PySide6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import QSettings, QPropertyAnimation, QEasingCurve, Qt, QTimer
from PySide6.QtGui import QCloseEvent
import sys
import traceback
from qfluentwidgets import (
    FluentWindow, NavigationInterface, NavigationItemPosition,
    StrongBodyLabel, FluentIcon, AvatarWidget, setTheme, isDarkTheme, Theme,
    InfoBar, InfoBarPosition, MessageBox
)
from gui.pages.HomePage import HomePage
from gui.pages.mtk_flash_page import MTKFlashPage
from gui.pages.adb_page import ADBPage
from gui.pages.SettingsPage import SettingsPage
from core.logging_config import logger


class FluentMainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        # 设置全局异常处理
        sys.excepthook = self.handle_exception
        
        self.setWindowTitle("XDFBoom Toolkit")
        self.resize(1200, 800)
        
        # 初始化设置
        self.settings = QSettings('XDFBoom', 'Toolkit')
        self.init_ui()
        self.init_navigation()
        self.load_theme()  # 加载保存的主题设置
        
        # 初始化导航栏动画
        self.nav_animation = QPropertyAnimation(self.nav_interface, b"minimumWidth")
        self.nav_animation.setDuration(200)
        self.nav_animation.setEasingCurve(QEasingCurve.InOutQuad)
        
        # 初始化导航栏自动折叠计时器
        self.collapse_timer = QTimer()
        self.collapse_timer.setSingleShot(True)
        self.collapse_timer.timeout.connect(self._auto_collapse_nav)

    def handle_exception(self, exc_type, exc_value, exc_traceback):
        """全局异常处理"""
        error_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        logger.error(f"发生未捕获的异常: {error_msg}")
        
        # 显示错误对话框
        w = MessageBox(
            '程序错误',
            f'程序发生错误：\n{str(exc_value)}\n\n是否要查看详细错误信息？',
            self
        )
        if w.exec():
            # 显示详细错误信息
            MessageBox(
                '详细错误信息',
                error_msg,
                self
            ).exec()

    def closeEvent(self, event: QCloseEvent):
        """关闭事件处理"""
        w = MessageBox(
            '确认退出',
            '确定要退出程序吗？',
            self
        )
        if w.exec():
            event.accept()
        else:
            event.ignore()

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

    def load_theme(self):
        # 从设置中加载主题
        theme = self.settings.value('theme', 'light')
        if theme == 'dark':
            setTheme(Theme.DARK)
        else:
            setTheme(Theme.LIGHT)

    def toggle_theme(self):
        # 添加主题切换动画
        animation = QPropertyAnimation(self, b"windowOpacity")
        animation.setDuration(200)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        
        if isDarkTheme():
            animation.setStartValue(1.0)
            animation.setEndValue(0.0)
            animation.finished.connect(lambda: self._switch_to_light())
        else:
            animation.setStartValue(1.0)
            animation.setEndValue(0.0)
            animation.finished.connect(lambda: self._switch_to_dark())
            
        animation.start()

    def _switch_to_light(self):
        setTheme(Theme.LIGHT)
        self.settings.setValue('theme', 'light')
        self._show_theme_notification('已切换至浅色主题')

    def _switch_to_dark(self):
        setTheme(Theme.DARK)
        self.settings.setValue('theme', 'dark')
        self._show_theme_notification('已切换至深色主题')

    def _show_theme_notification(self, message):
        InfoBar.success(
            title='主题切换',
            content=message,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )

    def enterEvent(self, event):
        try:
            if not self.nav_interface.isExpanded():
                self._expand_nav()
        except Exception as e:
            logger.error(f"导航展开异常: {e}")

    def leaveEvent(self, event):
        try:
            if self.nav_interface.isExpanded():
                self.collapse_timer.start(1000)  # 1秒后自动折叠
        except Exception as e:
            logger.error(f"导航收缩异常: {e}")

    def _expand_nav(self):
        """展开导航栏"""
        self.collapse_timer.stop()
        self.nav_animation.setStartValue(self.nav_interface.minimumWidth())
        self.nav_animation.setEndValue(300)
        self.nav_animation.start()
        self.nav_interface.expand()

    def _auto_collapse_nav(self):
        """自动折叠导航栏"""
        if not self.nav_interface.isExpanded():
            return
            
        self.nav_animation.setStartValue(self.nav_interface.minimumWidth())
        self.nav_animation.setEndValue(65)
        self.nav_animation.start()
        self.nav_interface.collapse()
