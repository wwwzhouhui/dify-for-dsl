# 使用官方 Python 3.13 镜像
#FROM python:3.13-slim
#FROM mirrors.cloud.tencent.com/python/python:3.13-slim
#FROM registry.cn-hangzhou.aliyuncs.com/luyuehm/python:3.13-slim
FROM crpi-e3ns1qhr61atprr9.cn-hangzhou.personal.cr.aliyuncs.com/geekaiapp2/python:3.13-slim
# 使用官方 Node.js 镜像作为基础镜像
#FROM node:19.9.0

# 设置工作目录
WORKDIR /app

# 复制当前目录内容到 container 中
COPY requirements.txt /app
COPY readme.txt /app

# 安装项目依赖
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 运行应用程序
#CMD ["python", "geekaiapp/g_jiekou.py"]
#CMD ["python", "geekaiapp/jimeng_video_service.py"]
# 将启动脚本复制到容器中
COPY start.sh /start.sh
RUN chmod +x /start.sh

# 使用CMD运行启动脚本
CMD ["/start.sh"]

#docker-compose up --build