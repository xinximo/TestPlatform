# docker pull xinximo/java8-python3.6
# Author: Wangxin
# Version: 2021-10-27

# 注意:Mac本地构建使用这个镜像:docker pull xinximo/java8-python3.6
# linux使用这个镜像:docker pull xinximo/java8-python3.6-linux

FROM xinximo/java8-python3.6-linux

MAINTAINER xinximo "woshiwangxin123@126.com"
COPY requirements.txt ./
RUN apk add --no-cache --virtual .build-deps gcc musl-dev gcc-c++ && \
    apk add --no-cache bash git openssh && \
    python -m pip install --upgrade pip && \
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install --no-cache-dir -r requirements.txt && \
    apk --purge del .build-deps
COPY . .