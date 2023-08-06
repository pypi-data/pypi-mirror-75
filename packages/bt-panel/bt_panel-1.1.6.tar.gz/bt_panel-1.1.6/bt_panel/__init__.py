# -*- coding: utf-8 -*-
# 修改 panel 模板
import time
from .log import get_logger
from .daemon import daemon_start
import os
import subprocess

try:
    logger = get_logger('/tmp/bt_panel.log',3)
except:
    logger = None


def log(message):
    if logger:
        logger.info(message)


def func():
    try:
        # 从云端取列表
        file = '/www/server/panel/class/panelPlugin.py'
        old_str = "softList['list'] = tmpList"
        new_str = "softList['list'] = tmpList\n        softList['pro'] = 1 \n        for soft in softList['list']:\n            soft['endtime'] = 0"
        file_data = ""
        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                if "softList['pro'] = 1" in line or "for soft in softList['list']:" in line or "soft['endtime'] = 0" in line:
                    pass
                else:
                    if old_str in line:
                        line = line.replace(old_str, new_str)
                    file_data += line

        with open(file, "r", encoding="utf-8") as f1:
            data = f1.read()
        if "soft['endtime'] = 0" in data:
            pass
        else:
            with open(file, "w", encoding="utf-8") as f:
                f.write(file_data)
                log("panelPlugin.py 破解成功")
                # 重启面板
                try:
                    info = subprocess.Popen(["/etc/init.d/bt", "restart"],stdout=subprocess.PIPE)
                    log(info.stdout.read().decode('utf-8'))
                except:
                    pass

    except Exception as e:
        if 'encoding' in str(e):
            try:
                # 从云端取列表
                file = '/www/server/panel/class/panelPlugin.py'
                old_str = "softList['list'] = tmpList"
                new_str = "softList['list'] = tmpList\n        softList['pro'] = 1 \n        for soft in softList['list']:\n            soft['endtime'] = 0"
                file_data = ""
                with open(file, "r") as f:
                    for line in f:
                        if "softList['pro'] = 1" in line or "for soft in softList['list']:" in line or "soft['endtime'] = 0" in line:
                            pass
                        else:
                            if old_str in line:
                                line = line.replace(old_str, new_str)
                            file_data += line

                with open(file, "r") as f1:
                    data = f1.read()
                if "soft['endtime'] = 0" in data:
                    pass
                else:
                    with open(file, "w") as f:
                        f.write(file_data)
                        log("panelPlugin.py 破解成功")
                        # 重启面板
                        try:
                            info = subprocess.Popen(["/etc/init.d/bt", "restart"], stdout=subprocess.PIPE)
                            log(info.stdout.read())
                        except:
                            pass
            except Exception as e:
                log("安装bt软件%s" % e)
        else:
            log("安装bt软件%s" % e)




     # __get_mod
    try:
        file = '/www/server/panel/plugin/total/total_main.py'
        old_str = "if 'bt_total' in session: return public.returnMsg(True,'OK!');"
        new_str = "# if 'bt_total' in session: return public.returnMsg(True,'OK!');\n        session['bt_total'] = True \n        return public.returnMsg(True, 'OK!');"
        file_data = ""
        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                if "# if 'bt_total' in session: return public.returnMsg(True,'OK!');" in line :
                    pass
                else:
                    if old_str in line:
                        line = line.replace(old_str, new_str)
                    file_data += line
        with open(file, "r", encoding="utf-8") as f1:
            data = f1.read()
        if "# if 'bt_total' in session: return public.returnMsg(True,'OK!');" in data:
            pass
        else:
            with open(file, "w", encoding="utf-8") as f:
                f.write(file_data)
                log("total_main.py 破解成功")
                # 重启面板
                try:
                    info = subprocess.Popen(["/etc/init.d/bt", "restart"], stdout=subprocess.PIPE)
                    log(info.stdout.read().decode('utf-8'))
                except:
                    pass
    except Exception as e :
        if 'encoding' in str(e):
            try:
                file = '/www/server/panel/plugin/total/total_main.py'
                old_str = "if 'bt_total' in session: return public.returnMsg(True,'OK!');"
                new_str = "# if 'bt_total' in session: return public.returnMsg(True,'OK!');\n        session['bt_total'] = True \n        return public.returnMsg(True, 'OK!');"
                file_data = ""
                with open(file, "r") as f:
                    for line in f:
                        if "# if 'bt_total' in session: return public.returnMsg(True,'OK!');" in line:
                            pass
                        else:
                            if old_str in line:
                                line = line.replace(old_str, new_str)
                            file_data += line
                with open(file, "r") as f1:
                    data = f1.read()
                if "# if 'bt_total' in session: return public.returnMsg(True,'OK!');" in data:
                    pass
                else:
                    with open(file, "w") as f:
                        f.write(file_data)
                        log("total_main.py 破解成功")
                        # 重启面板
                        try:
                            info = subprocess.Popen(["/etc/init.d/bt", "restart"], stdout=subprocess.PIPE)
                            log(info.stdout.read())
                        except:
                            pass
            except Exception as e:
                log("需要安装付费插件如：网站监控报表")
        else:
            log("需要安装付费插件如：网站监控报表")




    # 自动跟新 文件 修改
    try:
        file = '/www/server/panel/class/config.py'
        old_str = "AutoUpdatePanel"
        new_str = "Panel1"
        file_data = ""
        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                if old_str in line:
                    line = line.replace(old_str, new_str)
                file_data += line

        with open(file, "r", encoding="utf-8") as f1:
            data = f1.read()
        if new_str in data:
            pass
        else:
            with open(file, "w", encoding="utf-8") as f:
                f.write(file_data)
            log("config.py 破解成功")
            # 重启面板
            try:
                info = subprocess.Popen(["/etc/init.d/bt", "restart"], stdout=subprocess.PIPE)
                log(info.stdout.read().decode('utf-8'))
            except:
                pass
    except Exception as e:
        if 'encoding' in str(e):
            try:
                file = '/www/server/panel/class/config.py'
                old_str = "AutoUpdatePanel"
                new_str = "Panel1"
                file_data = ""
                with open(file, "r") as f:
                    for line in f:
                        if old_str in line:
                            line = line.replace(old_str, new_str)
                        file_data += line

                with open(file, "r") as f1:
                    data = f1.read()
                if new_str in data:
                    pass
                else:
                    with open(file, "w") as f:
                        f.write(file_data)
                    log("config.py 破解成功")
                    # 重启面板
                    try:
                        info = subprocess.Popen(["/etc/init.d/bt", "restart"], stdout=subprocess.PIPE)
                        log(info.stdout.read().decode('utf-8'))
                    except:
                        pass
            except Exception as e:
                log("安装bt软件%s" % e)
        else:
            log("安装bt软件%s" % e)


def  main():
    log('start success...')
    print('start success...')
    daemon_start()
    while True:
        func()
        time.sleep(15)






