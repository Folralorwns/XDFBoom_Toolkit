# core/path_manager.py
from pathlib import Path
import sys
import os

def is_frozen():
    """判断是否为 Nuitka / PyInstaller 打包后的可执行文件"""
    return hasattr(sys, "_MEIPASS") or getattr(sys, "frozen", False)

def base_path():
    """获取程序运行时的根路径"""
    if is_frozen():
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent  # 回到项目根目录

# === 路径区域 ===
BASE = base_path()
RES = BASE / "resources"

# 图标
def get_icon_path(theme="light"):
    if theme == "dark":
        return RES / "ico" / "logo_dark_theme.png"
    return RES / "ico" / "logo_light_theme.png"

# 协议文件f
AGREEMENT_USER = RES / "Agreements" / "XDFBoom_Software.txt"
AGREEMENT_OPEN = RES / "Agreements" / "AGPLv3.txt"

# 安装器、驱动
PYTHON_INSTALLER = RES / "Drivers" / "Python_3.11.9.exe"
SEVEN_ZIP_PATH = RES / "Env_Programs" / "7za.exe"

# Markdown
MARKDOWN_PATH = RES / "Markdown" / "README.md"

# 外部脚本路径
mtk_script_path = Path("C:/N1/Toolkit/tools/mtk.py")  # 固定刷机路径
