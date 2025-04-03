import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QMessageBox, QComboBox
)
from PySide6.QtCore import Qt
from core.path_manager import MTKCLIENT_DIR, MTK_EXAMPLES_DIR
from core.adb_manager import adb_connection_check

class MTKFlashPage(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_script = None
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        # 提示文字
        self.label = QLabel("刷机会清除所有数据，执行前请确认设备已连接。\n请选择要运行的 MTKClient 脚本：")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 15px;")
        layout.addWidget(self.label)

        # 脚本选择器
        self.script_combo = QComboBox()
        self.populate_script_list()
        layout.addWidget(self.script_combo)

        # 执行按钮
        self.flash_button = QPushButton("⚠️ 开始刷机")
        self.flash_button.setStyleSheet("""
            background-color: #e74c3c;
            color: white;
            font-size: 16px;
            font-weight: bold;
            border-radius: 10px;
            padding: 10px;
        """)
        self.flash_button.clicked.connect(self.confirm_and_flash)
        layout.addWidget(self.flash_button)

        self.setLayout(layout)

    def populate_script_list(self):
        """读取 examples/ 下的 .txt / .py 脚本文件"""
        if not MTK_EXAMPLES_DIR.exists():
            self.script_combo.addItem("（未找到脚本目录）")
            self.script_combo.setEnabled(False)
            return

        scripts = [f for f in MTK_EXAMPLES_DIR.iterdir() if f.suffix in ('.py', '.txt')]
        if not scripts:
            self.script_combo.addItem("（无可用脚本）")
            self.script_combo.setEnabled(False)
            return

        for script in scripts:
            self.script_combo.addItem(script.name)

    def confirm_and_flash(self):
        script_name = self.script_combo.currentText()
        if not script_name or script_name.startswith("（"):
            QMessageBox.warning(self, "无效脚本", "请选择一个有效的刷机脚本")
            return

        reply = QMessageBox.question(
            self,
            "确认刷机",
            f"将运行脚本：{script_name}\n该操作将清除所有数据，是否继续？",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.run_mtk_script(script_name)

    def run_mtk_script(self, script_name: str):
        try:
            adb_connection_check()
            os.chdir(MTKCLIENT_DIR)
            command = f'python mtk.py script examples/{script_name}'
            print(f"执行命令：{command}")
            result = os.system(command)
            if result == 0:
                QMessageBox.information(self, "刷机完成", "脚本执行成功，请拔线！")
            else:
                QMessageBox.warning(self, "刷机失败", "脚本执行出错，请检查控制台日志")
        except Exception as e:
            QMessageBox.critical(self, "异常", str(e))
