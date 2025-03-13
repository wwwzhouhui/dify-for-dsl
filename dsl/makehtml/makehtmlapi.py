from fastapi import FastAPI, HTTPException,Depends, Header
from pydantic import BaseModel
import logging
import time
import uvicorn
import configparser
import os
import json
import datetime
import random
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

app = FastAPI()

# 读取配置文件中的API密钥
config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')

# Tencent Cloud COS configuration
region = config.get('common', 'region')
secret_id = config.get('common', 'secret_id')
secret_key = config.get('common', 'secret_key')
bucket = config.get('common', 'bucket')

# 设置输出路径
output_path = config.get('html', 'output_path', fallback='html_output')

# 确保输出目录存在
os.makedirs(output_path, exist_ok=True)

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HTMLRequest(BaseModel):
    html_content: str
    filename: str = None  # 可选参数，如果不提供则自动生成

def verify_auth_token(authorization: str = Header(None)):
    """验证 Authorization Header 中的 Bearer Token"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization Header")
    
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid Authorization Scheme")
    
    # 从配置文件读取有效token列表
    valid_tokens = json.loads(config.get('auth', 'valid_tokens'))
    if token not in valid_tokens:
        raise HTTPException(status_code=403, detail="Invalid or Expired Token")
    
    return token
def generate_timestamp_filename(extension='html'):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    random_number = random.randint(1000, 9999)
    filename = f"{timestamp}_{random_number}.{extension}"
    return filename

def save_html_file(html_content, filename=None, output_dir=None):
    # 如果没有提供文件名，则生成一个
    if not filename:
        filename = generate_timestamp_filename()
    
    # 如果没有提供输出目录，则使用默认目录
    if not output_dir:
        output_dir = output_path
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 组合完整的输出路径
    file_path = os.path.join(output_dir, filename)
    
    # 写入HTML内容
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(html_content)
    
    # 返回文件名和输出路径
    return filename, file_path

def upload_cos(region, secret_id, secret_key, bucket, file_name, base_path):
    config = CosConfig(
        Region=region,
        SecretId=secret_id,
        SecretKey=secret_key
    )
    client = CosS3Client(config)
    file_path = os.path.join(base_path, file_name)
    response = client.upload_file(
        Bucket=bucket,
        LocalFilePath=file_path,
        Key=file_name,
        PartSize=10,
        MAXThread=10,
        EnableMD5=False
    )
    if response['ETag']:
        url = f"https://{bucket}.cos.{region}.myqcloud.com/{file_name}"
        return url
    else:
        return None

@app.post("/generate-html/")
async def generate_html(request: HTMLRequest,auth_token: str = Depends(verify_auth_token)):
    try:
        logger.info("开始处理HTML生成请求")
        start_time = time.time()
        
        # 保存HTML文件
        filename, file_path = save_html_file(request.html_content, request.filename)
        
        # 上传到腾讯云COS
        html_url = upload_cos(region, secret_id, secret_key, bucket, filename, output_path)
        
        elapsed_time = time.time() - start_time
        logger.info(f"HTML生成和上传完成，耗时 {elapsed_time:.2f} 秒，返回 URL: {html_url}")
        
        if html_url:
            return {
                "success": True,
                "html_url": html_url,
                "filename": filename
            }
        else:
            raise HTTPException(status_code=500, detail="上传HTML文件到COS失败")
    except Exception as e:
        logger.error(f"处理HTML生成请求时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8088)