from pathlib import Path
from enum import Enum

class WorkMode(Enum):
    受限 = "受限"
    完整模式 = "完整模式"

# 当前工具版本
MAIN_VERSION = "V6.0.0"
TOOLKIT_VERSION = "V6.0.0"

# 日志目录
LOG_PATH = Path("C:/N1/Logs")

# 各种状态标志
ENV_DONE_LOG = LOG_PATH / "Env_Done"
TOOLKIT_INSTALLED_LOG = LOG_PATH / "Package_Env_Installed"
USER_AGREEMENT_LOG_PATH = LOG_PATH / f"Agreed_{TOOLKIT_VERSION}"  # ✅ 带版本号标志

# 当前模式（由程序运行中赋值）
current_mode: WorkMode = WorkMode.受限

# 快捷判断函数
def is_env_ready() -> bool:
    return ENV_DONE_LOG.exists()

def is_toolkit_installed() -> bool:
    return TOOLKIT_INSTALLED_LOG.exists()

def is_agreement_accepted() -> bool:
    return USER_AGREEMENT_LOG_PATH.exists()
