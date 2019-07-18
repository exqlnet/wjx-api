# encoding=utf-8
"""
这是一个简单的调用示例
只需要输入问卷星账号密码和问卷的activity标识
用于在每天的20点清空填写数据，21点开启问卷，其他时间关闭问卷
如果没有下载数据则会自动下载数据并保存到data目录下
"""
activity = "42794295"

from wjx import Wjx
import time
from datetime import datetime
import random
import os
from logger import log

wjx = Wjx("wjx_username", "wjx_password")
stat = wjx.is_running("wjx_activity_id")
log("该问卷运行状态：", "正在运行" if stat else "未运行")

# 先创建data目录
if not os.path.exists("data"):
    os.mkdir("data")

while True:
    now = datetime.now()
    log("Checking...")
    filename = "data/" + now.strftime("%Y-%m-%d") + ".xls"
    if now.hour == 20:
        wjx.clear(activity)
    if now.hour >= 21:
        wjx.start(activity)
    else:
        wjx.stop(activity)
        if not os.path.exists(filename):
            wjx.download(activity, filename)
    time.sleep(1 + random.random())
