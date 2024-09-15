import os
import threading
import time
import requests
import logging
import sys
import shutil
from .Decompressor import Unzip
from PySide6.QtCore import QThread, Signal, QTimer, Qt
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QFont, QColor, QIcon, QPalette, QPainter, QPen
from PySide6.QtCore import QRectF

# 配置日志
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class CircularProgressBar(QWidget):
    def __init__(self, max_value=100):
        super().__init__()
        self.value = 0
        self.target_value = 0
        self.max_value = max_value
        self.setMinimumSize(240, 240)
        self.setMaximumSize(240, 240)
        
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.perform_animation)
        self.animation_timer.start(20)

    def set_value(self, value):
        self.target_value = min(value, self.max_value)
        if not self.animation_timer.isActive():
            self.animation_timer.start()

    def perform_animation(self):
        increment = max(1, int(abs(self.target_value - self.value) * 0.1))

        if self.value < self.target_value:
            self.value += increment
            if self.value > self.target_value:
                self.value = self.target_value
        elif self.value > self.target_value:
            self.value -= increment
            if self.value < self.target_value:
                self.value = self.target_value

        self.update()

        if self.value == self.target_value:
            self.animation_timer.stop()

    def paintEvent(self, event):
        painter = QPainter(self)
        if not painter.isActive():
            return

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor(255, 255, 255))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(0, 0, self.width(), self.height())

        pen = QPen(QColor(240, 240, 240), 20)
        painter.setPen(pen)
        painter.drawArc(QRectF(20, 20, 200, 200), 0, 360 * 16)

        pen.setColor(QColor(102, 204, 255))
        painter.setPen(pen)
        angle = int(360 * (self.value / self.max_value) * 16)
        painter.drawArc(QRectF(20, 20, 200, 200), 90 * 16, -angle)

        font = QFont("Microsoft YaHei", 28, QFont.Weight.Bold)
        painter.setFont(font)
        painter.setPen(QPen(Qt.GlobalColor.black))
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, f"{int(self.value)}%")

        painter.end()

