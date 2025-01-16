import os
import time
import subprocess

flash_dir = "C:/N1/Toolkit/ADB/"

def adb(config):
    adbuse = os.path.join(flash_dir, 'adb.exe ' + config)
    subprocess.run(adbuse, shell=True)

def adb_shell(config):
    adbshell = os.path.join(flash_dir, 'adb.exe shell ' + config)
    subprocess.run(adbshell, shell=True)

def adb_connection_check():
    while True:
        devices_cmd = subprocess.Popen([os.path.join(flash_dir, 'adb.exe'), 'devices'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        Device_Manager, _ = devices_cmd.communicate()
        Device_Manager = Device_Manager.decode('utf-8')
        
        if "XDFN1" in Device_Manager and "unauthorized" not in Device_Manager:
            print("[状态] ADB设备已接入")
            return "Connected"
        else:
            print("请打开USB调试并连接学习机")
            print("正在检测adb设备...")
            time.sleep(1)

def fastboot(config):
    fb_use = os.path.join(flash_dir,'fastboot.exe ' + config)
    subprocess.run(fb_use, shell=True)

def fastboot_connection_check():
    while True:
        devices_bootloader = subprocess.Popen([os.path.join(flash_dir, 'fastboot.exe'), 'devices'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        Device_Reader, _ = devices_bootloader.communicate()
        Device_Reader = Device_Reader.decode('utf-8')
        print(Device_Reader)
        if "XDFN1" in Device_Reader and "fastboot" in Device_Reader:
            print("设备已连接")
            return "Connected"
        else:
            os.system('color f9')
            print("请拔线并等待设备重启至bootloader")
            print("正在检测fastboot设备...")
            time.sleep(1)
