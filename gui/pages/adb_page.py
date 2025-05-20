
from qfluentwidgets import (
    FluentWindow, CardWidget, ComboBox, PrimaryPushButton,
    TextEdit, LineEdit,InfoBar, InfoBarPosition
)
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget
from logic.adb_tool import run_adb_command
from core.path_manager import ADB_PATH, FASTBOOT_PATH
import subprocess


class ADBPage(FluentWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ADB & Fastboot 工具")
        self.resize(960, 700)

        self.devices = []  # 存储设备 (序列号, 模式)

        self.init_ui()

    def init_ui(self):
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        self.layout = QVBoxLayout(self.main_widget)
        self.layout.setContentsMargins(20, 20, 20, 20)

        self.card = CardWidget("设备管理与命令执行", "请选择设备并执行ADB/Fastboot指令")
        self.layout.addWidget(self.card)

        self.card_layout = QVBoxLayout()
        self.card.setLayout(self.card_layout)

        # 设备列表 + 刷新按钮
        self.device_layout = QHBoxLayout()
        self.device_list = SimpleListWidget()
        self.device_list.setFixedHeight(120)
        self.refresh_btn = PrimaryPushButton("刷新设备")
        self.refresh_btn.clicked.connect(self.refresh_devices)

        self.device_layout.addWidget(self.device_list)
        self.device_layout.addWidget(self.refresh_btn)
        self.card_layout.addLayout(self.device_layout)

        # 预设命令部分
        self.preset_layout = QHBoxLayout()
        self.preset_selector = ComboBox()
        self.preset_selector.addItems([
            "adb reboot",
            "adb devices",
            "adb shell pm list packages",
            "fastboot devices",
            "fastboot reboot",
            "fastboot flash recovery recovery.img"
        ])

        self.preset_run_btn = PrimaryPushButton("执行预设命令")
        self.preset_run_btn.clicked.connect(self.run_preset_command)

        self.preset_layout.addWidget(self.preset_selector)
        self.preset_layout.addWidget(self.preset_run_btn)
        self.card_layout.addLayout(self.preset_layout)

        # 自定义命令部分
        self.custom_layout = QHBoxLayout()
        self.custom_command_box = LineEdit(placeholderText="请输入自定义 ADB 或 Fastboot 命令")
        self.custom_run_btn = PrimaryPushButton("执行自定义命令")
        self.custom_run_btn.clicked.connect(self.run_custom_command)

        self.custom_layout.addWidget(self.custom_command_box)
        self.custom_layout.addWidget(self.custom_run_btn)
        self.card_layout.addLayout(self.custom_layout)

        # 日志输出区
        self.log_output = TextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setPlaceholderText("执行日志将在此显示...")
        self.log_output.setFixedHeight(250)
        self.card_layout.addWidget(self.log_output)

        # 初始化时刷新一次设备
        self.refresh_devices()

    def append_log(self, msg: str):
        self.log_output.append(msg)
        self.log_output.verticalScrollBar().setValue(self.log_output.verticalScrollBar().maximum())

    def refresh_devices(self):
        self.devices = []
        self.device_list.clear()

        # 获取 adb devices
        adb_result = subprocess.run([str(ADB_PATH), 'devices'], capture_output=True, text=True)
        for line in adb_result.stdout.strip().splitlines()[1:]:
            if line.strip() and 'device' in line:
                serial = line.split()[0]
                self.devices.append((serial, 'adb'))
                self.device_list.addItem(f"[ADB] {serial}")

        # 获取 fastboot devices
        fastboot_result = subprocess.run([str(FASTBOOT_PATH), 'devices'], capture_output=True, text=True)
        for line in fastboot_result.stdout.strip().splitlines():
            if line.strip() and 'fastboot' in line:
                serial = line.split()[0]
                self.devices.append((serial, 'fastboot'))
                self.device_list.addItem(f"[FASTBOOT] {serial}")

    def get_selected_device(self):
        index = self.device_list.currentIndex().row()
        if 0 <= index < len(self.devices):
            return self.devices[index][0]  # 返回序列号
        else:
            return None

    def run_preset_command(self):
        device = self.get_selected_device()
        if not device:
            InfoBar.error(
                title="未选择设备",
                content="请先选择一个设备再执行命令",
                parent=self,
                position=InfoBarPosition.TOP
            )
            return

        cmd = self.preset_selector.currentText()
        parts = cmd.split()
        if parts[0] == 'adb':
            full_cmd = [str(ADB_PATH), '-s', device] + parts[1:]
        else:
            full_cmd = [str(FASTBOOT_PATH), '-s', device] + parts[1:]

        run_adb_command(full_cmd, log_callback=self.append_log)
        InfoBar.success(
            title="命令执行成功",
            content=f"{cmd} 已执行",
            parent=self,
            position=InfoBarPosition.TOP
        )

    def run_custom_command(self):
        device = self.get_selected_device()
        if not device:
            InfoBar.error(
                title="未选择设备",
                content="请先选择一个设备再执行命令",
                parent=self,
                position=InfoBarPosition.TOP
            )
            return

        user_cmd = self.custom_command_box.text().strip()
        if not user_cmd:
            InfoBar.error(
                title="命令为空",
                content="请输入有效命令",
                parent=self,
                position=InfoBarPosition.TOP
            )
            return

        parts = user_cmd.split()
        if parts[0] == 'adb':
            full_cmd = [str(ADB_PATH), '-s', device] + parts[1:]
        else:
            full_cmd = [str(FASTBOOT_PATH), '-s', device] + parts[1:]

        run_adb_command(full_cmd, log_callback=self.append_log)
        InfoBar.success(
            title="自定义命令执行成功",
            content="指令已发送",
            parent=self,
            position=InfoBarPosition.TOP
        )
