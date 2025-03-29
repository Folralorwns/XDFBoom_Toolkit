from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PySide6.QtCore import Qt
from core.adb_manager import adb_connection_check, adb_shell, adb

class NetworkFixPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("一键修复安卓网络连接异常（去除 × 和 ！）")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        self.btn_fix = QPushButton("🔧 修复网络")
        self.btn_fix.setStyleSheet("background-color: #3498db; color: white; font-weight: bold;")
        self.btn_fix.clicked.connect(self.fix_network)
        layout.addWidget(self.btn_fix)

        self.setLayout(layout)

    def fix_network(self):
        try:
            adb_connection_check()
            adb_shell('settings delete global captive_portal_http_url')
            adb_shell('settings delete global captive_portal_https_url')
            adb_shell('settings put global captive_portal_http_url http://connect.rom.miui.com/generate_204')
            adb_shell('settings put global captive_portal_https_url https://connect.rom.miui.com/generate_204')
            adb('kill-server')
            QMessageBox.information(self, "修复完成", "网络修复成功！")
        except Exception as e:
            QMessageBox.critical(self, "错误", str(e))
