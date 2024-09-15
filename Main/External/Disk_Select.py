import string
import os
import psutil
from tabulate import tabulate

def get_drives():
    """
    获取所有可用的盘符及其总空间和剩余空间。

    Returns:
    list: 包含每个盘符及其总空间和剩余空间的元组列表，如 [('C:', total, free), ('D:', total, free), ...]。
    """
    drives = []
    for letter in string.ascii_uppercase:
        drive = f"{letter}:\\"
        if os.path.exists(drive):
            try:
                usage = psutil.disk_usage(drive)
                drives.append((drive, usage.total, usage.free))
            except PermissionError:
                continue
    return drives

def select_drive():
    """
    让用户选择盘符并返回用户选择的盘符。

    Returns:
    str: 用户选择的盘符，如 'C:', 'D:', 等。
    """
    drives = get_drives()
    
    if not drives:
        print("未找到任何可用的盘符。")
        return None
    
    drive_data = []
    for idx, (drive, total, free) in enumerate(drives, start=1):
        drive_data.append([idx, drive, f"{total // (2**30)} GB", f"{free // (2**30)} GB"])

    print(tabulate(drive_data, headers=['序号', '盘符', '总空间', '剩余空间'],tablefmt='fancy_grid'))

    while True:
        try:
            choice = int(input("请选择您要解压到目标盘符(填序号): "))
            if 1 <= choice <= len(drives):
                return drives[choice - 1][0]
            else:
                print("请选择有效的序号。")
        except ValueError:
            print("请输入一个有效的序号。")
