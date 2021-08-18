#!/usr/bin/python3
# @Time    : 2021/4/11 4:40 下午
# @Author  : WangXin

from jenkinsapi.jenkins import Jenkins


def test_jenkins():
    J = Jenkins("http://localhost:8080/", username="admin", password="123456", useCrumb=True)
    print(J.keys())
    # J.build_job("TestPlatform", {"name": "wx1", "file_name": "wx3.csv"})
    r = J["TestPlatform"].invoke(build_params={"name": "wx2", "file_name": "wx3.csv"})
    if r.is_queued() or r.is_running():
        r.block_until_complete()

    build = r.get_build()
    print(build)
