import sys
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize, QTimer
from PySide6.QtGui import QPainter, QColor
from qfluentwidgets import (
    CardWidget, StrongBodyLabel, SubtitleLabel, PrimaryPushButton, 
    FluentIcon, FlowLayout, ScrollArea, ProgressBar, IndeterminateProgressBar
)

class HomePage(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('homePage')
        self.setWidgetResizable(True)
        
        # 主窗口部件
        self.scrollWidget = QWidget()
        self.setWidget(self.scrollWidget)
        
        self.layout = QVBoxLayout(self.scrollWidget)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)

        # 顶部大标题
        self.title_label = StrongBodyLabel("XDFBoom Toolkit")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title_label)

        # 添加加载进度条
        self.progressBar = IndeterminateProgressBar()
        self.progressBar.setVisible(False)
        self.layout.addWidget(self.progressBar)

        # 使用FlowLayout实现响应式布局
        self.flowLayout = FlowLayout()
        self.flowLayout.setSpacing(20)
        self.flowLayout.setContentsMargins(0, 0, 0, 0)
        self.layout.addLayout(self.flowLayout)

        # 显示加载动画
        self.show_loading_animation()

        # 延迟加载卡片，避免界面卡顿
        QTimer.singleShot(100, self.load_cards)

    def show_loading_animation(self):
        self.progressBar.setVisible(True)
        QTimer.singleShot(1000, lambda: self.progressBar.setVisible(False))

    def load_cards(self):
        # 添加功能卡片
        self.add_card(
            "刷机工具",
            "MTK/高通刷机工具",
            FluentIcon.SETTING,
            "mtk_flash"
        )
        self.add_card(
            "ADB工具",
            "Android调试工具",
            FluentIcon.COMMAND_PROMPT,
            "adb_tools"
        )
        self.add_card(
            "设置中心",
            "应用设置",
            FluentIcon.SETTING,
            "settings"
        )

    def add_card(self, title, subtitle, icon, route):
        card = CardWidget()
        card.setFixedSize(300, 200)
        
        # 卡片布局
        card_layout = QVBoxLayout(card)
        card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.setSpacing(10)
        
        # 图标
        icon_label = icon
        icon_label.setFixedSize(48, 48)
        card_layout.addWidget(icon_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # 标题
        title_label = StrongBodyLabel(title)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(title_label)
        
        # 副标题
        subtitle_label = SubtitleLabel(subtitle)
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(subtitle_label)
        
        # 按钮
        button = PrimaryPushButton("进入")
        button.setFixedWidth(120)
        button.clicked.connect(lambda: self.parent().switch_to(route))
        card_layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # 添加动画效果
        self.add_card_animation(card)
        
        # 添加到流式布局
        self.flowLayout.addWidget(card)

        # 添加悬停效果
        card.enterEvent = lambda e: self.card_hover_enter(card)
        card.leaveEvent = lambda e: self.card_hover_leave(card)

    def card_hover_enter(self, card):
        animation = QPropertyAnimation(card, b"geometry")
        animation.setDuration(200)
        animation.setEasingCurve(QEasingCurve.OutBack)
        
        rect = card.geometry()
        rect.setHeight(rect.height() + 10)
        rect.setWidth(rect.width() + 10)
        rect.moveCenter(card.geometry().center())
        
        animation.setEndValue(rect)
        animation.start()

    def card_hover_leave(self, card):
        animation = QPropertyAnimation(card, b"geometry")
        animation.setDuration(200)
        animation.setEasingCurve(QEasingCurve.OutBack)
        
        rect = card.geometry()
        rect.setHeight(rect.height() - 10)
        rect.setWidth(rect.width() - 10)
        rect.moveCenter(card.geometry().center())
        
        animation.setEndValue(rect)
        animation.start()

    def add_card_animation(self, card):
        # 设置初始透明度
        card.setGraphicsEffect(None)
        card.setWindowOpacity(0)
        
        # 创建渐入动画
        opacity_animation = QPropertyAnimation(card, b"windowOpacity")
        opacity_animation.setDuration(500)
        opacity_animation.setStartValue(0)
        opacity_animation.setEndValue(1)
        opacity_animation.setEasingCurve(QEasingCurve.OutCubic)
        
        # 创建缩放动画
        scale_animation = QPropertyAnimation(card, b"geometry")
        scale_animation.setDuration(500)
        scale_animation.setEasingCurve(QEasingCurve.OutBack)
        
        start_rect = card.geometry()
        start_rect.setHeight(0)
        scale_animation.setStartValue(start_rect)
        scale_animation.setEndValue(card.geometry())
        
        # 启动动画
        opacity_animation.start()
        scale_animation.start()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # 根据窗口大小调整卡片大小
        width = self.width()
        if width < 800:
            card_width = 280
        elif width < 1200:
            card_width = 300
        else:
            card_width = 320
            
        for i in range(self.flowLayout.count()):
            widget = self.flowLayout.itemAt(i).widget()
            if isinstance(widget, CardWidget):
                widget.setFixedWidth(card_width)