class DownloadThread(QThread):
    update_progress = Signal(int)
    download_complete = Signal()
    download_failed = Signal(str)

    def __init__(self, download_url, filename, num_threads=4):
        super().__init__()
        self.download_url = download_url
        self.filename = filename
        self.num_threads = num_threads
        self.total_size = 0
        self.downloaded_size = 0
        self.chunk_size = 0
        self.stop_update = False

    def run(self):
        try:
            resp = requests.get(self.download_url, stream=True)
            resp.raise_for_status()

            self.total_size = int(resp.headers.get('content-length', 0))
            self.chunk_size = (self.total_size // self.num_threads) + 1

            logging.info(f"Total size to download: {self.total_size} bytes")

            def download_chunk(start, end):
                headers = {'Range': f'bytes={start}-{end}'}
                chunk_resp = requests.get(self.download_url, headers=headers, stream=True)
                chunk_resp.raise_for_status()
                chunk_data = chunk_resp.content
                with open(self.filename, 'r+b') as file:
                    file.seek(start)
                    file.write(chunk_data)
                downloaded_chunk_size = len(chunk_data)
                self.downloaded_size += downloaded_chunk_size

                progress = int((self.downloaded_size / self.total_size) * 100)
                logging.debug(f"Downloaded chunk: {downloaded_chunk_size} bytes, progress: {progress}%")
                self.update_progress.emit(progress)

            with open(self.filename, 'wb') as file:
                file.write(b'\0' * self.total_size)

            threads = []
            for i in range(self.num_threads):
                start = i * self.chunk_size
                end = min((i + 1) * self.chunk_size - 1, self.total_size - 1)
                thread = threading.Thread(target=download_chunk, args=(start, end))
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()

            self.stop_update = True
            logging.info("Download complete")
            self.download_complete.emit()

        except requests.exceptions.RequestException as e:
            self.stop_update = True
            logging.error(f"Request exception: {e}")
            self.download_failed.emit(f"下载失败: {e}")
        except IOError as e:
            self.stop_update = True
            logging.error(f"I/O error: {e}")
            self.download_failed.emit(f"文件写入失败: {e}")

class DownloadApp(QWidget):
    def __init__(self, download_url, filename):
        super().__init__()

        self.download_url = download_url
        self.filename = filename

        self.setWindowTitle("下载进度条示例")
        self.setGeometry(500, 200, 400, 400)

        # 隐藏窗口边框
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # 设置窗口背景色为白色
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(255, 255, 255))
        self.setPalette(palette)

        self.setWindowIcon(QIcon("path_to_icon"))  # 替换为实际图标路径

        self.progressbar = CircularProgressBar()
        self.size_label = QLabel("已下载: 0 / 0 MB")
        self.speed_label = QLabel("速度: 0 MB/s")
        self.time_label = QLabel("总时间: 0 s")
        self.elapsed_label = QLabel("已用时间: 0 s")
        self.status_label = QLabel("")

        for label in [self.size_label, self.speed_label, self.time_label, self.elapsed_label, self.status_label]:
            label.setFont(QFont("Microsoft YaHei", 14))
            label.setStyleSheet("color: black;")

        self.button = QPushButton("开始下载")
        self.button.setStyleSheet("""
            QPushButton {
                background-color: #66ccff;
                color: white;
                font-size: 16px;
                border-radius: 10px;
                padding: 8px;
                font-family: "Microsoft YaHei";
            }
            QPushButton:pressed {
                background-color: #4da6ff;
            }
        """)
        self.button.setEnabled(False)
        self.button.setText("正在下载...")

        layout = QVBoxLayout()
        layout.addWidget(self.progressbar, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.size_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.speed_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.time_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.elapsed_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        self.setLayout(layout)

        self.start_time = time.time()
        self.download_thread = DownloadThread(self.download_url, self.filename)
        self.download_thread.update_progress.connect(self.update_progress)
        self.download_thread.download_complete.connect(self.download_complete)
        self.download_thread.download_failed.connect(self.download_failed)

        self.ui_timer = QTimer(self)
        self.ui_timer.timeout.connect(self.force_update_ui)
        self.ui_timer.start(100)  # 每100毫秒更新一次UI

        self.start_download()

    def start_download(self):
        self.start_time = time.time()
        self.download_thread.start()

    def force_update_ui(self):
        if self.download_thread.stop_update:
            self.ui_timer.stop()
        else:
            if self.download_thread.total_size > 0:
                progress = (self.download_thread.downloaded_size / self.download_thread.total_size) * 100
                self.update_progress(progress)
            else:
                progress = 0

    def update_progress(self, progress):
        self.progressbar.set_value(progress)

        # 已下载大小
        downloaded_size_mb = self.download_thread.downloaded_size / (1024 * 1024)
        total_size_mb = self.download_thread.total_size / (1024 * 1024)

        # 时间计算
        current_time = time.time()
        elapsed_time = current_time - self.start_time

        # 速度计算（使用已下载大小除以总时间）
        speed = (downloaded_size_mb / elapsed_time) if elapsed_time > 0 else 0

        # 更新UI上的标签
        self.size_label.setText(f"已下载: {downloaded_size_mb:.2f} / {total_size_mb:.2f} MB")
        self.speed_label.setText(f"速度: {speed:.2f} MB/s")
        self.time_label.setText(f"总时间: {elapsed_time:.2f} s")
        self.elapsed_label.setText(f"已用时间: {elapsed_time:.2f} s")

    def download_complete(self):
        self.status_label.setText("下载完成")
        self.button.setEnabled(True)
        self.button.setText("下载完成")
        QTimer.singleShot(3000, self.close)  # 1秒后关闭窗口

    def download_failed(self, error_message):
        self.status_label.setText(f"下载失败: {error_message}")
        self.button.setEnabled(True)
        self.button.setText("重试")

def main(download_url, filename):
    app = QApplication(sys.argv)
    window = DownloadApp(download_url, filename) 
    window.show() 
    sys.exit(app.exec())


def Down_and_Dec(type,download_url,filename):
    main(download_url, filename)
    if type == 'image':
        Unzip(filename,'C:/N1/Toolkit/ADB/Image/')
        shutil.move(filename,'C:/N1/Cache')
    if type == 'tools':
        Unzip(filename,'C:/N1/')
        os.remove(filename)
    