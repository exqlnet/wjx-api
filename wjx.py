# encoding=utf-8
import requests
import time
from vcode import v
from bs4 import BeautifulSoup
import urllib
from logger import log


class Wjx:

    cookie = ""
    session = requests.session()
    username = ""
    password = ""
    _VIEWSTATE = ""
    _EVENTVALIDATION = ""
    _STATEGENERATOR = ""

    def __init__(self, username, password):

        self.username = username
        self.password = password

    def request(self, url, data=None, method="get", content_type=None, params=None):
        while True:
            if content_type:
                res = self.session.request(method, url, data=data, params=params, headers={"Content-Type": content_type})
            else:
                res = self.session.request(method, url, data=data, params=params)

            if "第三方登录" in res.text:
                log("正在尝试登陆...")
                self.login()
                time.sleep(1)
                continue
            break
        return res

    def login(self):

        def get_img():
            img_url = "https://www.wjx.cn/AntiSpamImageGen.aspx?t={}&cp=1".format(str(int(time.time())))
            return self.session.get(img_url).content

        def has_vcode():
            res = self.session.get("https://www.wjx.cn/login.aspx")
            has = "验证码" in res.text
            soup = BeautifulSoup(res.content, "html.parser", from_encoding="utf-8")
            viewstate = soup.select("#__VIEWSTATE")[0]["value"]
            viewstategenerator = soup.select("#__VIEWSTATEGENERATOR")[0]["value"]
            eventvalidation = soup.select("#__EVENTVALIDATION")[0]["value"]
            # log(viewstate, eventvalidation, viewstategenerator)

            return has, {
                "viewstate": viewstate,
                "viewstategenerator": viewstategenerator,
                "eventvalidation": eventvalidation
            }

        def is_success(res):
            return "我的问卷" in res.text

        while True:
            self.session.cookies.clear()
            pre_info = has_vcode()
            data = {
                "__VIEWSTATE": pre_info[1]["viewstate"],
                "__VIEWSTATEGENERATOR": pre_info[1]["viewstategenerator"],
                "__EVENTVALIDATION": pre_info[1]["eventvalidation"],
                "UserName": self.username,
                "Password": self.password,
                "hfUserName": "",
                "LoginButton": "登 录"
            }
            headers = {
                'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                'accept-encoding': "gzip, deflate, br",
                'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
                'cache-control': "no-cache",
                'connection': "keep-alive",
                'content-type': "application/x-www-form-urlencoded",
                'host': "www.wjx.cn",
                'origin': "https://www.wjx.cn",
                'referer': "https://www.wjx.cn/login.aspx",
                'upgrade-insecure-requests': "1",
                'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
            }
            if pre_info[0]:  # 有验证码
                log("发现验证码，正在识别验证码.")

                img_data = get_img()
                # img_file = BytesIO(img_data)
                # from PIL import Image
                # img = Image.open(img_file)
                # img.show()
                code = v.recognize(img_data, "30400")
                if code != "":
                    log("识别验证码成功：", code)
                    data["AntiSpam1$txtValInputCode"] = code
                    res = self.session.post("https://www.wjx.cn/login.aspx", data=urllib.parse.urlencode(data),
                                            headers=headers)
                    if is_success(res):
                        log("你成功绕过了验证码，登陆成功！")
                        break
            else:
                log("无验证码，正在登录...")
                res = self.session.request("POST", "https://www.wjx.cn/login.aspx", data=urllib.parse.urlencode(data), headers=headers)
                if is_success(res):
                    log("还是没有验证码的时候爽😊，登陆成功！")
                    break
                log("登陆失败")
            time.sleep(1)
            continue

    def start(self, activity):
        if not self.is_running(activity):
            url = "https://www.wjx.cn/wjx/design/designstart.aspx"

            querystring = {"activity": activity}
            payload = {
                "__VIEWSTATE": self._VIEWSTATE,
                "__VIEWSTATEGENERATOR": self._STATEGENERATOR,
                "__EVENTVALIDATION": self._EVENTVALIDATION,
                "ctl02$ContentPlaceHolder1$btnRun": "恢复运行"
            }
            res = self.request(url, method="POST", data=urllib.parse.urlencode(payload),
                               params=querystring, content_type="application/x-www-form-urlencoded")
            if self.is_running(activity):
                log("OK start")
            else:
                log("Error start! ", res.status_code)

    def stop(self, activity):
        if self.is_running(activity):
            url = "https://www.wjx.cn/wjx/design/designstart.aspx"

            querystring = {"activity": activity}
            payload = {
                "__VIEWSTATE": self._VIEWSTATE,
                "__VIEWSTATEGENERATOR": self._STATEGENERATOR,
                "__EVENTVALIDATION": self._EVENTVALIDATION,
                "ctl02$ContentPlaceHolder1$btnRun": "暂停接收答卷"
            }
            res = self.request(url, method="POST", data=urllib.parse.urlencode(payload), params=querystring,
                               content_type="application/x-www-form-urlencoded")
            if not self.is_running(activity):
                log("OK stop")
            else:
                log("Error stop!", res.status_code)

    def download(self, activity, filename):
        res = self.request("https://www.wjx.cn/wjx/activitystat/viewstatsummary.aspx?activity={}&reportid=-1&dw=1&dt=2".format(activity))
        res = requests.get(res.url)
        with open(filename, "wb") as file:
            file.write(res.content)
        log("OK download: ", filename)

    def clear(self, activity):
        payload = {
            "__VIEWSTATE": self._VIEWSTATE,
            "__VIEWSTATEGENERATOR": self._STATEGENERATOR,
            "__EVENTVALIDATION": self._EVENTVALIDATION,
            "btnContinue": "清空"
        }
        self.request("https://www.wjx.cn/wjx/activitystat/clearalldata.aspx?activity={}".format(activity), method="post",
                     data=payload, content_type="application/x-www-form-urlencoded")
        log("OK clear data")

    def is_running(self, activity):
        res = self.request(url="https://www.wjx.cn/wjx/design/designstart.aspx?activity={}".format(activity))
        soup = BeautifulSoup(res.content, "html.parser", from_encoding="utf-8")
        self._VIEWSTATE = soup.select("#__VIEWSTATE")[0]["value"]
        self._STATEGENERATOR = soup.select("#__VIEWSTATEGENERATOR")[0]["value"]
        self._EVENTVALIDATION = soup.select("#__EVENTVALIDATION")[0]["value"]
        if "正在运行" in res.text:
            return True
        else:
            return False
