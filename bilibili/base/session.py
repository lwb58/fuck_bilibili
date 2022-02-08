import os
import json
import re
import requests
from requests.adapters import HTTPAdapter


class Session(requests.Session):
    def __init__(self, tries=None, headers=None, cookies=None, **request_kw):
        super().__init__()
        self.request_kw = request_kw
        self.last_response = None
        self.mount_http_adapter(tries)
        self.update_headers(headers)
        self.update_cookies(cookies)

    def mount_http_adapter(self, tries):
        self.mount('http://', HTTPAdapter(max_retries=tries))
        self.mount('https://', HTTPAdapter(max_retries=tries))

    def update_headers(self, headers):
        headers = headers or {
            "accept":
            "*/*",
            "accept-encoding":
            "json",
            "accept-language":
            "zh-CN,zh;q=0.9,en;q=0.8",
            "user-agent":
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
        }
        self.headers.update(headers)

    def update_cookies(self, cookies):
        if isinstance(cookies, str):
            if os.path.exists(cookies):
                self.add_cookies_by_file(cookies)
            else:
                self.add_cookie_by_str(cookies)
        elif isinstance(cookies, list):
            self.add_cookie_by_jar(cookies)
        elif isinstance(cookies, dict):
            self.cookies.update(cookies)

    def add_cookies_by_file(self, path):
        with open(path, "r") as f:
            content = f.read()
            try:
                data = json.loads(content)
                self.add_cookie_by_jar(data)
            except:
                self.headers.update({"cookie": content})

    def add_cookie_by_jar(self, data):
        for cookie in data:
            self.cookies.set(cookie['name'], cookie['value'])

    def add_cookie_by_str(self, data):
        self.headers.update({"cookie": data})
        for cookie in data.split(";"):
            k, v = re.search(r"([^=]+)=(.*)", cookie).groups()
            self.cookies.set(k.strip(), v.strip())

    def request(self, *args, **kw):
        kw.update(self.request_kw)
        res = super().request(*args, **kw)
        self.last_response = res
        print("\n", "---" * 20)
        print(args, res)
        for k, v in kw.items():
            if k == "data" and kw["data"] and len(kw["data"]) > 10:
                print(k, f'{kw["data"][:10]}...')
            else:
                print(k, v)
        return res
