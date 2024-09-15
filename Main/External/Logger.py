import logging
import os
from datetime import datetime

# 获取当前时间作为前缀
now = datetime.now()
timestamp = now.strftime('%Y%m%d_%H%M%S')
LOG_FILE = f'log_{timestamp}.tklog'
LOG_DIR = 'C:/N1/Logs/'

# 确保日志目录存在
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_PATH = os.path.join(LOG_DIR, LOG_FILE)

# 配置日志记录器
logging.basicConfig(
    level=logging.DEBUG,  # 设置日志级别为 DEBUG，记录所有级别的日志
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_PATH, encoding='utf-8'),  # 写入日志到带有时间戳的文件
        logging.StreamHandler()  # 同时输出到控制台（可选）
    ]
)

# 获取记录器
logger = logging.getLogger(__name__)

def log_debug(message):
    """记录调试信息"""
    logger.debug(message)

def log_info(message):
    """记录普通信息"""
    logger.info(message)

def log_warning(message):
    """记录警告信息"""
    logger.warning(message)

def log_error(message):
    """记录错误信息"""
    logger.error(message)

def log_critical(message):
    """记录严重错误信息"""
    logger.critical(message)

def Log():
    log_debug("这是一个调试信息")

