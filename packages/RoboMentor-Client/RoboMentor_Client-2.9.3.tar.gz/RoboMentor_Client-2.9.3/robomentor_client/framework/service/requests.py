import requests
from ..log import Log

class Requests:

    @staticmethod
    def api(url, params, headers, http_method):
        res = ""
        if http_method.upper() == "POST":
            try:
                res = requests.post(url, params, headers=headers)
            except Exception as e:
                Log.error("POST请求出现了异常：{0}".format(e))
        elif http_method.upper() == "GET":
            try:
                res = requests.get(url, params, headers=headers)
            except Exception as e:
                Log.error("GET请求出现了异常：{0}".format(e))
        return res