import subprocess
from .Env_Packages import Env_7zip_path,Now_Path

# 拼接程序路径，使用 os.path.join 来确保路径拼接正确
def Unzip(file_name: str, target_path: str):
    # 如果路径或文件名中包含空格，使用引号包裹
    Unzip_command = f'"{Env_7zip_path}" x "{file_name}" -o"{target_path}"'
    
    # 执行解压命令
    print(Unzip_command)
    subprocess.run(Unzip_command)




