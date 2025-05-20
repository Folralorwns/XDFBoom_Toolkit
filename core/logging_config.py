import logging
from pathlib import Path
import sys
from logging.handlers import RotatingFileHandler

# 获取当前程序目录（支持 exe 和 py）
def get_base_dir():
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    else:
        return Path(__file__).resolve().parent

base_dir = get_base_dir()
log_dir = base_dir / "Logs"
log_dir.mkdir(parents=True, exist_ok=True)

log_file_path = log_dir / "runtime.log"

# 日志格式配置
LOG_FORMAT = "[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# 创建日志记录器
logger = logging.getLogger("xdfboom")
logger.setLevel(logging.DEBUG)

# 控制台输出
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))
console_handler.setLevel(logging.INFO)  # 控制台只显示 INFO 及以上级别

# 文件输出（带轮转）
file_handler = RotatingFileHandler(
    log_file_path,
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5,
    encoding='utf-8'
)
file_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))
file_handler.setLevel(logging.DEBUG)  # 文件记录所有级别

# 添加 handler（防止重复）
if not logger.hasHandlers():
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

# 捕捉未处理异常
def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.error("未捕获的异常", exc_info=(exc_type, exc_value, exc_traceback))
    # 可以在这里添加错误报告或通知机制

sys.excepthook = handle_exception
