import sys
import os
import time
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, QMessageBox
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from qfluentwidgets import NavigationInterface, FluentIcon, Theme, setTheme
from tabulate import tabulate

# 假设导入外部函数和常量
from External.env_ver_checker import checker, workmode
from External.ROM_Dowload_Link import *
from External.Android_Debug_Bridge import flash_dir, adb, adb_shell, adb_connection_check, fastboot, fastboot_connection_check
from External.Dowloader import Down_and_Dec
from External.Path_Dict import Now_Path
from External.Security_Agreement import agreement_check
from External.Screen_Clear import prepare_screen


class FluentGalleryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fluent Gallery")
        self.resize(1200, 700)

        # Set Fluent Dark Theme
        setTheme(Theme.DARK)

        # Main layout
        main_layout = QHBoxLayout()

        # Sidebar with NavigationInterface
        self.navigation_interface = NavigationInterface(self)
        self.navigation_interface.addItem(
            routeKey="getting_started",
            icon=FluentIcon.DOCUMENT,
            text="环境检查",
            onClick=self.check_environment
        )
        self.navigation_interface.addItem(
            routeKey="install_tools",
            icon=FluentIcon.SETTING,
            text="工具包配置",
            onClick=self.install_tools
        )
        self.navigation_interface.addItem(
            routeKey="flash_system",
            icon=FluentIcon.UPDATE,
            text="刷入系统",
            onClick=self.flash_system
        )
        self.navigation_interface.addItem(
            routeKey="install_apps",
            icon=FluentIcon.DOWNLOAD,
            text="安装常用软件",
            onClick=self.install_apps
        )
        self.navigation_interface.addItem(
            routeKey="network_fix",
            icon=FluentIcon.WIFI,
            text="修复网络问题",
            onClick=self.fix_network
        )

        main_layout.addWidget(self.navigation_interface)

        # Main content area
        self.content_area = QWidget()
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_area.setLayout(self.content_layout)

        # Add header
        self.header = QLabel("Fluent Gallery", alignment=Qt.AlignCenter)
        self.header.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.content_layout.addWidget(self.header)

        main_layout.addWidget(self.content_area)

        # Main widget
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    # Button functionality
    def check_environment(self):
        self.header.setText("环境检查")
        prepare_screen()
        checker(1)
        checker(2)
        checker(3)
        QMessageBox.information(self, "环境检查", "环境检查完成！")

    def install_tools(self):
        self.header.setText("工具包配置")
        prepare_screen()
        toolkit_path = 'C:/N1/Toolkit'
        log_path = 'C:/N1/Logs/Package_Env_Installed'
        if os.path.exists(toolkit_path) and os.path.exists(log_path):
            QMessageBox.information(self, "配置检查", "工具包已配置！")
        else:
            Down_and_Dec('tools', Toolkit_link, Toolkit)
            with open(log_path, 'w+') as f:
                pass
            QMessageBox.information(self, "配置成功", "工具包配置完成！")

    def flash_system(self):
        self.header.setText("刷入系统")
        if workmode == "受限":
            QMessageBox.warning(self, "限制模式", "请先配置工具包！")
            return

        # Display system options
        system_info = "\n".join([f"{sys['编号']}. {sys['系统名称']} - Android {sys['安卓版本']} - 包含谷歌套件: {sys['包含谷歌套件']}"
                                 for sys in system_list])
        system_id, ok = QMessageBox.getInt(self, "选择系统", f"可用系统:\n{system_info}\n请输入系统编号：")
        if ok:
            selected_system = next((sys for sys in system_list if sys['编号'] == system_id), None)
            if selected_system:
                Down_and_Dec('image', selected_system['下载链接'], selected_system['文件名'])
                QMessageBox.information(self, "刷入系统", f"已选择系统：{selected_system['系统名称']}，刷入完成！")
            else:
                QMessageBox.warning(self, "错误", "无效的系统编号。")

    def install_apps(self):
        self.header.setText("安装常用软件")
        if workmode == "受限":
            QMessageBox.warning(self, "限制模式", "请先配置工具包！")
            return

        prepare_screen()
        adb_connection_check()
        app_list = [
            "Android_System_WebView.apk", "Gboard.apk", "Huawei_AppGallery.apk",
            "Huawei_Mobile_Services_Core.apk", "HUAWEI_Services_Framework.apk", "MT_Manager.apk", "Via_Browser.apk"
        ]
        for app in app_list:
            adb(f'install -r C:/N1/Toolkit/ADB/App/{app}')
        adb('kill-server')
        QMessageBox.information(self, "安装完成", "所有应用已成功安装！")

    def fix_network(self):
        self.header.setText("修复网络问题")
        if workmode == "受限":
            QMessageBox.warning(self, "限制模式", "请先配置工具包！")
            return

        prepare_screen()
        adb_connection_check()
        adb_shell('settings delete global captive_portal_http_url')
        adb_shell('settings delete global captive_portal_https_url')
        adb_shell('settings put global captive_portal_http_url http://connect.rom.miui.com/generate_204')
        adb_shell('settings put global captive_portal_https_url https://connect.rom.miui.com/generate_204')
        adb('kill-server')
        QMessageBox.information(self, "修复完成", "网络问题已解决！")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gallery = FluentGalleryApp()
    gallery.show()
    sys.exit(app.exec())
