import requests
import json
import base64
from PIL import Image
import io
import os
import sys
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import datetime
import random
import configparser
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

# 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')

# 从配置文件中读取参数
api_key = config.get('DEFAULT', 'api_key')
output_path = config.get('DEFAULT', 'output_path')
region = config.get('DEFAULT', 'region')
secret_id = config.get('DEFAULT', 'secret_id')
secret_key = config.get('DEFAULT', 'secret_key')
bucket = config.get('DEFAULT', 'bucket')

app = FastAPI()

class GenerateImageRequest(BaseModel):
    prompt: str
def generate_timestamp_filename(extension='png'):
    # 获取当前时间的时间戳
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    # 生成一个随机数
    random_number = random.randint(1000, 9999)
    # 组合生成文件名
    filename = f"{timestamp}_{random_number}.{extension}"
    return filename

def base64_to_image(base64_string, output_dir):
    # 生成文件名
    filename = generate_timestamp_filename()
    # 组合完整的输出路径
    output_path = os.path.join(output_dir, filename)

    # 解码Base64字符串
    image_data = base64.b64decode(base64_string)

    # 将解码后的数据转换为图像
    image = Image.open(io.BytesIO(image_data))

    # 保存图像到指定路径
    image.save(output_path)

    print(f"图片已保存到 {output_path}")
    # 返回文件名和输出路径
    return filename, output_path

def upload_cos(env, file_name, base_path):
    # 读取配置文件
    config = CosConfig(
        Region=region,  # 替换为你的Region
        SecretId=secret_id,  # 替换为你的SecretId
        SecretKey=secret_key  # 替换为你的SecretKey
    )
    client = CosS3Client(config)

    # 构造上传文件的完整路径
    file_path = os.path.join(base_path, file_name)

    # 上传文件
    response = client.upload_file(
        Bucket=bucket,  # 替换为你的Bucket名称
        LocalFilePath=file_path,
        Key=file_name,
        PartSize=10,
        MAXThread=10,
        EnableMD5=False
    )

    if response['ETag']:
        print(f"文件 {file_name} 上传成功")
        # 构造并返回图片的URL
        url = f"https://{bucket}.cos.{region}.myqcloud.com/{file_name}"
        return url
    else:
        print(f"文件 {file_name} 上传失败")
        return None

@app.post("/generate_image/")
async def generate_image(request: GenerateImageRequest):
    url = "https://ai.gitee.com/v1/images/generations"

    payload = {
        "model": "Kolors",
        "prompt": request.prompt,
        "n": 1,
        "response_format": "b64_json"
    }
    # print(prompt)
    # print(api_key)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    result = response.json()["data"][0]["b64_json"]

    # 输出图片路径
    filename, output_path2 = base64_to_image(result, output_path)

    print(f"图片已保存到 {output_path2}")

    env = 'test'  # 或 'prod'
    etag = upload_cos(env, filename, output_path)

    return {
        "filename": filename,
        "output_path": output_path2,
        "etag": etag
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)
