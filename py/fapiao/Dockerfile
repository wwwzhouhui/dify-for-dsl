# 使用官方Python运行时作为基础镜像
# FROM python:3.11-slim
FROM crpi-e3ns1qhr61atprr9.cn-hangzhou.personal.cr.aliyuncs.com/geekaiapp2/python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制requirements文件
COPY requirements.txt /app/

# 安装Python依赖
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# 复制项目文件
COPY fapiaosqd.py /app/
COPY fapiaosqd.css /app/
COPY README.md /app/

# 暴露端口
EXPOSE 15601

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:15601 || exit 1

# 启动命令
CMD ["python", "fapiaosqd.py"]