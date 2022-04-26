# Author: Wangxin
# Version: 2021-10-27

FROM python:3.9

MAINTAINER xinximo "woshiwangxin123@126.com"
WORKDIR /app
COPY requirements.txt ./
RUN python -m pip install --upgrade pip && \
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install --no-cache-dir -r requirements.txt
COPY . .
ENTRYPOINT ["python","backend/back.py"]