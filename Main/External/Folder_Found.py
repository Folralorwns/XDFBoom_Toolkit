import os

def find_specific_folder_in_root(folder_name):
    """
    在每一个分区的根目录下检查特定名称的文件夹，并输出其路径。

    Args:
    folder_name (str): 要查找的文件夹名称。

    Returns:
    list: 包含每个找到的文件夹路径的列表。
    """
    found_folders = []
    for drive in range(ord('A'), ord('Z') + 1):
        drive_letter = chr(drive) + ':\\'
        if os.path.exists(drive_letter):
            try:
                root_folders = next(os.walk(drive_letter))[1]
                if folder_name in root_folders:
                    found_folders.append(os.path.join(drive_letter, folder_name))
            except PermissionError:
                print(f"无法访问 {drive_letter}，权限不足。")

    return found_folders

# 示例用法
if __name__ == "__main__":
    folder_name_to_find = input("请输入要查找的文件夹名称: ")
    found_folders = find_specific_folder_in_root(folder_name_to_find)

    if found_folders:
        print(f"找到的文件夹 '{folder_name_to_find}' 的路径:")
        for folder_path in found_folders:
            print(folder_path)
    else:
        print(f"未找到名称为 '{folder_name_to_find}' 的文件夹。")
