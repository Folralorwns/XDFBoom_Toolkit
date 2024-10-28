#程序
Toolkit = "Toolkit.7z"
Toolkit_link = "https://github.com/Folralorwns/XDFBoom_Toolkit/releases/download/Toolkit_Package/Toolkit.7z"
#GAPPS Android11
ga111 = "crDroid.7z"
ga111url = "https://github.com/Folralorwns/XDFBoom_Toolkit/releases/download/GAPPS_Android11/crDroid.7z"
ga112 = "LineageOS.7z"
ga112url = "https://github.com/Folralorwns/XDFBoom_Toolkit/releases/download/GAPPS_Android11/LineageOS.7z"
ga113 = "DotOS.7z"
ga113url = "https://github.com/Folralorwns/XDFBoom_Toolkit/releases/download/GAPPS_Android11/DotOS.7z"
#GAPPS Android10
ga101 = "HavocOS.7z"
ga101url = "https://github.com/Folralorwns/XDFBoom_Toolkit/releases/download/GAPPS_Android10/HavocOS.7z"
ga102 = "Resurrection_Remix.7z"
ga102url = "https://github.com/Folralorwns/XDFBoom_Toolkit/releases/download/GAPPS_Android10/Resurrection_Remix.7z"
#Vanilla Android 11
va111 = "LineageOS.7z"
va111url = "https://github.com/Folralorwns/XDFBoom_Toolkit/releases/download/Vanillia_Android11/LineageOS.7z"
va112 = "DotOS.7z"
va112url = "https://github.com/Folralorwns/XDFBoom_Toolkit/releases/download/Vanillia_Android11/DotOS.7z"
va113 = "crDroid.7z"
va113url = "https://github.com/Folralorwns/XDFBoom_Toolkit/releases/download/Vanillia_Android11/crDroid.7z"
#Vanilla Android 10
va101 = "LineageOS.7z"
va101url = "https://github.com/Folralorwns/XDFBoom_Toolkit/releases/download/VANILLIA_Android10/LineageOS.7z"
va102 = "HavocOS.7z"
va102url = "https://github.com/Folralorwns/XDFBoom_Toolkit/releases/download/VANILLIA_Android10/HavocOS.7z"
va103 = "Resurrection_Remix.7z"
va103url = "https://github.com/Folralorwns/XDFBoom_Toolkit/releases/download/VANILLIA_Android10/Resurrection_Remix.7z"
#原厂系统包
RP = "Recovery_package.7z"
RPurl = "https://file2.xdfboom.com/d/N1/Recovery_package.7z?sign=MhBwY6WsLYHJT4iVtso3ld_nqe1f29hxSCw-UtPRI8I=:0"

#程序
Toolkit_TEST = "Toolkit.7z"
Toolkit_link_TEST = "http://10.0.0.2:65535/d/N1/Toolkit/Toolkit.7z?sign=LxguVrVs1nqd0nGVcr-z4E6kTTPnYUH9JaNPiMSLhf0=:0"
#GAPPS Android10
ga102_TEST = "Resurrection_Remix.7z"
ga102url_TEST = "http://10.0.0.2:65535/d/N1/Generic_System_Image/GAPPS/Android10/Resurrection_Remix.7z?sign=BaFIL_vv27-Rhyk6dUj5PYe6ENk9QqKg4NgCkwyeaMA=:0"


system_list = [
    {'编号': 1, '系统名称': 'crDroid', '安卓版本': 11, '包含谷歌套件': '是', '下载链接': ga111url, '文件名': ga111},
    {'编号': 2, '系统名称': 'LineageOS', '安卓版本': 11, '包含谷歌套件': '是', '下载链接': ga112url, '文件名': ga112},
    {'编号': 3, '系统名称': 'DotOS', '安卓版本': 11, '包含谷歌套件': '是', '下载链接': ga113url, '文件名': ga113},
    {'编号': 4, '系统名称': 'LineageOS', '安卓版本': 11, '包含谷歌套件': '否', '下载链接': va111url, '文件名': va111},
    {'编号': 5, '系统名称': 'DotOS', '安卓版本': 11, '包含谷歌套件': '否', '下载链接': va112url, '文件名': va112},
    {'编号': 6, '系统名称': 'crDroid', '安卓版本': 11, '包含谷歌套件': '否', '下载链接': va113url, '文件名': va113},
    {'编号': 7, '系统名称': 'HavocOS', '安卓版本': 10, '包含谷歌套件': '是', '下载链接': ga101url, '文件名': ga101},
    {'编号': 8, '系统名称': 'Resurrection_Remix', '安卓版本': 10, '包含谷歌套件': '是', '下载链接': ga102url, '文件名': ga102},
    {'编号': 9, '系统名称': 'LineageOS', '安卓版本': 10, '包含谷歌套件': '否', '下载链接': va101url, '文件名': va101},
    {'编号': 10, '系统名称': 'HavocOS', '安卓版本': 10, '包含谷歌套件': '否', '下载链接': va102url, '文件名': va102},
    {'编号': 11, '系统名称': 'Resurrection_Remix', '安卓版本': 10, '包含谷歌套件': '否', '下载链接': va103url, '文件名': va103},
]

system_list_TEST = [['编号','系统名称','安卓版本','包含谷歌套件'], 
             [1,'Resurrection_Remix',10,'是']]

boot_list = [['编号','boot类型','包含root'], 
             [1,'原厂boot','否'], 
             [2,'Magisk_Delta','是']]
