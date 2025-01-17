from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QWidget, QCheckBox, QFrame, QPushButton
from PySide6.QtGui import QPixmap, QColor, QIcon
from PySide6.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve
from Path_Dict import ico_light_theme,ico_dark_theme
import sys

class AboutUsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("关于我们 | About Us")
        self.resize(640, 600)
        self.is_light_mode = True  # 默认是明亮模式
        self.init_ui()

    def init_ui(self):
        # 创建主窗口部件和布局
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)  # 设置主窗口边距

        # 标题图片
        self.label_image = QLabel(self)
        self.change_image()  # 根据当前模式切换图片
        self.label_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.label_image)

        # 主标题
        self.title_label = QLabel("XDFBoom Toolkit Open Source Project")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 26px; font-weight: bold; color: #333;")
        self.main_layout.addWidget(self.title_label)

        # 添加分隔线
        self.add_separator()

        # 信息部分
        info_section = QLabel(
            '<p style="color: #FF8C00; font-weight: bold;">⚠️ Warning</p>'
            '<p style="margin-left: 10px;">如果您的程序出现了类似闪退的情况，请发送issue</p>'
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

        checkbox2 = QCheckBox("更严酷的调试和过滤机制")
        checkbox2.setChecked(False)
        checkbox2.setDisabled(True)
        
        checkbox3 = QCheckBox("底层重写")
        checkbox3.setChecked(True) 
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

        # 亮度切换按钮（左侧或右侧的小按钮）
        self.brightness_button = QPushButton("🌞")
        self.brightness_button.setStyleSheet("""
            background-color: transparent;
            font-size: 24px;
            border: none;
            padding: 5px;
        """)
        self.brightness_button.clicked.connect(self.toggle_theme)
        self.main_layout.addWidget(self.brightness_button, alignment=Qt.AlignmentFlag.AlignRight)  # 将按钮放置在右侧

        # 退出按钮（小按钮，右下角）
        self.exit_button = QPushButton("退出")
        self.exit_button.setStyleSheet("""
            background-color: #1E90FF;
            color: white;
            font-size: 12px;
            font-weight: bold;
            border-radius: 10px;
            padding: 5px 10px;
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

        # 初始化背景色和文字颜色动画
        self.bg_animation = QPropertyAnimation(self.main_widget, b"styleSheet")
        self.bg_animation.setDuration(2000)
        self.bg_animation.setEasingCurve(QEasingCurve.InOutQuad)

        # 设置初始的背景样式为明亮
        self.apply_light_theme()

    def start_exit_button_animation(self):
        """ 在原位置基础上移动到窗口底部 """
        window_height = self.height()

        # 计算目标位置
        button_width = 180
        button_height = 50
        x_position = (self.width() - button_width) // 2  # 水平居中
        y_position = window_height - button_height - 20  # 距离底部20像素

        # 更新目标位置
        self.exit_button_animation.setEndValue(QRect(x_position, y_position, button_width, button_height))

        # 启动动画
        self.exit_button_animation.start()

    def resizeEvent(self, event):
        """ 在窗口尺寸变化时，保持按钮在底部，动画会在原位置基础上移动 """
        super().resizeEvent(event)  # 调用基类的resizeEvent方法
        self.start_exit_button_animation()  # 在窗口尺寸变化时启动动画

    def toggle_theme(self):
        """ 切换明亮和暗色主题 """
        if self.is_light_mode:
            self.apply_dark_theme()
        else:
            self.apply_light_theme()
        self.is_light_mode = not self.is_light_mode

    def apply_light_theme(self):
        """ 应用明亮主题 """
        # 明亮模式背景色和文字颜色
        self.bg_animation.setStartValue("background-color: #FFFFFF; color: #333;")
        self.bg_animation.setEndValue("background-color: #FFFFFF; color: #333;")
        self.bg_animation.start()

        self.title_label.setStyleSheet("font-size: 26px; font-weight: bold; color: #333;")
        self.brightness_button.setStyleSheet("""
            background-color: transparent;
            font-size: 24px;
            border: none;
            padding: 5px;
        """)

        self.change_image()

    def apply_dark_theme(self):
        """ 应用暗色主题 """
        # 暗色模式背景色和文字颜色
        self.bg_animation.setStartValue("background-color: #333333; color: #FFFFFF;")
        self.bg_animation.setEndValue("background-color: #333333; color: #FFFFFF;")
        self.bg_animation.start()

        self.title_label.setStyleSheet("font-size: 26px; font-weight: bold; color: #FFFFFF;")
        self.brightness_button.setStyleSheet("""
            background-color: transparent;
            font-size: 24px;
            border: none;
            padding: 5px;
        """)

        self.change_image()

    def change_image(self):
        """ 根据当前主题变化图片 """
        if self.is_light_mode:
            pixmap = QPixmap(ico_light_theme)  # 这里使用你自己的图片路径
        else:
            pixmap = QPixmap(ico_dark_theme)  # 暗色主题的图片路径

        self.label_image.setPixmap(pixmap.scaled(800, 200, Qt.AspectRatioMode.KeepAspectRatio))

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
