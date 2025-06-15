import os
import time
import subprocess
from core.path_manager import RES,ADB_PATH,FASTBOOT_PATH  # resources 根目录

def adb(command: str):
    """执行 adb 命令（非 shell）"""
    full_cmd = f'"{ADB_PATH}" {command}'
    print(f"[ADB] {full_cmd}")
    subprocess.run(full_cmd, shell=True)

def adb_shell(shell_command: str):
    """执行 adb shell 命令"""
    full_cmd = f'"{ADB_PATH}" shell {shell_command}'
    print(f"[ADB Shell] {full_cmd}")
    subprocess.run(full_cmd, shell=True)

def adb_connection_check():
    """循环检测 adb 设备接入"""
    while True:
        process = subprocess.Popen([str(ADB_PATH), 'devices'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, _ = process.communicate()
        decoded = output.decode('utf-8')
        if "XDFN1" in decoded and "unauthorized" not in decoded:
            print("[状态] ADB 设备已连接")
            return True
        else:
            print("请开启 USB 调试并连接学习机，正在检测 ADB 设备...")
            time.sleep(1)

def fastboot(command: str):
    """执行 fastboot 命令"""
    full_cmd = f'"{FASTBOOT_PATH}" {command}'
    print(f"[Fastboot] {full_cmd}")
    subprocess.run(full_cmd, shell=True)

def fastboot_connection_check():
    """循环检测 fastboot 模式接入"""
    while True:
        process = subprocess.Popen([str(FASTBOOT_PATH), 'devices'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, _ = process.communicate()
        decoded = output.decode('utf-8')
        print(decoded)
        if "XDFN1" in decoded and "fastboot" in decoded:
            print("[状态] Fastboot 设备已连接")
            return True
        else:
            print("请拔线并等待设备重启至 bootloader，正在检测 Fastboot...")
            time.sleep(1)
