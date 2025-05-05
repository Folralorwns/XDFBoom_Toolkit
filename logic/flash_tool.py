
import subprocess
import os
from core.path_manager import MTKCLIENT_DIR
from core.logging_config import logger


def run_flash_script(script_name: str, log_callback=None):
    """
    执行MTK刷机脚本
    :param script_name: 脚本文件名（如 example.xml）
    :param log_callback: 日志回调函数（通常是页面上的append_log）
    """
    logger.info(f"开始执行刷机脚本: {script_name}")
    if log_callback:
        log_callback(f"[刷机脚本] 开始执行：{script_name}")

    try:
        os.chdir(MTKCLIENT_DIR)
        command = ["python", "mtk.py", "xml", f"examples/{script_name}"]
        _run_subprocess(command, log_callback)

    except Exception as e:
        error_msg = f"[刷机脚本] 执行异常：{e}"
        logger.exception(error_msg)
        if log_callback:
            log_callback(error_msg)


def run_custom_mtk_command(short_command: str, log_callback=None):
    """
    执行自定义MTK命令
    :param short_command: 用户输入的短指令（如 e userdata）
    :param log_callback: 日志回调函数
    """
    logger.info(f"开始执行自定义MTK命令: {short_command}")
    if log_callback:
        log_callback(f"[自定义命令] 开始执行：{short_command}")

    try:
        os.chdir(MTKCLIENT_DIR)
        parts = short_command.strip().split()
        if not parts:
            raise ValueError("输入的命令不能为空")

        command = ["python", "mtk.py"] + parts
        _run_subprocess(command, log_callback)

    except Exception as e:
        error_msg = f"[自定义命令] 执行异常：{e}"
        logger.exception(error_msg)
        if log_callback:
            log_callback(error_msg)


def _run_subprocess(command: list, log_callback=None):
    """
    封装子进程执行流程
    :param command: 完整命令列表
    :param log_callback: 日志回调函数
    """
    logger.info(f"执行命令：{' '.join(command)}")
    if log_callback:
        log_callback(f"[命令] {' '.join(command)}")

    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    # 实时输出stdout
    for line in process.stdout:
        line = line.strip()
        if line:
            logger.info(line)
            if log_callback:
                log_callback(line)

    # 检查stderr
    stderr = process.stderr.read().strip()
    if stderr:
        logger.error(stderr)
        if log_callback:
            log_callback(f"[错误] {stderr}")

    retcode = process.poll()
    if retcode == 0:
        logger.info("[完成] 命令执行成功 ✅")
        if log_callback:
            log_callback("[完成] 命令执行成功 ✅")
    else:
        logger.error(f"[错误] 命令执行失败，返回码 {retcode}")
        if log_callback:
            log_callback(f"[错误] 命令执行失败，返回码 {retcode}")
