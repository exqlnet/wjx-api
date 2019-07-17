import requests


class Wjx:

    cookie = ""

    def __init__(self, cookie):
        self.cookie = cookie

    def start(self, activity):
        if not self.is_running(activity):
            url = "https://www.wjx.cn/wjx/design/designstart.aspx"

            querystring = {"activity": activity}

            payload = "__VIEWSTATE=%2FwEPDwUKLTk0MDg2MTE5NA9kFgJmD2QWFgIBD2QWAgIBDxYCHglpbm5lcmh0bWwF%2FAI8YSBocmVmPSdqYXZhc2NyaXB0OiB2b2lkKDApOycgb25jbGljaz0nUERGX2xhdW5jaCgiL3dqeC9tYW5hZ2Uvb25saW5lc3VwcG9ydC5hc3B4IiwgNjIwLCA0MDApOyAnICBjbGFzcz0nYnRuIGJ0bi1kZWZhdWx0IGJ0bi1zbSBidG4tc20tYXBwbHkgJz7nlLPor7fljY%2Fliqk8L2E%2BPGRpdiBjbGFzcz0nZnJlZXByb21vdGV0eHQnIHN0eWxlPSdtYXJnaW4tdG9wOjhweDsnPjxiPuaPkOekuu%2B8mjwvYj7ljYfnuqfliLDkvIHkuJrniYjlj6%2Fkuqvlj5flnKjnur%2Flkqjor6Llj4rnlLXor53mlK%2FmjIHvvIw8YSBocmVmPScgL3JlZ2lzdGVyL3VwZ3JhZGV2aXAuYXNweD91cGdyYWRlUmVhc29uPTE3JyAgY2xhc3M9J3RpdGxlbG5rJz7kuobop6Por6bmg4U8L2E%2BPC9zcGFuPmQCAg8WAh8ABfMBPHNlbGVjdCAgaWQ9J2RkbEFjdGl2aXR5bmV3JyBzdHlsZT0nJz48b3B0aW9uIHZhbHVlPSc0Mjc5NDI5NScgc2VsZWN0ZWQ9J3NlbGVjdGVkJz4yMDE55pqR5pyf5YC854%2Bt4oCc6Zu25oql5ZGK4oCd5oOF5Ya15oql6YCBKElEOjQyNzk0Mjk1KTwvb3B0aW9uPjxvcHRpb24gdmFsdWU9JzQxMjg0NjcxJz7lrabplb%2FlsI%2FmlZnlkZjlupTnn6XlupTkvJrnkIborrrlrabkuaAoSUQ6NDEyODQ2NzEpPC9vcHRpb24%2BPC9zZWxlY3Q%2BZAIDDxYCHgRocmVmBTQvd2p4L2Rlc2lnbi9wcmV2aWV3bW9iaWxlLmFzcHg%2FYWN0aXZpdHk9NDI3OTQyOTUmcz0xZAIEDxYEHwEFLC93angvcHJvbW90ZS9pbnZpdGUuYXNweD9hY3Rpdml0eWlkPTQyNzk0Mjk1HgdWaXNpYmxlaGQCBQ8WBB8BBS8vd2p4L3Byb21vdGUvaW52aXRlc21zLmFzcHg%2FYWN0aXZpdHlpZD00Mjc5NDI5NR8CaGQCBg8WAh8CZ2QCBw8WAh8BBTQvc2FtcGxlL2RlbWFuZC5hc3B4P2FjdGl2aXR5aWQ9NDI3OTQyOTUmbHN0PTEmbnB1Yj0xZAIIDxYEHwEFMC93angvcHJvbW90ZS9qb2luYmFja2xpc3QuYXNweD9hY3Rpdml0eT00Mjc5NDI5NR8CZ2QCCQ8WBB8BBTAvd2p4L3Byb21vdGUvcHJvbW90ZWFwcGx5LmFzcHg%2FYWN0aXZpdHk9NDI3OTQyOTUfAmdkAg0PFgIfAQU0L3dqeC9kZXNpZ24vcHJldmlld21vYmlsZS5hc3B4P2FjdGl2aXR5PTQyNzk0Mjk1JnM9MWQCDw9kFgICAQ9kFgoCAQ8WAh8CZxYEAgEPDxYCHgRUZXh0BWnmraTpl67ljbfmraPlnKjov5DooYzvvIzmgqjlj6%2Fku6U8YSBocmVmPScvcmVwb3J0LzQyNzk0Mjk1LmFzcHgnIGNsYXNzPSd3anhfYWxpbmsnPuafpeeci%2Be7k%2BaenDwvYT7miJbogIVkZAIDDw8WBB8DBRLmmoLlgZzmjqXmlLbnrZTljbceDU9uQ2xpZW50Q2xpY2sFT3JldHVybiBkb0FjdGlvbign54q25oCB6K6%2B5Li64oCc5YGc5q2i4oCd5ZCO5bCG5LiN6IO95aGr5YaZ77yM5piv5ZCm57un57ut77yfJylkZAICDxYCHwJnZAIHDxYCHwEFNy9uZXd3angvZGVzaWduL2VkaXRxdWVzdGlvbm5haXJlLmFzcHg%2FYWN0aXZpdHk9NDI3OTQyOTVkAgkPFgIfAmhkAgwPZBYCAgEPEGRkFgFmZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WBAUeY3RsMDIkQ29udGVudFBsYWNlSG9sZGVyMSRyYmxBBR5jdGwwMiRDb250ZW50UGxhY2VIb2xkZXIxJHJibEEFHmN0bDAyJENvbnRlbnRQbGFjZUhvbGRlcjEkcmJsQwUeY3RsMDIkQ29udGVudFBsYWNlSG9sZGVyMSRyYmxD%2FOup%2F2xx4YGkdquUP11Cdd8xPQA%3D&__VIEWSTATEGENERATOR=54ECBFBC&__EVENTVALIDATION=%2FwEdAAfxBLPxM07xxGeIDAjv75L%2BJiB5twIPGrw%2BKcy63oTAP7%2FQCMc5phBLVPhp1UWM0wO4GikaWkkz6p28PrqaxvNKSe3rUU4Mkdn7V7T7lCLTl3gRplDDVJVDDhV2jPDS9TEQmKv%2FwYin78idBCqpeMwvNRzeCqVYNTJuDVQIqkUcqXoL%2BVw%3D&ctl02%24ContentPlaceHolder1%24btnRun=%e6%81%a2%e5%a4%8d%e8%bf%90%e8%a1%8c"
            headers = {
                'Content-Type': "application/x-www-form-urlencoded",
                'Cookie': self.cookie,
                'User-Agent': "PostmanRuntime/7.15.0",
                'Accept': "*/*",
                'Cache-Control': "no-cache",
                'Host': "www.wjx.cn",
                'accept-encoding': "gzip, deflate",
                'content-length': "2645",
                'cache-control': "no-cache"
            }

            requests.request("POST", url, data=payload, headers=headers, params=querystring)
            print("OK start")

    def stop(self, activity):
        if self.is_running(activity):
            url = "https://www.wjx.cn/wjx/design/designstart.aspx"

            querystring = {"activity": activity}

            payload = "__VIEWSTATE=%2FwEPDwUKLTk0MDg2MTE5NA9kFgJmD2QWFgIBD2QWAgIBDxYCHglpbm5lcmh0bWwF%2FAI8YSBocmVmPSdqYXZhc2NyaXB0OiB2b2lkKDApOycgb25jbGljaz0nUERGX2xhdW5jaCgiL3dqeC9tYW5hZ2Uvb25saW5lc3VwcG9ydC5hc3B4IiwgNjIwLCA0MDApOyAnICBjbGFzcz0nYnRuIGJ0bi1kZWZhdWx0IGJ0bi1zbSBidG4tc20tYXBwbHkgJz7nlLPor7fljY%2Fliqk8L2E%2BPGRpdiBjbGFzcz0nZnJlZXByb21vdGV0eHQnIHN0eWxlPSdtYXJnaW4tdG9wOjhweDsnPjxiPuaPkOekuu%2B8mjwvYj7ljYfnuqfliLDkvIHkuJrniYjlj6%2Fkuqvlj5flnKjnur%2Flkqjor6Llj4rnlLXor53mlK%2FmjIHvvIw8YSBocmVmPScgL3JlZ2lzdGVyL3VwZ3JhZGV2aXAuYXNweD91cGdyYWRlUmVhc29uPTE3JyAgY2xhc3M9J3RpdGxlbG5rJz7kuobop6Por6bmg4U8L2E%2BPC9zcGFuPmQCAg8WAh8ABfMBPHNlbGVjdCAgaWQ9J2RkbEFjdGl2aXR5bmV3JyBzdHlsZT0nJz48b3B0aW9uIHZhbHVlPSc0Mjc5NDI5NScgc2VsZWN0ZWQ9J3NlbGVjdGVkJz4yMDE55pqR5pyf5YC854%2Bt4oCc6Zu25oql5ZGK4oCd5oOF5Ya15oql6YCBKElEOjQyNzk0Mjk1KTwvb3B0aW9uPjxvcHRpb24gdmFsdWU9JzQxMjg0NjcxJz7lrabplb%2FlsI%2FmlZnlkZjlupTnn6XlupTkvJrnkIborrrlrabkuaAoSUQ6NDEyODQ2NzEpPC9vcHRpb24%2BPC9zZWxlY3Q%2BZAIDDxYCHgRocmVmBTQvd2p4L2Rlc2lnbi9wcmV2aWV3bW9iaWxlLmFzcHg%2FYWN0aXZpdHk9NDI3OTQyOTUmcz0xZAIEDxYEHwEFLC93angvcHJvbW90ZS9pbnZpdGUuYXNweD9hY3Rpdml0eWlkPTQyNzk0Mjk1HgdWaXNpYmxlaGQCBQ8WBB8BBS8vd2p4L3Byb21vdGUvaW52aXRlc21zLmFzcHg%2FYWN0aXZpdHlpZD00Mjc5NDI5NR8CaGQCBg8WAh8CZ2QCBw8WAh8BBTQvc2FtcGxlL2RlbWFuZC5hc3B4P2FjdGl2aXR5aWQ9NDI3OTQyOTUmbHN0PTEmbnB1Yj0xZAIIDxYEHwEFMC93angvcHJvbW90ZS9qb2luYmFja2xpc3QuYXNweD9hY3Rpdml0eT00Mjc5NDI5NR8CZ2QCCQ8WBB8BBTAvd2p4L3Byb21vdGUvcHJvbW90ZWFwcGx5LmFzcHg%2FYWN0aXZpdHk9NDI3OTQyOTUfAmdkAg0PFgIfAQU0L3dqeC9kZXNpZ24vcHJldmlld21vYmlsZS5hc3B4P2FjdGl2aXR5PTQyNzk0Mjk1JnM9MWQCDw9kFgICAQ9kFgoCAQ8WAh8CZxYEAgEPDxYCHgRUZXh0BWnmraTpl67ljbfmraPlnKjov5DooYzvvIzmgqjlj6%2Fku6U8YSBocmVmPScvcmVwb3J0LzQyNzk0Mjk1LmFzcHgnIGNsYXNzPSd3anhfYWxpbmsnPuafpeeci%2Be7k%2BaenDwvYT7miJbogIVkZAIDDw8WBB8DBRLmmoLlgZzmjqXmlLbnrZTljbceDU9uQ2xpZW50Q2xpY2sFT3JldHVybiBkb0FjdGlvbign54q25oCB6K6%2B5Li64oCc5YGc5q2i4oCd5ZCO5bCG5LiN6IO95aGr5YaZ77yM5piv5ZCm57un57ut77yfJylkZAICDxYCHwJnZAIHDxYCHwEFNy9uZXd3angvZGVzaWduL2VkaXRxdWVzdGlvbm5haXJlLmFzcHg%2FYWN0aXZpdHk9NDI3OTQyOTVkAgkPFgIfAmhkAgwPZBYCAgEPEGRkFgFmZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WBAUeY3RsMDIkQ29udGVudFBsYWNlSG9sZGVyMSRyYmxBBR5jdGwwMiRDb250ZW50UGxhY2VIb2xkZXIxJHJibEEFHmN0bDAyJENvbnRlbnRQbGFjZUhvbGRlcjEkcmJsQwUeY3RsMDIkQ29udGVudFBsYWNlSG9sZGVyMSRyYmxD%2FOup%2F2xx4YGkdquUP11Cdd8xPQA%3D&__VIEWSTATEGENERATOR=54ECBFBC&__EVENTVALIDATION=%2FwEdAAfxBLPxM07xxGeIDAjv75L%2BJiB5twIPGrw%2BKcy63oTAP7%2FQCMc5phBLVPhp1UWM0wO4GikaWkkz6p28PrqaxvNKSe3rUU4Mkdn7V7T7lCLTl3gRplDDVJVDDhV2jPDS9TEQmKv%2FwYin78idBCqpeMwvNRzeCqVYNTJuDVQIqkUcqXoL%2BVw%3D&ctl02%24ContentPlaceHolder1%24btnRun=%e6%9a%82%e5%81%9c%e6%8e%a5%e6%94%b6%e7%ad%94%e5%8d%b7"
            headers = {
                'Content-Type': "application/x-www-form-urlencoded",
                'Cookie': self.cookie,
                'User-Agent': "PostmanRuntime/7.15.0",
                'Accept': "*/*",
                'Cache-Control': "no-cache",
                'Host': "www.wjx.cn",
                'accept-encoding': "gzip, deflate",
                'content-length': "2645",
                'cache-control': "no-cache"
            }

            requests.request("POST", url, data=payload, headers=headers, params=querystring)
            print("OK stop")

    def download(self, activity, filename):
        headers = {
            'Cookie': self.cookie,
            'User-Agent': "PostmanRuntime/7.15.0",
            'Accept': "*/*",
            'Cache-Control': "no-cache",
            'Host': "www.wjx.cn",
            'accept-encoding': "gzip, deflate",
            'cache-control': "no-cache"
        }
        res = requests.get("https://www.wjx.cn/wjx/activitystat/viewstatsummary.aspx?activity={activity}&reportid=-1&dw=1&dt=2".format(activity=activity), headers=headers)
        res = requests.get(res.url)
        with open(filename, "wb") as file:
            file.write(res.content)

    def clear(self, activity):
        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'Cookie': self.cookie,
            'User-Agent': "PostmanRuntime/7.15.0",
            'Accept': "*/*",
            'Cache-Control': "no-cache",
            'Host': "www.wjx.cn",
            'accept-encoding': "gzip, deflate",
            'cache-control': "no-cache"
        }
        payload = "__VIEWSTATE=%2FwEPDwUKLTk0OTgzNTYwOA9kFgICAw9kFgICAQ8QDxYCHgRUZXh0BSvlsIbluo%2Flj7flvZLpm7Yo5q2k6Zeu5Y235b2T5YmN5bqP5Y%2B35Li6MTkpZGRkZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WAQUJY2JTZXRaZXJveyz0ClLPCE28yb2%2B%2B%2FsQ0h0fG5g%3D&__VIEWSTATEGENERATOR=2C076B20&__EVENTVALIDATION=%2FwEdAAPvnmVnxrcUrI4Udnygep35wLUC%2FJIggF33CSuxsPN6uzXG%2F58GMRFfvKBtMCp%2FMqIu9Q2TPXECWAXhtfUUlX5WtqxxKw%3D%3D&btnContinue=%E6%B8%85%E7%A9%BA"
        requests.post("https://www.wjx.cn/wjx/activitystat/clearalldata.aspx?activity={}".format(activity), data=payload, headers=headers)

    def is_running(self, activity):
        i = 0
        while i <= 3:
            i += 1
            headers = {
                'Cookie': self.cookie,
                'User-Agent': "PostmanRuntime/7.15.0",
                'Accept': "*/*",
                'Cache-Control': "no-cache",
                'Host': "www.wjx.cn",
                'accept-encoding': "gzip, deflate",
                'cache-control': "no-cache"
            }
            res = requests.get("https://www.wjx.cn/wjx/design/designstart.aspx?activity={}".format(activity), headers=headers)
            # print(res.text)

            if res.status_code == 200:
                if "此问卷正在运行，您可以" in res.text:
                    return True
                else:
                    return False
        return False
