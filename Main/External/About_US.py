from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QWidget, QCheckBox, QFrame, QPushButton
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve
from Path_Dict import ico_light_theme, ico_dark_theme
import sys

class AboutUsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("关于我们 | About Us")
        self.resize(640, 600)  # 初始化窗口大小
        self.setWindowIcon(QIcon(str(ico_light_theme)))  # 设置窗口图标，可以更改为任何路径
        self.init_ui()

    def init_ui(self):
        # 创建主窗口部件和布局
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)  # 设置主窗口边距

        # 标题图片
        self.label_image = QLabel(self)
        pixmap = QPixmap(str(ico_light_theme))  # 替换为您的图片路径
        self.label_image.setPixmap(pixmap.scaled(800, 200, Qt.AspectRatioMode.KeepAspectRatio))
        self.label_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.label_image)

        # 主标题
        title_label = QLabel("XDFBoom Toolkit Open Source Project")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 26px; font-weight: bold; color: #333;")
        self.main_layout.addWidget(title_label)

        # 添加分隔线
        self.add_separator()

        # 信息部分
        info_section = QLabel(
            '<p style="color: #FF8C00; font-weight: bold;">⚠️ Warning</p>'
            '<p style="margin-left: 10px;">如果您的程序出现了类似闪退的情况，请发送issue<br>此程序暂时不支持V1.2.7及其以上版本的学习机</p>'
            '<p style="color: #32CD32; font-weight: bold;">💡 Tip</p>'
            '<p style="margin-left: 10px;">提示：打包请使用Auto-py-to-exe</p>'
            '<p style="color: #6A5ACD; font-weight: bold;">⚠️ Important</p>'
            '<p style="margin-left: 10px;">最低系统要求：Windows 10 x64</p>'
        )
        info_section.setAlignment(Qt.AlignmentFlag.AlignLeft)
        info_section.setWordWrap(True)
        info_section.setStyleSheet("font-size: 14px;")
        self.main_layout.addWidget(info_section)

        # 添加分隔线
        self.add_separator()

        # 使用方式
        usage_label = QLabel("使用方式")
        usage_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        usage_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 10px;")
        self.main_layout.addWidget(usage_label)

        usage_content = QLabel("开袋即食")
        usage_content.setAlignment(Qt.AlignmentFlag.AlignLeft)
        usage_content.setStyleSheet("font-size: 14px; color: #555; margin-left: 10px;")
        self.main_layout.addWidget(usage_content)

        # 添加分隔线
        self.add_separator()

        # TODO列表
        todo_label = QLabel("WILLTODO")
        todo_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        todo_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 10px;")
        self.main_layout.addWidget(todo_label)

        # 任务列表布局
        todo_layout = QVBoxLayout()
        todo_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        checkbox1 = QCheckBox("编写GUI完全界面")
        checkbox1.setChecked(False)
        checkbox1.setDisabled(True)

        checkbox2 = QCheckBox("更严格的日志分析")
        checkbox2.setChecked(False)
        checkbox2.setDisabled(True)
        
        checkbox3 = QCheckBox("适配V1.2.7及其以上版本")
        checkbox3.setChecked(False) 
        checkbox3.setDisabled(True) 

        checkbox1.setStyleSheet("font-size: 14px; color: #555;")
        checkbox2.setStyleSheet("font-size: 14px; color: #555;")
        checkbox3.setStyleSheet("font-size: 14px; color: #555;")

        todo_layout.addWidget(checkbox1)
        todo_layout.addWidget(checkbox2)
        todo_layout.addWidget(checkbox3)
        self.main_layout.addLayout(todo_layout)

        # 添加分隔线
        self.add_separator()

        # 下载链接
        download_label = QLabel("下载链接")
        download_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        download_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 10px;")
        self.main_layout.addWidget(download_label)

        link_label = QLabel(
            '<a href="https://github.com/Folralorwns/XDFBoom_Toolkit" style="color: #1E90FF; text-decoration: none;">开源界面</a> | '
            '<a href="https://blog.xdfboom.com" style="color: #1E90FF; text-decoration: none;">XDFBoom小站发布地址</a>'
        )
        link_label.setOpenExternalLinks(True)
        link_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        link_label.setStyleSheet("font-size: 14px; margin-left: 10px;")
        self.main_layout.addWidget(link_label)

        # 退出按钮
        self.exit_button = QPushButton("退出")
        self.exit_button.setStyleSheet("""
            background-color: #1E90FF;
            color: white;
            font-size: 16px;
            font-weight: bold;
            border-radius: 10px;
            padding: 10px 20px;
        """)
        self.exit_button.clicked.connect(self.close)

        # 设置初始位置为窗口底部外部
        self.exit_button_animation = QPropertyAnimation(self.exit_button, b"geometry")
        self.exit_button_animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.exit_button_animation.setDuration(1000)
        
        # 动画初始位置在窗口外面
        self.exit_button_animation.setStartValue(QRect(0, self.height(), 180, 50))
        
        # 启动按钮动画
        self.start_exit_button_animation()

        # 添加退出按钮到布局
        self.main_layout.addWidget(self.exit_button)

        # 添加底部空白以增加美观
        self.main_layout.addStretch()

    def start_exit_button_animation(self):
        """ 在原位置基础上移动到窗口底部 """
        window_height = self.height()

        # 计算目标位置
        button_width = 180
        button_height = 50
        x_position = (self.width() - button_width) // 2  # 水平居中
        y_position = window_height - button_height - 20  # 距离底部20像素

        # 更新目标位置
        self.exit_button_animation.setStartValue(QRect(x_position, y_position, button_width, button_height))
        self.exit_button_animation.setEndValue(QRect(x_position, y_position, button_width, button_height))

        # 启动动画
        self.exit_button_animation.start()

    def resizeEvent(self, event):
        """ 在窗口尺寸变化时，保持按钮在底部，动画会在原位置基础上移动 """
        super().resizeEvent(event)  # 调用基类的resizeEvent方法
        self.start_exit_button_animation()  # 在窗口尺寸变化时启动动画

    def add_separator(self):
        """添加一个分隔线"""
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setStyleSheet("color: #CCCCCC; margin: 15px 0;")
        self.main_layout.addWidget(line)
    
def main():
    app = QApplication(sys.argv)
    window = AboutUsWindow()
    window.show()
    app.exec()

def About_US():
    main()

About_US()
