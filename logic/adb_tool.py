
import subprocess
import time
from core.logging_config import logger
from core.path_manager import ADB_PATH


def run_adb_command(command: list, log_callback=None):
    """
    统一执行 ADB 命令，带日志和异常捕获
    """
    try:
        logger.info(f"执行 ADB 命令: {' '.join(command)}")
        if log_callback:
            log_callback(f"执行 ADB 命令: {' '.join(command)}")

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()

        if stdout:
            for line in stdout.strip().splitlines():
                logger.info(line)
                if log_callback:
                    log_callback(line)

        if stderr:
            for line in stderr.strip().splitlines():
                logger.warning(line)
                if log_callback:
                    log_callback(line)

    except Exception as e:
        logger.exception(f"执行 ADB 命令出错: {e}")
        if log_callback:
            log_callback(f"执行 ADB 命令出错: {e}")


def check_adb_connection(log_callback=None):
    """
    检查是否有设备连接
    """
    cmd = [str(ADB_PATH), 'devices']
    try:
        logger.info("检查 ADB 设备连接状态")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        output = result.stdout.strip()
        if 'device' in output and not 'unauthorized' in output:
            msg = "ADB 设备已连接 ✅"
            logger.info(msg)
            if log_callback:
                log_callback(msg)
            return True
        else:
            msg = "ADB 未连接或未授权 ❌"
            logger.warning(msg)
            if log_callback:
                log_callback(msg)
            return False
    except Exception as e:
        msg = f"检查 ADB 连接出错: {e}"
        logger.exception(msg)
        if log_callback:
            log_callback(msg)
        return False


def fix_network_issue(log_callback=None):
    """
    修复 Android captive_portal 网络异常
    """
    logger.info("开始修复网络 × 和 ！ 问题")
    if log_callback:
        log_callback("开始修复网络 × 和 ！ 问题")

    commands = [
        [str(ADB_PATH), 'shell', 'settings delete global captive_portal_http_url'],
        [str(ADB_PATH), 'shell', 'settings delete global captive_portal_https_url'],
        [str(ADB_PATH), 'shell', 'settings put global captive_portal_http_url http://connect.rom.miui.com/generate_204'],
        [str(ADB_PATH), 'shell', 'settings put global captive_portal_https_url https://connect.rom.miui.com/generate_204']
    ]

    for cmd in commands:
        run_adb_command(cmd, log_callback)

    restart_adb_server(log_callback)


def restart_adb_server(log_callback=None):
    """
    重启 ADB server
    """
    logger.info("重启 ADB Server")
    if log_callback:
        log_callback("重启 ADB Server")
    
    cmds = [
        [str(ADB_PATH), 'kill-server'],
        [str(ADB_PATH), 'start-server']
    ]

    for cmd in cmds:
        run_adb_command(cmd, log_callback)
