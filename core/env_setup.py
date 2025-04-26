import platform
import os
import subprocess
import time
from config.global_state import LOG_PATH, ENV_DONE_LOG
from core.path_manager import PYTHON_INSTALLER, RES

def check_system_compatibility():
    bit = platform.architecture()[0]
    version = platform.version()
    if "64bit" not in bit or "10.0" not in version:
        raise EnvironmentError("系统不兼容：需要 Windows 10 64 位或以上")

def create_n1_structure():
    folders = [
        "C:/N1",
        "C:/N1/Logs",
        "C:/N1/Cache",
        "C:/N1/Cache/Images",
        "C:/N1/Cache/Toolkit"
    ]
    for path in folders:
        os.makedirs(path, exist_ok=True)

def install_python():
    try:
        subprocess.run(
            [str(PYTHON_INSTALLER), '/passive', 'InstallAllUsers=1', 'PrependPath=1'],
            check=True
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Python 安装失败：{e}")

def install_drivers():
    try:
        os.chdir(RES)
        print("安装 ADB 驱动...")
        subprocess.run(['pnputil', '-i', '-a', './Drivers/ADB/android_winusb.inf'], check=True)
        print("安装 MTK 驱动...")
        subprocess.run(['.\\Drivers\\SP_Driver.exe', '/sp-', '/verysilent'], check=True)
        msi_path = os.path.abspath('.\\Drivers\\mtk.msi')
        subprocess.run(['msiexec', '/i', msi_path, '/quiet', '/norestart'], check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"驱动安装失败：{e}")

def install_pip_requirements():
    try:
        os.system('pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/')
        os.system('pip install -r C:\\N1\\Toolkit\\tools\\requirements.txt')
    except Exception as e:
        raise RuntimeError(f"pip 安装失败：{e}")

def write_env_flag():
    ENV_DONE_LOG.parent.mkdir(parents=True, exist_ok=True)
    ENV_DONE_LOG.touch()

def reboot_system():
    print("准备重启电脑...")
    time.sleep(1)
    subprocess.run(['shutdown', '-r', '-t', '3'])

def full_environment_setup():
    check_system_compatibility()
    create_n1_structure()
    install_drivers()
    install_python()
    install_pip_requirements()
    write_env_flag()
