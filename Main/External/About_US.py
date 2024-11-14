from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from .Path_Dict import ico_path  # 假设 ico_path 是图片路径
import sys

class QLabelDemo(QMainWindow):
    """标签示例"""
    def __init__(self) -> None:
        """构造函数"""
        super().__init__()  # 调用父类初始化函数
        self.init_ui()  # 初始化界面

    def init_ui(self):
        """初始化UI界面"""
        self.setWindowTitle("关于我们 | About us")  # 设置标题
        self.resize(640, 480)  # 设置窗体尺寸

        # 创建主控件和布局
        self.mainwidget = QWidget()
        self.vblayout_main = QVBoxLayout()
        self.vblayout_main.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 设置居中对齐
        self.mainwidget.setLayout(self.vblayout_main)
        self.setCentralWidget(self.mainwidget)

        # 读取 README.md 文件内容
        try:
            with open("README.md", "r", encoding="utf-8") as file:
                readme_content = file.read()
        except FileNotFoundError:
            readme_content = "<p>README.md 文件未找到。</p>"

        # 富文本标签
        self.label_richtext = QLabel(self)
        self.label_richtext.setText(f'<p>{readme_content}</p>')  # 设置 README 内容为标签文本
        self.label_richtext.setOpenExternalLinks(True)  # 允许点击富文本中的链接

        # 将富文本标签添加到布局中
        self.vblayout_main.addWidget(self.label_richtext)

        # 图片标签
        self.label_image = QLabel(self)
        pixmap = QPixmap(ico_path)  # 假设 ico_path 是您的图片路径
        self.label_image.setPixmap(pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))  # 设置图片大小并保持长宽比
        self.vblayout_main.addWidget(self.label_image)

        # 设置窗口图标（如果有图标路径）
        self.setWindowIcon(QPixmap(ico_path))

# 应用程序入口
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QLabelDemo()
    window.show()
    sys.exit(app.exec())
