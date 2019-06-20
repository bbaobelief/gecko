# -*- coding: UTF-8 -*-

import os
import random
import subprocess

# 随机获取壁纸
path = "/home/zheng/Pictures/wispx/full"
files = os.listdir(path)
name = random.choice(files)
img = "{0}/{1}".format(path, name)


# 清除当前session
pid = subprocess.check_output(["pgrep", "dde-session"]).decode("utf-8").strip()
cmd = "grep -z DBUS_SESSION_BUS_ADDRESS /proc/" + pid + "/environ|cut -d= -f2-"
os.environ["DBUS_SESSION_BUS_ADDRESS"] = subprocess.check_output(['/bin/bash', '-c', cmd]).decode(
    "utf-8").strip().replace("\0", "")

# 更换壁纸
command = "gsettings set com.deepin.wrap.gnome.desktop.background picture-uri {0}".format(img)
os.system(command)
