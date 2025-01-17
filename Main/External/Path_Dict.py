from pathlib import Path

# 获取当前文件的路径
Now_Path = Path(__file__).resolve().parent

# 如果路径中包含"External"，则移除它
if 'External' in Now_Path.parts:
    Now_Path = Path(*[part for part in Now_Path.parts if part != 'External'])

# 构建各个文件路径
ico_dark_theme = Now_Path / 'ico' / 'logo_dark_theme.png'
ico_light_theme = Now_Path / 'ico' / 'logo_light_theme.png'
Python_Installer_Path = Now_Path / 'Drivers' / 'Python_3.11.9.exe'
Env_7zip_path = Now_Path / 'Env_Programs' / '7za.exe'
Agreement_Path_Open_Source = Now_Path / 'Agreements' / 'AGPLv3.txt'
Agreement_Path_User = Now_Path / 'Agreements' / 'XDFBoom_Software.txt'
Markdown_Path = Now_Path / 'Markdown' / 'README.md'

mtk_path = Path("C:/N1/Toolkit/tools/mtk")
