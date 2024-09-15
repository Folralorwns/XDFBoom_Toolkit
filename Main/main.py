#######################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
#预加载区|安装区
import os
import time
from tabulate import tabulate
import webbrowser
from External.env_ver_checker import checker,workmode
from External.Record import record_time
from External.ROM_Dowload_Link import *
from External.Android_Debug_Bridge import flash_dir,adb,adb_shell,adb_connection_check,fastboot,fastboot_connection_check
from External.Dowloader import Down_and_Dec
from External.Env_Packages import Now_Path
from External.Security_Agreement import agreement_check
from External.Screen_Clear import prepare_screen
from External.Logger import Log
os.system('@echo off')
prepare_screen()
dir = os.path.abspath(Now_Path)
os.chdir(dir)
checker(1)
checker(2)
checker(3)
#################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
#主程序
prepare_screen()
agreement_check()
Log()
while True:
    os.chdir(dir)
    prepare_screen()
    Tools_Check = os.path.exists('C:/N1/Toolkit')
    Toolsp_check = os.path.exists('C:/N1/Logs/Package_Env_Installed')
    if Tools_Check == False and Toolsp_check == False:
        workmode = "受限"
    elif Tools_Check == True and Toolsp_check == False:
        open('C:/N1/Logs/Package_Env_Installed','w+').close()
        workmode = "完整模式"
    elif Tools_Check == False and Toolsp_check == True:
        os.remove('C:/N1/Logs/Package_Env_Installed')
        workmode = "受限"
    elif Tools_Check == True and Toolsp_check == True:
        workmode = "完整模式" 
    time.sleep(3)
    print("当前工作模式：%s" % (workmode))
    print("1.配置工具包和fastboot")
    print("2.进入fastboot并刷入系统")
    print("3.安装常用软件")
    print("4.解决网络问题（去×和！）")
    print("5.退出")
    print("6.关于我们")
    select = int(input("请选择您的操作（写入相应的数字)："))
    if select == 114514:
        Toolkit_link = Toolkit_link_TEST
        ga102url = ga102url_TEST
    if select == 1:
        prepare_screen()
        if workmode == "完整模式":
            print("您已经完成配置！")
            time.sleep(3)
            pass
        else:
            record_time(0)
            x = 0
            Down_and_Dec('tools',Toolkit_link,Toolkit)
            os.system('pip install -r C:/N1/Tookit/tools/requirements.txt')
            open('C:/N1/Logs/Package_Env_Installed','w+').close()
            workmode == "完整模式"
            while True:
                x += 1
                if x > 1e6:
                    break
            time.sleep(3)
    elif select == 2:
        prepare_screen()
        if workmode == "受限":
            print("请先去配置再使用！！！")
            time.sleep(3)
        elif workmode == "完整模式":
            while True:
                os.system('cls')
                os.system('color f9')
                # 显示系统列表，只包含系统名称、安卓版本和是否包含谷歌套件
                print(tabulate([[sys['编号'], sys['系统名称'], sys['安卓版本'], sys['包含谷歌套件']] for sys in system_list], headers=['系统名称', '安卓版本', '包含谷歌套件'], tablefmt='fancy_grid'))
                try:
                    system_select = int(input("请选择您要刷入的系统编号："))
                    selected_system = next((sys for sys in system_list if sys['编号'] == system_select), None)
                    if selected_system:
                        os.system('cls')
                        print(f"已选择刷入系统：{selected_system['系统名称']}")
                        # 在这里调用下载工具函数，并传入下载链接和文件名
                        Down_and_Dec('image',selected_system['下载链接'], selected_system['文件名'])
                        break
                    else:
                        print("请选择正确的系统编号。")
                except ValueError:
                    print("请输入有效的数字编号。")
            print("刷机前确认，此操作会造成数据全部被抹除，要继续吗？（按任意键继续）")
            os.system('pause')
            print("二次确认，您确定要继续吗？（按任意键继续）")
            os.system('pause')
            os.system('cls')
            print("程序开始")
            record_time(0)
            x = 0
            devices_bootloader = os.popen(r'fastboot.exe devices',"r")
            Device_Reader = devices_bootloader.read()
            if "fastboot" and "XDFN1" in Device_Reader:
                fb_checker = input("检测到fastboot设备，是否直接刷入(Y/N)")
                if "N" in fb_checker:                   
                    os.system('python C:/N1/Toolkit/tools/mtk script run.example')
                    print("现在，请立即拔线")
                    time.sleep(5)
                    prepare_screen()
                    os.chdir(flash_dir)
                    fastboot_connection_check()
                elif "Y" in fb_checker:
                    prepare_screen()
                    os.chdir(flash_dir)
                    pass
            else:
                os.system('python C:/N1/Toolkit/tools/mtk script run.example')
                print("现在，请立即拔线")
                time.sleep(3)
                prepare_screen()
                os.chdir(flash_dir)
                fastboot_connection_check()
            flash_vbmeta = fastboot('--disable-verity --disable-verification flash vbmeta C:/N1/Toolkit/ADB/Image/vbmeta.img')
            print("vbmeta刷入成功")
            flash_super = fastboot('flash super C:/N1/Toolkit/ADB/Image/super.img')
            print("一些GSI镜像以及原厂系统可能会Sparse到最后一个报错，不用管，放心开机")
            print("super刷入成功")
            prepare_screen()
            # while True:
            #     print(tabulate(boot_list, headers='firstrow', tablefmt='fancy_grid'))
            #     sselect = int(input("请您选择您要的操作："))
            #     if sselect == 1:
            #         flash_boot = fastboot('flash boot C:/N1/Toolkit/ADB/Image/Magisk.img')
            #         print("boot刷入成功")
            #         break
            #     elif sselect == 2:
            #         flash_normal_boot = fastboot('flash boot C:/N1/Toolkit/ADB/Image/normal.img')
            #         print("boot刷入成功")
            #         break
            # prepare_screen()
            print("正在三清...")
            erase = fastboot('-w')
            prepare_screen()
            print("正在重启")
            fastboot('reboot')
            print("刚刷完机后的第一次开机可能会持续1~3分钟，请耐心等待")
            print("正在清理super.img")
            os.remove('C:/N1/Toolkit/ADB/Image/super.img')
            time.sleep(5)
            while True:
                x += 1
                if x > 1e6:
                    break
            record_time(1)
    elif select == 3:
        if  workmode== "受限":
            print("请去先去配置再使用此功能！！！")
            time.sleep(3)
        elif workmode == "完整模式":
            record_time(0)
            x = 0
            prepare_screen()
            adb_connection_check()
            adb('install -r C:/N1/Toolkit/ADB/App/Android_System_WebView.apk')
            adb('install -r C:/N1/Toolkit/ADB/App/Gboard.apk')
            adb('install -r C:/N1/Toolkit/ADB/App/Huawei_AppGallery.apk')
            adb('install -r C:/N1/Toolkit/ADB/App/Huawei_Mobile_Services_Core.apk')
            adb('install -r C:/N1/Toolkit/ADB/App/HUAWEI_Services_Framework.apk')
            adb('install -r C:/N1/Toolkit/ADB/App/Kitsune_Mask.apk')
            adb('install -r C:/N1/Toolkit/ADB/App/MT_Manager.apk')
            adb('install -r C:/N1/Toolkit/ADB/App/Via_Browser.apk')
            adb('kill-server')
            print("安装成功")
            while True:
                x += 1
                if x > 1e6:
                    break
            record_time(1)
            time.sleep(5)
    elif select == 4:
        if workmode== "受限":
            print("请您先去配置再使用此功能！！！")
            time.sleep(3)
        elif workmode== "完整模式":
            record_time(0)
            x = 0
            prepare_screen()
            adb_connection_check()
            adb_shell('settings delete global captive_portal_http_url')
            adb_shell('settings delete global captive_portal_https_url')
            adb_shell('settings put global captive_portal_http_url http://connect.rom.miui.com/generate_204')
            adb_shell('settings put global captive_portal_https_url https://connect.rom.miui.com/generate_204')
            adb('kill-server')
            print("解决成功")
            while True:
                x += 1
                if x > 1e6:
                    break
            record_time(1)
        time.sleep(5)
    elif select == 5:
        prepare_screen()
        os.chdir(dir)
        exitt = input("感谢您使用我的工具包，是否想请作者喝一杯咖啡呢？[Y/N]")
        if exitt == "Y" or exitt == "y":
            webbrowser.open_new_tab('https://afdian.net/a/lin757009986')
            time.sleep(10)
            print("谢谢🥰")
            time.sleep(3)
            os.system('exit')
            break
        elif exitt =="N" or exitt == "n":
            print("欢迎下次使用哦~")
            time.sleep(3)
            os.system('exit')
            break
#######################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
from charset_normalizer import md__mypyc
