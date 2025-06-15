from pathlib import Path
from enum import Enum
import json
from typing import Dict, Any
from core.logging_config import logger

class WorkMode(Enum):
    受限 = "受限"
    完整模式 = "完整模式"

# 当前工具版本
MAIN_VERSION = "V6.0.0"
TOOLKIT_VERSION = "V6.0.0"

# 配置目录
CONFIG_DIR = Path.home() / ".xdfboom"
CONFIG_DIR.mkdir(parents=True, exist_ok=True)

# 配置文件路径
CONFIG_FILE = CONFIG_DIR / "config.json"

# 日志目录
LOG_PATH = CONFIG_DIR / "Logs"
LOG_PATH.mkdir(parents=True, exist_ok=True)

# 各种状态标志
ENV_DONE_LOG = LOG_PATH / "Env_Done"
TOOLKIT_INSTALLED_LOG = LOG_PATH / "Package_Env_Installed"
USER_AGREEMENT_LOG_PATH = LOG_PATH / f"Agreed_{TOOLKIT_VERSION}"

# 默认配置
DEFAULT_CONFIG = {
    "work_mode": "受限",
    "theme": "light",
    "language": "zh_CN",
    "auto_update": True,
    "log_level": "INFO"
}

# 当前模式（由程序运行中赋值）
current_mode: WorkMode = WorkMode.受限

# 配置管理
def load_config() -> Dict[str, Any]:
    """加载配置文件"""
    try:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # 验证配置完整性
                for key, value in DEFAULT_CONFIG.items():
                    if key not in config:
                        config[key] = value
                return config
    except Exception as e:
        logger.error(f"加载配置文件失败: {e}")
    return DEFAULT_CONFIG.copy()

def save_config(config: Dict[str, Any]) -> bool:
    """保存配置文件"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        logger.error(f"保存配置文件失败: {e}")
        return False

# 快捷判断函数
def is_env_ready() -> bool:
    return ENV_DONE_LOG.exists()

def is_toolkit_installed() -> bool:
    return TOOLKIT_INSTALLED_LOG.exists()

def is_agreement_accepted() -> bool:
    return USER_AGREEMENT_LOG_PATH.exists()

# 初始化配置
config = load_config()
current_mode = WorkMode(config.get("work_mode", "受限"))
