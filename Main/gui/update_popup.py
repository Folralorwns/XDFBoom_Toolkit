from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl
from core.version_checker import fetch_update_info, compare_versions
from config.global_state import TOOLKIT_VERSION

UPDATE_CHECK_URL = "https://your-domain.com/version.json"  # ✅ 你上传 JSON 的位置

def show_update_popup(parent=None):
    update_info = fetch_update_info(UPDATE_CHECK_URL)

    if "error" in update_info:
        QMessageBox.warning(parent, "更新检查失败", f"错误：{update_info['error']}")
        return

    latest = update_info.get("最新版本")
    changelog = update_info.get("更新信息", "暂无说明")
    download_url = update_info.get("下载地址", "https://github.com/Folralorwns/XDFBoom_Toolkit")

    if latest and compare_versions(TOOLKIT_VERSION, latest) < 0:
        reply = QMessageBox.information(
            parent,
            f"发现新版本 {latest}",
            f"当前版本：{TOOLKIT_VERSION}\n最新版本：{latest}\n\n更新内容：\n{changelog}\n\n是否现在前往下载？",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            QDesktopServices.openUrl(QUrl(download_url))
    else:
        QMessageBox.information(parent, "无更新", "您已经是最新版本了喵～")
