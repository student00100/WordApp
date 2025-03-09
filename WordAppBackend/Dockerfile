FROM python:3.10

RUN apt update -y
RUN apt-get update -y
RUN apt-get install vim ffmpeg libsm6 libxext6 netcat-traditional build-essential ca-certificates -y

# 修改时区为国内时区
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 安装必要的项目依赖
WORKDIR /app/WordAppBackend
ADD ./requirements.txt /app/WordAppBackend/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD WordAppBackend /app/WordAppBackend
RUN mkdir -p /usr/local/var/log
