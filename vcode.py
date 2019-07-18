# encoding=utf-8
import requests
import hashlib
import time
import json
from logger import log


class Verify:
    """
    该验证码识别调用的是http://www.fateadm.com平台
    识别率挺高的
    需要注册，获取到pd_id和pd_key再实例化Verify
    """
    pd_id = ""
    pd_key = ""

    def __init__(self, pd_id, pd_key):

        self.pd_id = pd_id
        self.pd_key = pd_key
        self.host = "http://pred.fateadm.com"

    @staticmethod
    def CalcSign(pd_id, passwd, timestamp):
        md5 = hashlib.md5()
        md5.update((timestamp + passwd).encode())
        csign = md5.hexdigest()

        md5 = hashlib.md5()
        md5.update((pd_id + timestamp + csign).encode())
        csign = md5.hexdigest()
        return csign

    def recognize(self, img_data, pred_type):
        tm = str(int(time.time()))
        sign = self.CalcSign(self.pd_id, self.pd_key, tm)

        data = {
                "user_id": self.pd_id,
                "timestamp": tm,
                "sign": sign,
                "predict_type": pred_type,
                "up_type": "mt"
        }

        url = self.host + "/api/capreg"
        files = {'img_data': ('img_data', img_data)}
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.post(url, data=data, files=files, headers=headers)

        res = r.json()
        if res["RetCode"] == "4003":
            log("账户余额不足请及时充值")
            return ""

        if res["RetCode"] != "0":
            log("Error: 验证码识别异常:", res["RetCode"])
            return ""

        return json.loads(res["RspData"])["result"]

#
v = Verify("pd_id", "pd_key")
# img_data = open("test.gif", "rb").read()
# log(v.recognize(img_data, "30400"))
#

