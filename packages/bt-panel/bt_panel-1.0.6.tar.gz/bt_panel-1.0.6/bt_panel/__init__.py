# -*- coding: utf-8 -*-
# 修改 panel 模板
import time
from .log import get_logger
from .daemon import daemon_start

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

        with open(file, "w", encoding="utf-8") as f:
            f.write(file_data)
            log("panelPlugin.py 破解成功")
    except Exception as e:
        log("安装bt软件%s"%e)


    #  __get_mod
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
    except Exception as e :
        log("需要安装付费插件如：网站监控报表")

    else:
        with open(file, "w", encoding="utf-8") as f:
            f.write(file_data)
            log("total_main.py 破解成功")


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

        with open(file, "w", encoding="utf-8") as f:
            f.write(file_data)
    except Exception as e:
        log("安装bt软件%s" % e)



    # 自动跟新 文件 修改
    try:
        file = '/www/server/panel/BTPanel/templates/default/index.html'
        old_str = "javascript:index.check_update();"
        new_str = "#"
        file_data = ""
        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                if old_str in line:
                    line = line.replace(old_str, new_str)
                file_data += line
        with open(file, "w", encoding="utf-8") as f:
            f.write(file_data)

    except Exception as e:
        log("安装bt软件%s" % e)


def  main():
    log('start success...')
    print('start success...')
    daemon_start()
    while True:
        time.sleep(10)
        func()





