import requests

def fetch_update_info(update_url):
    """
    从云端获取更新信息。

    Returns:
    dict or str: 如果获取到 JSON 格式数据，则返回解析后的字典。
                如果获取到文本格式数据，则直接返回文本内容。
                如果获取失败，则返回空字典 {} 或空字符串 ''。
    """
    
    try:
        response = requests.get(update_url)
        if response.status_code == 200:
            try:
                update_info = response.json()  # 尝试解析为 JSON
                return update_info
            except ValueError:
                update_info = response.text  # 如果无法解析为 JSON，则返回文本内容
                return update_info
        else:
            print(f"获取更新信息失败：HTTP 状态码 {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"获取更新信息失败：{e}")
    
    return {}  # 或 ''

def compare_versions(now_version, lastest_version):
    """
    版本比较函数。比较两个版本号的大小。

    Args:
    version1 (str): 版本号1。
    version2 (str): 版本号2。

    Returns:
    int: 如果 version1 > version2，则返回正数。
         如果 version1 < version2，则返回负数。
         如果 version1 == version2，则返回0。
    """
    version1_parts = [int(part) for part in now_version.split('.')]
    version2_parts = [int(part) for part in lastest_version.split('.')]
    
    for part1, part2 in zip(version1_parts, version2_parts):
        if part1 > part2:
            return 1
        elif part1 < part2:
            return -1
    
    if len(version1_parts) > len(version2_parts):
        return 1
    elif len(version1_parts) < len(version2_parts):
        return -1
    else:
        return 0

def Ver_Checker(update_url):
    update_info = fetch_update_info(update_url)
    if isinstance(update_info, dict):
        print("获取到的更新信息:")
        print(f"版本号: {update_info.get('最新版本')}")
        print(f"更新内容: {update_info.get('更新信息')}")
    elif isinstance(update_info, str):
        print("获取到的更新信息:")
        print(update_info)
    else:
        print("未能获取更新信息。")