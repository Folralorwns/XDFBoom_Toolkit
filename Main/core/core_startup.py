import os
from PySide6.QtWidgets import QMessageBox
from gui.agreement_window import agreement_check
from config.global_state import (
    is_agreement_accepted,
    is_env_ready,
    is_toolkit_installed,
    USER_AGREEMENT_LOG_PATH,
    TOOLKIT_INSTALLED_LOG,
    ENV_DONE_LOG,
    WorkMode,
)
from config import global_state
from gui.main_window import MainWindow
from gui.update_popup import show_update_popup
from PySide6.QtWidgets import QApplication
import sys

def run():
    app = QApplication(sys.argv)

    # 步骤 1：协议确认
    if not is_agreement_accepted():
        agreement_check()

    # 步骤 2：环境检查
    if not is_env_ready():
        QMessageBox.warning(None, "环境未配置", "系统环境未配置，请运行环境安装程序或手动安装所需依赖。")
        sys.exit(0)

    # 步骤 3：工具包检查
    if os.path.exists("C:/N1/Toolkit") and TOOLKIT_INSTALLED_LOG.exists():
        global_state.current_mode = WorkMode.完整模式
    else:
        global_state.current_mode = WorkMode.受限

    # 步骤 4：更新检查（可选）
    show_update_popup()

    # 步骤 5：进入主程序
    win = MainWindow()
    win.show()
    app.exec()
