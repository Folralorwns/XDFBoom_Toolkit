from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QObject, Signal, QTimer
from qfluentwidgets import Theme, setTheme, isDarkTheme


class ThemeSwitcher(QObject):
    """兼容所有版本的动画主题切换器（不依赖 FluentThemeManager）"""
    switchingFinished = Signal()

    def __init__(self, window, duration=300):
        super().__init__()
        self.window = window
        self.duration = duration
        self.anim = QPropertyAnimation(window, b"windowOpacity")
        self.anim.setDuration(self.duration)
        self.anim.setEasingCurve(QEasingCurve.InOutQuad)
        self.anim.finished.connect(self._on_fade_out_finished)
        self._next_theme = Theme.DARK

    def toggle(self):
        # 判断当前主题并设置下一个
        self._next_theme = Theme.LIGHT if isDarkTheme() else Theme.DARK
        self._fade_out()

    def _fade_out(self):
        self.anim.stop()
        self.anim.setStartValue(1.0)
        self.anim.setEndValue(0.0)
        self.anim.start()

    def _on_fade_out_finished(self):
        setTheme(self._next_theme)
        QTimer.singleShot(10, self._fade_in)

    def _fade_in(self):
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.start()
        self.switchingFinished.emit()
