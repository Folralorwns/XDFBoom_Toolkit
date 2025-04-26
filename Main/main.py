import sys
import os
from gui.FluentMainWindow_v2 import FluentMainWindow
from gui.agreement_window import AgreementWindow
from PySide6.QtWidgets import QApplication
from config.global_state import USER_AGREEMENT_LOG_PATH
from core.logging_config import logger

logger.info("启动程序")

def check_user_agreement():
    if not os.path.exists(USER_AGREEMENT_LOG_PATH):
        app = QApplication(sys.argv)
        agreement_window = AgreementWindow()
        agreement_window.show()
        app.exec()

        if not agreement_window.user_agreed:
            print("用户未同意协议，程序退出。")
            sys.exit(0)


def main():
    if __name__ == "__main__":
        import sys
        app = QApplication(sys.argv)
        window = FluentMainWindow()
        window.show()
        app.exec()


if __name__ == '__main__':
    main()
