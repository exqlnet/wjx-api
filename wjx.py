# encoding=utf-8
import requests
import time
from bs4 import BeautifulSoup
import urllib
from logger import log
from vcode import v


class Wjx:
    """
    该类对应问卷星的用户
    能够自动登陆、遇到验证码后调用接口识别验证码登陆
    """
    cookie = ""
    session = requests.session()
    username = ""
    password = ""

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
                    log("还是没有验证码更爽😊，登陆成功！")
                    break
                log("登陆失败")
            time.sleep(1)
            continue

    def start(self, activity):
        if not self.is_running(activity):
            url = "https://www.wjx.cn/wjx/design/designstart.aspx"

            querystring = {"activity": activity}

            payload = "__VIEWSTATE=%2FwEPDwUKLTk0MDg2MTE5NA9kFgJmD2QWFgIBD2QWAgIBDxYCHglpbm5lcmh0bWwF%2FAI8YSBocmVmPSdqYXZhc2NyaXB0OiB2b2lkKDApOycgb25jbGljaz0nUERGX2xhdW5jaCgiL3dqeC9tYW5hZ2Uvb25saW5lc3VwcG9ydC5hc3B4IiwgNjIwLCA0MDApOyAnICBjbGFzcz0nYnRuIGJ0bi1kZWZhdWx0IGJ0bi1zbSBidG4tc20tYXBwbHkgJz7nlLPor7fljY%2Fliqk8L2E%2BPGRpdiBjbGFzcz0nZnJlZXByb21vdGV0eHQnIHN0eWxlPSdtYXJnaW4tdG9wOjhweDsnPjxiPuaPkOekuu%2B8mjwvYj7ljYfnuqfliLDkvIHkuJrniYjlj6%2Fkuqvlj5flnKjnur%2Flkqjor6Llj4rnlLXor53mlK%2FmjIHvvIw8YSBocmVmPScgL3JlZ2lzdGVyL3VwZ3JhZGV2aXAuYXNweD91cGdyYWRlUmVhc29uPTE3JyAgY2xhc3M9J3RpdGxlbG5rJz7kuobop6Por6bmg4U8L2E%2BPC9zcGFuPmQCAg8WAh8ABfMBPHNlbGVjdCAgaWQ9J2RkbEFjdGl2aXR5bmV3JyBzdHlsZT0nJz48b3B0aW9uIHZhbHVlPSc0Mjc5NDI5NScgc2VsZWN0ZWQ9J3NlbGVjdGVkJz4yMDE55pqR5pyf5YC854%2Bt4oCc6Zu25oql5ZGK4oCd5oOF5Ya15oql6YCBKElEOjQyNzk0Mjk1KTwvb3B0aW9uPjxvcHRpb24gdmFsdWU9JzQxMjg0NjcxJz7lrabplb%2FlsI%2FmlZnlkZjlupTnn6XlupTkvJrnkIborrrlrabkuaAoSUQ6NDEyODQ2NzEpPC9vcHRpb24%2BPC9zZWxlY3Q%2BZAIDDxYCHgRocmVmBTQvd2p4L2Rlc2lnbi9wcmV2aWV3bW9iaWxlLmFzcHg%2FYWN0aXZpdHk9NDI3OTQyOTUmcz0xZAIEDxYEHwEFLC93angvcHJvbW90ZS9pbnZpdGUuYXNweD9hY3Rpdml0eWlkPTQyNzk0Mjk1HgdWaXNpYmxlaGQCBQ8WBB8BBS8vd2p4L3Byb21vdGUvaW52aXRlc21zLmFzcHg%2FYWN0aXZpdHlpZD00Mjc5NDI5NR8CaGQCBg8WAh8CZ2QCBw8WAh8BBTQvc2FtcGxlL2RlbWFuZC5hc3B4P2FjdGl2aXR5aWQ9NDI3OTQyOTUmbHN0PTEmbnB1Yj0xZAIIDxYEHwEFMC93angvcHJvbW90ZS9qb2luYmFja2xpc3QuYXNweD9hY3Rpdml0eT00Mjc5NDI5NR8CZ2QCCQ8WBB8BBTAvd2p4L3Byb21vdGUvcHJvbW90ZWFwcGx5LmFzcHg%2FYWN0aXZpdHk9NDI3OTQyOTUfAmdkAg0PFgIfAQU0L3dqeC9kZXNpZ24vcHJldmlld21vYmlsZS5hc3B4P2FjdGl2aXR5PTQyNzk0Mjk1JnM9MWQCDw9kFgICAQ9kFgoCAQ8WAh8CZxYEAgEPDxYCHgRUZXh0BWnmraTpl67ljbfmraPlnKjov5DooYzvvIzmgqjlj6%2Fku6U8YSBocmVmPScvcmVwb3J0LzQyNzk0Mjk1LmFzcHgnIGNsYXNzPSd3anhfYWxpbmsnPuafpeeci%2Be7k%2BaenDwvYT7miJbogIVkZAIDDw8WBB8DBRLmmoLlgZzmjqXmlLbnrZTljbceDU9uQ2xpZW50Q2xpY2sFT3JldHVybiBkb0FjdGlvbign54q25oCB6K6%2B5Li64oCc5YGc5q2i4oCd5ZCO5bCG5LiN6IO95aGr5YaZ77yM5piv5ZCm57un57ut77yfJylkZAICDxYCHwJnZAIHDxYCHwEFNy9uZXd3angvZGVzaWduL2VkaXRxdWVzdGlvbm5haXJlLmFzcHg%2FYWN0aXZpdHk9NDI3OTQyOTVkAgkPFgIfAmhkAgwPZBYCAgEPEGRkFgFmZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WBAUeY3RsMDIkQ29udGVudFBsYWNlSG9sZGVyMSRyYmxBBR5jdGwwMiRDb250ZW50UGxhY2VIb2xkZXIxJHJibEEFHmN0bDAyJENvbnRlbnRQbGFjZUhvbGRlcjEkcmJsQwUeY3RsMDIkQ29udGVudFBsYWNlSG9sZGVyMSRyYmxD%2FOup%2F2xx4YGkdquUP11Cdd8xPQA%3D&__VIEWSTATEGENERATOR=54ECBFBC&__EVENTVALIDATION=%2FwEdAAfxBLPxM07xxGeIDAjv75L%2BJiB5twIPGrw%2BKcy63oTAP7%2FQCMc5phBLVPhp1UWM0wO4GikaWkkz6p28PrqaxvNKSe3rUU4Mkdn7V7T7lCLTl3gRplDDVJVDDhV2jPDS9TEQmKv%2FwYin78idBCqpeMwvNRzeCqVYNTJuDVQIqkUcqXoL%2BVw%3D&ctl02%24ContentPlaceHolder1%24btnRun=%e6%81%a2%e5%a4%8d%e8%bf%90%e8%a1%8c"
            res = self.request(url, method="POST", data=payload, params=querystring, content_type="application/x-www-form-urlencoded")
            log("OK start")

    def stop(self, activity):
        if self.is_running(activity):
            url = "https://www.wjx.cn/wjx/design/designstart.aspx"

            querystring = {"activity": activity}

            payload = "__VIEWSTATE=%2FwEPDwUKLTk0MDg2MTE5NA9kFgJmD2QWFgIBD2QWAgIBDxYCHglpbm5lcmh0bWwF%2FAI8YSBocmVmPSdqYXZhc2NyaXB0OiB2b2lkKDApOycgb25jbGljaz0nUERGX2xhdW5jaCgiL3dqeC9tYW5hZ2Uvb25saW5lc3VwcG9ydC5hc3B4IiwgNjIwLCA0MDApOyAnICBjbGFzcz0nYnRuIGJ0bi1kZWZhdWx0IGJ0bi1zbSBidG4tc20tYXBwbHkgJz7nlLPor7fljY%2Fliqk8L2E%2BPGRpdiBjbGFzcz0nZnJlZXByb21vdGV0eHQnIHN0eWxlPSdtYXJnaW4tdG9wOjhweDsnPjxiPuaPkOekuu%2B8mjwvYj7ljYfnuqfliLDkvIHkuJrniYjlj6%2Fkuqvlj5flnKjnur%2Flkqjor6Llj4rnlLXor53mlK%2FmjIHvvIw8YSBocmVmPScgL3JlZ2lzdGVyL3VwZ3JhZGV2aXAuYXNweD91cGdyYWRlUmVhc29uPTE3JyAgY2xhc3M9J3RpdGxlbG5rJz7kuobop6Por6bmg4U8L2E%2BPC9zcGFuPmQCAg8WAh8ABfMBPHNlbGVjdCAgaWQ9J2RkbEFjdGl2aXR5bmV3JyBzdHlsZT0nJz48b3B0aW9uIHZhbHVlPSc0MTI4NDY3MSc%2B5a2m6ZW%2F5bCP5pWZ5ZGY5bqU55%2Bl5bqU5Lya55CG6K665a2m5LmgKElEOjQxMjg0NjcxKTwvb3B0aW9uPjxvcHRpb24gdmFsdWU9JzQyNzk0Mjk1JyBzZWxlY3RlZD0nc2VsZWN0ZWQnPjIwMTnmmpHmnJ%2FlgLznj63igJzpm7bmiqXlkYrigJ3mg4XlhrXmiqXpgIEoSUQ6NDI3OTQyOTUpPC9vcHRpb24%2BPC9zZWxlY3Q%2BZAIDDxYCHgRocmVmBTQvd2p4L2Rlc2lnbi9wcmV2aWV3bW9iaWxlLmFzcHg%2FYWN0aXZpdHk9NDI3OTQyOTUmcz0xZAIEDxYEHwEFLC93angvcHJvbW90ZS9pbnZpdGUuYXNweD9hY3Rpdml0eWlkPTQyNzk0Mjk1HgdWaXNpYmxlaGQCBQ8WBB8BBS8vd2p4L3Byb21vdGUvaW52aXRlc21zLmFzcHg%2FYWN0aXZpdHlpZD00Mjc5NDI5NR8CaGQCBg8WAh8CZ2QCBw8WAh8BBTQvc2FtcGxlL2RlbWFuZC5hc3B4P2FjdGl2aXR5aWQ9NDI3OTQyOTUmbHN0PTEmbnB1Yj0xZAIIDxYEHwEFMC93angvcHJvbW90ZS9qb2luYmFja2xpc3QuYXNweD9hY3Rpdml0eT00Mjc5NDI5NR8CZ2QCCQ8WBB8BBTAvd2p4L3Byb21vdGUvcHJvbW90ZWFwcGx5LmFzcHg%2FYWN0aXZpdHk9NDI3OTQyOTUfAmdkAg0PFgIfAQU0L3dqeC9kZXNpZ24vcHJldmlld21vYmlsZS5hc3B4P2FjdGl2aXR5PTQyNzk0Mjk1JnM9MWQCDw9kFgICAQ9kFgoCAQ8WAh8CZxYEAgEPDxYCHgRUZXh0BWnmraTpl67ljbfmraPlnKjov5DooYzvvIzmgqjlj6%2Fku6U8YSBocmVmPScvcmVwb3J0LzQyNzk0Mjk1LmFzcHgnIGNsYXNzPSd3anhfYWxpbmsnPuafpeeci%2Be7k%2BaenDwvYT7miJbogIVkZAIDDw8WBB8DBRLmmoLlgZzmjqXmlLbnrZTljbceDU9uQ2xpZW50Q2xpY2sFT3JldHVybiBkb0FjdGlvbign54q25oCB6K6%2B5Li64oCc5YGc5q2i4oCd5ZCO5bCG5LiN6IO95aGr5YaZ77yM5piv5ZCm57un57ut77yfJylkZAICDxYCHwJnZAIHDxYCHwEFNy9uZXd3angvZGVzaWduL2VkaXRxdWVzdGlvbm5haXJlLmFzcHg%2FYWN0aXZpdHk9NDI3OTQyOTVkAgkPFgIfAmhkAgwPZBYCAgEPEGRkFgFmZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WBAUeY3RsMDIkQ29udGVudFBsYWNlSG9sZGVyMSRyYmxBBR5jdGwwMiRDb250ZW50UGxhY2VIb2xkZXIxJHJibEEFHmN0bDAyJENvbnRlbnRQbGFjZUhvbGRlcjEkcmJsQwUeY3RsMDIkQ29udGVudFBsYWNlSG9sZGVyMSRyYmxDD9eo06cWKTNauU5W6lopaqAO2M4%3D&__VIEWSTATEGENERATOR=54ECBFBC&__EVENTVALIDATION=%2FwEdAAdPlc3R%2Fjgl6MbZMn0KTwg7JiB5twIPGrw%2BKcy63oTAP7%2FQCMc5phBLVPhp1UWM0wO4GikaWkkz6p28PrqaxvNKSe3rUU4Mkdn7V7T7lCLTl3gRplDDVJVDDhV2jPDS9TEQmKv%2FwYin78idBCqpeMwv%2B5PVjLYbAyFkNphjZ7SjmPgvjZc%3D&ctl02%24ContentPlaceHolder1%24btnRun=%E6%9A%82%E5%81%9C%E6%8E%A5%E6%94%B6%E7%AD%94%E5%8D%B7"
            res = self.request(url, method="POST", data=payload, params=querystring,
                               content_type="application/x-www-form-urlencoded")
            log("OK stop")

    def download(self, activity, filename):
        res = self.request("https://www.wjx.cn/wjx/activitystat/viewstatsummary.aspx?activity={activity}&reportid=-1&dw=1&dt=2".format(activity=activity))
        res = requests.get(res.url)
        with open(filename, "wb") as file:
            file.write(res.content)
        log("OK download: ", filename)

    def clear(self, activity):
        payload = "__VIEWSTATE=%2FwEPDwUKLTk0OTgzNTYwOA9kFgICAw9kFgICAQ8QDxYCHgRUZXh0BSvlsIbluo%2Flj7flvZLpm7Yo5q2k6Zeu5Y235b2T5YmN5bqP5Y%2B35Li6MTkpZGRkZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WAQUJY2JTZXRaZXJveyz0ClLPCE28yb2%2B%2B%2FsQ0h0fG5g%3D&__VIEWSTATEGENERATOR=2C076B20&__EVENTVALIDATION=%2FwEdAAPvnmVnxrcUrI4Udnygep35wLUC%2FJIggF33CSuxsPN6uzXG%2F58GMRFfvKBtMCp%2FMqIu9Q2TPXECWAXhtfUUlX5WtqxxKw%3D%3D&btnContinue=%E6%B8%85%E7%A9%BA"
        self.request("https://www.wjx.cn/wjx/activitystat/clearalldata.aspx?activity={}".format(activity), method="post", data=payload, content_type="application/x-www-form-urlencoded")
        log("OK clear data")

    def is_running(self, activity):
        i = 0
        i += 1
        res = self.request(url="https://www.wjx.cn/wjx/design/designstart.aspx?activity={}".format(activity))

        if "正在运行" in res.text:
            return True
        else:
            return False
