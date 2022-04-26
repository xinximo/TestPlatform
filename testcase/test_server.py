#!/usr/bin/python3
# @Time    : 2021/4/11 4:34 下午
# @Author  : WangXin
import json
import requests


class TestServer:
    def test_get_testcase(self):
        r = requests.get("http://127.0.0.1:5000/get_testcase", params={"name": "wx1"})
        assert "wx1" in r.text

    def test_login(self):
        data = {
            "account": "wx",
            "password": "123456"
        }
        r = requests.post("http://127.0.0.1:5000/login", data=json.dumps(data), headers={"Content-Type": "application/json"})
        assert "OK" in r.text
