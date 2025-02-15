from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
import json
from openai import OpenAI
import logging
import time  # 导入 time 模块用于计算耗时
import requests
from typing import List
import uvicorn
import configparser
import os
import datetime
import random
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
app = FastAPI()


# 读取配置文件中的API密钥
config = configparser.ConfigParser()
#config.read('E:\\work\\code\\2024pythontest\\jimeng\\config.ini',encoding='utf-8')  # 假设配置文件名为config.ini，并且API密钥在[DEFAULT]部分
config.read('config.ini',encoding='utf-8')
image_generation_url = config.get('DEFAULT', 'image_generation_url')
audio_generation_url = config.get('DEFAULT', 'audio_generation_url')
image_api_key = config.get('DEFAULT', 'image_api_key')
audio_model = config.get('DEFAULT', 'audio_model')
audio_voice = config.get('DEFAULT', 'audio_voice')
tts_model = config.get('DEFAULT', 'tts_model')
tts_voice = config.get('DEFAULT', 'tts_voice')
speed = config.get('DEFAULT', 'speed')
response_format = config.get('DEFAULT', 'response_format')

# Tencent Cloud COS configuration
region = config.get('common', 'region')
secret_id = config.get('common', 'secret_id')
secret_key = config.get('common', 'secret_key')
bucket = config.get('common', 'bucket')

# Load configuration
api_key = config.get('edgetts', 'openai_api_key')
base_url = config.get('edgetts', 'openai_base_url')
output_path = config.get('edgetts', 'output_path')

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

# 定义请求体模型
class TTSRequest(BaseModel):
    input_text: str
    voice: str = "zh-CN-XiaoxiaoNeural"
    model: str = "tts-1"
    speed: float = 1.0
    response_format: str = "mp3"

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Item(BaseModel):
    description: str
    prompt: str
    text_snippet: str
    importance: str

@app.post("/process-data/")
async def process_data(item: Item):
    try:
        logger.info(f"process_data 调用 generate_image API 开始")
        # 记录图像生成的开始时间
        start_time_image = time.time()
        image_url = await generate_image(item.prompt)
        # 计算图像生成耗时
        elapsed_time_image = time.time() - start_time_image
        logger.info(f"process_data 调用 generate_image API 结束，耗时 {elapsed_time_image:.2f} 秒，返回 image_url: {image_url}")

        logger.info(f"process_data 调用 generate_audio API 开始")
        # 记录音频生成的开始时间
        start_time_audio = time.time()
        #audio_url = await generate_audio(item.text_snippet)
        audio_url = await generate_tts(item.text_snippet)
        # 计算音频生成耗时
        elapsed_time_audio = time.time() - start_time_audio
        logger.info(f"process_data 调用 generate_audio API 结束，耗时 {elapsed_time_audio:.2f} 秒，返回 audio_url: {audio_url}")

        return {
            "description": item.text_snippet,
            "image_url": image_url,
            "audio_url": audio_url,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def generate_timestamp_filenameforaudio(extension='mp3'):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    random_number = random.randint(1000, 9999)
    filename = f"{timestamp}_{random_number}.{extension}"
    return filename
def save_audio_file(audio_content, output_dir):
    # 生成文件名
    filename = generate_timestamp_filenameforaudio()
    # 组合完整的输出路径
    output_path = os.path.join(output_dir, filename)
    with open(output_path, 'wb') as file:
        file.write(audio_content)
    # 返回文件名和输出路径
    return filename, output_path

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

async def generate_image(prompt: str):
    headers = {
        "Authorization": f"Bearer {image_api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "jimeng-2.1",
        "prompt": prompt,
        "negativePrompt": "",
        "width": 1024,
        "height": 1024,
        "sample_strength": 0.5,
    }
    try:
        response = requests.post(image_generation_url, headers=headers, json=data)
        response.raise_for_status()  # 检查 HTTP 状态码
        result = response.json()
        return result["data"][0]["url"]
    except requests.exceptions.RequestException as e:
        raise Exception(f"图像生成 API 请求失败: {e}")
    except (KeyError, IndexError) as e:
        raise Exception(f"图像生成 API 响应解析失败: {e}")


async def generate_tts(text_snippet: str):
    """
    Generates text-to-speech audio using the edge tts API and uploads it to Tencent Cloud COS.
    """
    try:
        data = {
            'model': tts_model,
            'input': text_snippet,
            'voice': tts_voice,
            'response_format': response_format,
            'speed': speed,
        }
        response = client.audio.speech.create(
            **data
        )
        # Save the audio file
        filename, output_path2 = save_audio_file(response.content, output_path)
        # Upload to COS
        etag = upload_cos(region, secret_id, secret_key, bucket, filename, output_path)
        if etag:
            audio_url = f"https://{bucket}.cos.{region}.myqcloud.com/{filename}"
            return audio_url
        else:
            raise HTTPException(status_code=500, detail="Failed to upload audio to COS")
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def generate_audio(text_snippet: str):
    headers = {"Content-Type": "application/json"}
    data = {
        "input": text_snippet,
        "model": audio_model,
        "voice": audio_voice,
    }
    try:
        response = requests.post(audio_generation_url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result["etag"]
    except requests.exceptions.RequestException as e:
        raise Exception(f"音频生成 API 请求失败: {e}")
    except KeyError as e:
        raise Exception(f"音频生成 API 响应解析失败: {e}")


@app.post("/make_AI_picture_audio/")
async def make_ai_picture_audio(data: List[Item]):
    try:
        results = []
        for item in data:
            result = await process_data(item)
            results.append(result)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8087)