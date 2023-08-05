# -*- coding: utf-8 -*-
# 修改 panel 模板
import time

def main():
    file = '/www/server/panel/class/panelPlugin.py'
    old_str = "softList['list'] = tmpList"
    new_str = "softList['list'] = tmpList\n\tsoftList['pro'] = 1 \n\tfor soft in softList['list']:\n\t\tsoft['endtime'] = 0"
    file_data = ""
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            if old_str in line:
                line = line.replace(old_str, new_str)
            file_data += line
    with open(file, "w", encoding="utf-8") as f:
        f.write(file_data)


    # 自动跟新 文件 修改
    file = '/www/server/panel/class/config.py'
    # file = '/Users/zhao/githubs/set_panel/config.py'
    old_str = "AutoUpdatePane"
    new_str = "AutoUpdatePanel1"
    file_data = ""
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            if old_str in line:
                line = line.replace(old_str, new_str)
            file_data += line

    with open(file, "w", encoding="utf-8") as f:
        f.write(file_data)

    # 自动跟新 文件 修改
    file = '/www/server/panel/BTPanel/templates/default/index.html'
    # file = '/Users/zhao/githubs/set_panel/index.html'
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

    while True:
        try:
            file = '/www/server/panel/plugin/total/total_main.py'
            # file = '/Users/zhao/githubs/nginx_manage/12.py'
        except:
            print('需要安装付费插件')
            time.sleep(10)
            continue
        else:
            print('success')
            old_str = "if 'bt_total' in session: return public.returnMsg(True,'OK!');"
            new_str = "# if 'bt_total' in session: return public.returnMsg(True,'OK!');\n\tsession['bt_total'] = True \n\treturn public.returnMsg(True, 'OK!');"
            file_data = ""
            with open(file, "r", encoding="utf-8") as f:
                for line in f:
                    if old_str in line:
                        line = line.replace(old_str, new_str)
                    file_data += line
            with open(file, "w", encoding="utf-8") as f:
                f.write(file_data)
            break



if __name__ == '__main__':
    main()