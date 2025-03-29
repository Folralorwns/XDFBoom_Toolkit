import sys
import os
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow
from gui.agreement_window import AgreementWindow
from config.global_state import USER_AGREEMENT_LOG_PATH


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
    check_user_agreement()

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
