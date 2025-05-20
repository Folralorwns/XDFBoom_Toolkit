from qfluentwidgets import (
    FluentWindow, CardWidget, ComboBox, PrimaryPushButton,
    SubtitleLabel, TextEdit, LineEdit,InfoBar, InfoBarPosition
)
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget
from logic.flash_tool import run_flash_script, run_custom_mtk_command
import subprocess


class MTKFlashPage(FluentWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MTK 刷机工具")
        self.resize(960, 700)

        self.device_connected = False  # 是否有设备连接

        self.init_ui()

    def init_ui(self):
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        self.layout = QVBoxLayout(self.main_widget)
        self.layout.setContentsMargins(20, 20, 20, 20)

        self.card = CardWidget("刷机助手", "请选择刷机脚本或自定义命令")
        self.layout.addWidget(self.card)

        self.card_layout = QVBoxLayout()
        self.card.setLayout(self.card_layout)

        # 设备检测+刷新
        self.device_layout = QHBoxLayout()
        self.device_status = SubtitleLabel("设备状态：未知")
        self.refresh_btn = PrimaryPushButton("刷新设备")
        self.refresh_btn.clicked.connect(self.check_device)

        self.device_layout.addWidget(self.device_status)
        self.device_layout.addWidget(self.refresh_btn)
        self.card_layout.addLayout(self.device_layout)

        # 脚本选择 + 刷机按钮
        self.flash_layout = QHBoxLayout()
        self.script_selector = ComboBox()
        self.script_selector.addItems([
            "example.xml",
            "recovery.xml",
            "boot_only.xml"
        ])

        self.flash_button = PrimaryPushButton("执行刷机")
        self.flash_button.clicked.connect(self.run_flash)

        self.flash_layout.addWidget(self.script_selector)
        self.flash_layout.addWidget(self.flash_button)
        self.card_layout.addLayout(self.flash_layout)

        # 自定义命令输入 + 执行按钮
        self.custom_layout = QHBoxLayout()
        self.custom_command_box = LineEdit(placeholderText="请输入简短MTK指令，如: e userdata")
        self.custom_run_btn = PrimaryPushButton("执行自定义命令")
        self.custom_run_btn.clicked.connect(self.run_custom_command)

        self.custom_layout.addWidget(self.custom_command_box)
        self.custom_layout.addWidget(self.custom_run_btn)
        self.card_layout.addLayout(self.custom_layout)

        # 日志输出区域
        self.log_output = TextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setPlaceholderText("执行日志将在此显示...")
        self.log_output.setFixedHeight(250)
        self.card_layout.addWidget(self.log_output)

        # 初始化检测设备
        self.check_device()

    def append_log(self, msg: str):
        self.log_output.append(msg)
        self.log_output.verticalScrollBar().setValue(self.log_output.verticalScrollBar().maximum())

    def check_device(self):
        # 这里只简单模拟检测 —— MTK设备通常不会直接显示，需要在刷机中检测
        # 我们假定adb连接表示设备在线
        try:
            result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
            devices = [line for line in result.stdout.splitlines() if 'device' in line and not line.startswith('List')]
            if len(devices) == 1:
                self.device_connected = True
                self.device_status.setText(f"设备已连接 ✅ {devices[0].split()[0]}")
                InfoBar.success(
                    title="设备已连接",
                    content="检测到一个设备，准备刷机",
                    parent=self,
                    position=InfoBarPosition.TOP
                )
            elif len(devices) == 0:
                self.device_connected = False
                self.device_status.setText("未检测到设备 ❌")
                InfoBar.error(
                    title="无设备连接",
                    content="请连接设备后刷新",
                    parent=self,
                    position=InfoBarPosition.TOP
                )
            else:
                self.device_connected = False
                self.device_status.setText("检测到多个设备 ❌")
                InfoBar.error(
                    title="检测到多个设备",
                    content="请只连接一个设备",
                    parent=self,
                    position=InfoBarPosition.TOP
                )
        except Exception as e:
            self.device_connected = False
            self.device_status.setText(f"检测异常 ❌ {e}")

    def run_flash(self):
        if not self.device_connected:
            InfoBar.error(
                title="设备未连接",
                content="请连接设备后再刷机",
                parent=self,
                position=InfoBarPosition.TOP
            )
            return

        script = self.script_selector.currentText()
        run_flash_script(script, log_callback=self.append_log)
        InfoBar.success(
            title="刷机任务发送完成",
            content=f"执行脚本：{script}",
            parent=self,
            position=InfoBarPosition.TOP
        )

    def run_custom_command(self):
        if not self.device_connected:
            InfoBar.error(
                title="设备未连接",
                content="请连接设备后再执行命令",
                parent=self,
                position=InfoBarPosition.TOP
            )
            return

        custom_cmd = self.custom_command_box.text().strip()
        if not custom_cmd:
            InfoBar.error(
                title="命令为空",
                content="请输入有效的MTK指令",
                parent=self,
                position=InfoBarPosition.TOP
            )
            return

        run_custom_mtk_command(custom_cmd, log_callback=self.append_log)
        InfoBar.success(
            title="自定义命令发送完成",
            content=f"指令：{custom_cmd}",
            parent=self,
            position=InfoBarPosition.TOP
        )
