import os
import platform

def prepare_screen():
    if platform.system() == 'Windows':
        os.system('cls')  # 清屏
        os.system('color f9')  # 设置颜色
    else:
        print("\033[H\033[J", end='')  # 适用于类Unix系统的清屏方法
