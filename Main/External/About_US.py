from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from Env_Packages import ico_path
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

        # 富文本标签
        self.label_richtext = QLabel(self)
        self.label_richtext.setText(
            '<a style="font-family: Sans Serif; color: #0000EE; font-size: 15pt; text-decoration: none" '
            'href="https://blog.xdfboom.com/about">关于我们 | About us</a>'
        )
        self.label_richtext.setOpenExternalLinks(True)
        self.label_richtext.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.vblayout_main.addWidget(self.label_richtext)

        # 图片标签
        self.label_image = QLabel(self)
        self.label_image.setPixmap(QPixmap(ico_path))
        self.label_image.setIndent(100)
        self.label_image.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.label_image.setToolTip("我们的logo")
        # 关联鼠标滑过和点击事件
        self.label_image.linkHovered.connect(self.link_hovered)
        self.label_image.linkActivated.connect(self.link_action)
        self.vblayout_main.addWidget(self.label_image)

        # 纯文本标签
        self.label_plaintext = QLabel(self)
        self.label_plaintext.setText(
            "本团队由 @folralorwns 于 2023 年 / 1 月 / 12 日正式创建，主要成员有\n"
            "服务器提供者：土拨鼠(file/file2)，yeenjie(blog)\n"
            "网站技术及域名提供者：yeenjie\n"
            "工具包以及教程编写者：folralorwns\n"
            "“XDFBoom Team”或“XDFBoom团队”及其工具包与 新东方教育科技集团有限公司 没有任何关系！\n"
            "XDFBoom Team | XDFBoom 团队©所有"
        )
        self.label_plaintext.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.label_plaintext.setWordWrap(True)  # 允许换行
        self.label_plaintext.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.vblayout_main.addWidget(self.label_plaintext)

    def link_hovered(self, link):
        """链接被鼠标悬停时的处理"""
        print(f"Link hovered: {link}")

    def link_action(self, link):
        """链接被点击时的处理"""
        print(f"Link activated: {link}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QLabelDemo()
    window.show()
    sys.exit(app.exec())
