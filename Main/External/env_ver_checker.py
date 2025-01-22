import os
import time
import platform
import sys
import subprocess
from PySide6.QtWidgets import QApplication, QFileDialog
from .Path_Dict import Now_Path,Python_Installer_Path

workmode = None
Env_Check = os.path.exists('C:/N1/Logs/Env_Done')

def install_python(Python_installer_path):
    try:
        # 执行安装程序并捕获输出
        result = subprocess.run(
            [Python_installer_path, '/passive', 'InstallAllUsers=1', 'PrependPath=1'],
            capture_output=True,  # 捕获标准输出和标准错误
            text=True,            # 以文本模式处理输出
            check=True            # 如果命令失败，则引发异常
        )
        # 打印标准输出和标准错误
        print("安装程序输出：")
        print(result.stdout)
        if result.stderr:
            print("安装程序错误输出：")
            print(result.stderr)

    except subprocess.CalledProcessError as e:
        print(f"安装失败: {e}")

def checker(config):
    if config == 1:
        Bitcheck = platform.architecture()
        Vcheck = platform.version()
        if "64bit" in Bitcheck and "10.0" in Vcheck:
            pass
        else:
            print("您的设备不支持！请确认您的电脑系统为Windows10 64bit及以上！")
            time.sleep(3)
            exit(1)
    
    elif config == 2:
        selected_drive = 'C:/'
        if selected_drive:
            folders_to_create = [
                os.path.join(selected_drive, 'N1'),
                os.path.join(selected_drive, 'N1', 'Logs'),
                os.path.join(selected_drive, 'N1', 'Cache'),
                os.path.join(selected_drive, 'N1', 'Cache', 'Images'),
                os.path.join(selected_drive, 'N1', 'Cache', 'Toolkit')
            ]
            for folder_path in folders_to_create:
                if not os.path.exists(folder_path):
                    os.mkdir(folder_path)
        else:
            print("没有选择任何驱动器")
    
    if config == 3:
        if not Env_Check:
            os.chdir(Now_Path)
            print("正在打开adb驱动")
            subprocess.run(['pnputil', '-i', '-a', './Drivers/ADB/android_winusb.inf'], check=True)
            print("正在打开mtk驱动")
            # 执行SP_Driver.exe
            subprocess.run(['.\\Drivers\\SP_Driver.exe', '/sp-', '/verysilent'], check=True)
            # 获取绝对路径
            msi_path = os.path.abspath('.\\Drivers\\mtk.msi')
            # 执行mtk.msi
            subprocess.run(['msiexec', '/i', msi_path, '/quiet', '/norestart'], check=True)
            install_python(Python_Installer_Path)
            print("正在安装pip库")
            os.system('pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/')
            os.system('pip install -r C:\\N1\\Toolkit\\tools\\requirements.txt')
            # 创建或更新文件
            open('C:/N1/Logs/Env_Done', 'w+').close()
            print("驱动安装成功，按任意键使电脑重启")
            input("按任意键继续...")
            print("正在重启")
            time.sleep(1)
            # 进行系统重启
            subprocess.run(['shutdown', '-r', '-t', '3'], check=True)
            exit()

"""1：系统版本检测"""
"""2：目录检测"""
"""3：环境检测"""
