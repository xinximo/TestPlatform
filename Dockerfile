# docker pull xinximo/java8-python3.6
# Author: Wangxin
# Version: 2021-10-27

# 注意:Mac本地构建使用这个镜像:docker pull xinximo/java8-python3.6
# linux使用这个镜像:docker pull xinximo/java8-python3.6-linux

FROM xinximo/java8-python3.6-linux

MAINTAINER xinximo "woshiwangxin123@126.com"
# 解决psycopg无法在python3.6-alpine中没有基础依赖环境问题,安装git
COPY requirements.txt ./
RUN apk add --no-cache bash git openssh && \
    python -m pip install --upgrade pip && \
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install --no-cache-dir -r requirements.txt
COPY . .