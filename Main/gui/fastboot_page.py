from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PySide6.QtCore import Qt
import os
from core.adb_manager import fastboot_connection_check
from core.path_manager import mtk_script_path

class FastbootPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("刷机将清除所有数据，请谨慎操作。")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        self.btn_flash = QPushButton("⚠️ 开始刷机")
        self.btn_flash.setStyleSheet("background-color: #e74c3c; color: white; font-weight: bold;")
        self.btn_flash.clicked.connect(self.confirm_flash)
        layout.addWidget(self.btn_flash)

        self.setLayout(layout)

    def confirm_flash(self):
        reply = QMessageBox.question(
            self,
            "二次确认",
            "刷机会清除数据，您确定要继续吗？",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.flash_device()

    def flash_device(self):
        QMessageBox.information(self, "执行中", "准备进入 fastboot...")
        fastboot_connection_check()
        try:
            os.system(f'python {mtk_script_path} script C:/N1/Toolkit/tools/run.example')
            QMessageBox.information(self, "刷机完成", "刷机结束，请立即拔线")
        except Exception as e:
            QMessageBox.critical(self, "刷机失败", str(e))
