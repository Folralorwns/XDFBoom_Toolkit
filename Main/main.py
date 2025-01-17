#预加载区|安装区
import os
import time
from tabulate import tabulate
import webbrowser
from External.env_ver_checker import checker,workmode
from External.Android_Debug_Bridge import adb,adb_shell,adb_connection_check
from External.Path_Dict import Now_Path
from External.Security_Agreement import agreement_check
from External.Screen_Clear import prepare_screen
from External.About_US import About_US
os.system('@echo off')
prepare_screen()
dir = os.path.abspath(Now_Path)
os.chdir(dir)
checker(1)
checker(2)
checker(3)
#主程序
prepare_screen()
agreement_check()
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
    print("3.解决网络问题（去×和！）")
    print("4.退出")
    print("5.关于我们")
    select = int(input("请选择您的操作（写入相应的数字)："))
    if select == 1:
        prepare_screen()
        if workmode == "完整模式":
            print("您已经完成配置！")
            time.sleep(3)
            pass
        else:
            
            open('C:/N1/Logs/Package_Env_Installed','w+').close()
            workmode == "完整模式"
            time.sleep(3)
    elif select == 2:
        prepare_screen()
        if workmode == "受限":
            print("请先去配置再使用！！！")
            time.sleep(3)
        elif workmode == "完整模式":
            print("刷机前确认，此操作会造成数据全部被抹除，要继续吗？（按任意键继续）")
            os.system('pause')
            print("二次确认，您确定要继续吗？（按任意键继续）")
            os.system('pause')
            os.system('cls')
            print("程序开始")
            os.system('python C:/N1/Toolkit/tools/mtk.py script C:/N1/Toolkit/tools/run.example')
            print("现在，请立即拔线")
            time.sleep(3)
            prepare_screen()
    elif select == 3:
        if workmode== "受限":
            print("请您先去配置再使用此功能！！！")
            time.sleep(3)
        elif workmode== "完整模式":
            prepare_screen()
            adb_connection_check()
            adb_shell('settings delete global captive_portal_http_url')
            adb_shell('settings delete global captive_portal_https_url')
            adb_shell('settings put global captive_portal_http_url http://connect.rom.miui.com/generate_204')
            adb_shell('settings put global captive_portal_https_url https://connect.rom.miui.com/generate_204')
            adb('kill-server')
            print("解决成功")
        time.sleep(5)
    elif select == 4:
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
    elif select == 5:
        About_US() 
from charset_normalizer import md__mypyc
