#!/usr/bin/python3
# @Time    : 2021/4/11 4:34 下午
# @Author  : WangXin

import requests


class TestServer:
    def test_get_testcase(self):
        r = requests.get("http://127.0.0.1:5000/get_testcase", params={"name": "wx1"})
        assert "wx1" in r.text
