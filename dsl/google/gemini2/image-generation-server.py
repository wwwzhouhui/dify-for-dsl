from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import base64
import configparser
import os
import logging
import time
import datetime
import random
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import requests

app = FastAPI()

# 读取配置文件中的API密钥
config = configparser.ConfigParser()
#windows (windows下的路径)
config.read('F:\\work\\code\\2024pythontest\\makehtml\\config.ini', encoding='utf-8')

# Tencent Cloud COS configuration
region = config.get('common', 'region')
secret_id = config.get('common', 'secret_id')
secret_key = config.get('common', 'secret_key')
bucket = config.get('common', 'bucket')

# 设置输出路径
output_path = config.get('google', 'output_path', fallback='picture_output')

# 确保输出目录存在
os.makedirs(output_path, exist_ok=True)

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GenerateImageRequest(BaseModel):
    prompt: str
    model: str = "gemini-2.0-flash-exp-image-generation"
    api_key: str

class EditImageRequest(BaseModel):
    prompt: str
    image_url: str
    model: str = "gemini-2.0-flash-exp-image-generation"
    api_key: str

def generate_timestamp_filename(extension='png'):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    random_number = random.randint(1000, 9999)
    filename = f"{timestamp}_{random_number}.{extension}"
    return filename

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

def download_image(url: str) -> Image.Image:
    try:
        response = requests.get(url)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"下载图片失败: {str(e)}")

@app.post("/gemini/generate-image")
async def generate_image(request: GenerateImageRequest):
    try:
        logger.info("开始处理图片生成请求")
        start_time = time.time()

        client = genai.Client(api_key=request.api_key)
        
        response = client.models.generate_content(
            model=request.model,
            contents=request.prompt,
            config=types.GenerateContentConfig(
                response_modalities=['Text', 'Image']
            )
        )

        result = {"success": True, "data": []}
        
        for part in response.candidates[0].content.parts:
            if part.text is not None:
                result["data"].append({"type": "text", "content": part.text})
            elif part.inline_data is not None:
                try:
                    # 生成文件名
                    filename = generate_timestamp_filename()
                    file_path = os.path.join(output_path, filename)
                    
                    # 解码并保存图片
                    #decoded_data = base64.b64decode(part.inline_data.data)
                    image = Image.open(BytesIO(part.inline_data.data))
                    image.save(file_path)
                    
                    # 上传到腾讯云COS
                    image_url = upload_cos(region, secret_id, secret_key, bucket, filename, output_path)
                    
                    if image_url:
                        result["data"].append({
                            "type": "image",
                            "url": image_url,
                            "filename": filename
                        })
                    else:
                        raise HTTPException(status_code=500, detail="上传图片到COS失败")
                        
                except Exception as e:
                    raise HTTPException(status_code=500, detail=f"处理图像时出现错误: {str(e)}")
        
        elapsed_time = time.time() - start_time
        logger.info(f"图片生成和上传完成，耗时 {elapsed_time:.2f} 秒")
        
        return result

    except Exception as e:
        logger.error(f"处理图片生成请求时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/gemini/generate-editimage")
async def generate_edit_image(request: EditImageRequest):
    try:
        logger.info("开始处理图片编辑请求")
        start_time = time.time()

        # 下载原始图片
        original_image = download_image(request.image_url)
        
        client = genai.Client(api_key=request.api_key)
        
        # 准备输入内容
        contents = [request.prompt, original_image]
        
        response = client.models.generate_content(
            model=request.model,
            contents=contents,
            config=types.GenerateContentConfig(
                response_modalities=['Text', 'Image']
            )
        )

        result = {"success": True, "data": []}
        
        for part in response.candidates[0].content.parts:
            if part.text is not None:
                result["data"].append({"type": "text", "content": part.text})
            elif part.inline_data is not None:
                try:
                    # 生成文件名
                    filename = generate_timestamp_filename()
                    file_path = os.path.join(output_path, filename)
                    
                    # 解码并保存图片
                    #decoded_data = base64.b64decode(part.inline_data.data)
                    image = Image.open(BytesIO(part.inline_data.data))
                    image.save(file_path)
                    
                    # 上传到腾讯云COS
                    image_url = upload_cos(region, secret_id, secret_key, bucket, filename, output_path)
                    
                    if image_url:
                        result["data"].append({
                            "type": "image",
                            "url": image_url,
                            "filename": filename
                        })
                    else:
                        raise HTTPException(status_code=500, detail="上传图片到COS失败")
                        
                except Exception as e:
                    raise HTTPException(status_code=500, detail=f"处理图像时出现错误: {str(e)}")
        
        elapsed_time = time.time() - start_time
        logger.info(f"图片编辑和上传完成，耗时 {elapsed_time:.2f} 秒")
        
        return result

    except Exception as e:
        logger.error(f"处理图片编辑请求时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9090)