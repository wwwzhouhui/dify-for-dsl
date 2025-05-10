import requests
import json
import base64
from PIL import Image
import io
import os
import datetime
import random
import configparser
from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, Form
from openai import OpenAI, APIError, APIConnectionError # <--- 修改: 导入 APIConnectionError
from pydantic import BaseModel
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import logging # <--- 新增导入
from typing import Optional # <--- 新增导入
import httpx # <-- 新增: 导入 httpx 用于代理配置示例
# 读取配置文件
config = configparser.ConfigParser()
# windows
config.read('F:\\work\\code\\2025fastapi\\difyforgitee\\config.ini',encoding='utf-8')
# linux
#config.read('config.ini', encoding='utf-8')

# 设置日志记录器 (如果应用级别没有统一配置, 可以在这里配置基础的)
# logging.basicConfig(level=logging.INFO) # 可选，如果 FastAPI 应用层面已配置则不需要
logger = logging.getLogger(__name__) # <--- 新增

# 从配置文件中读取参数
api_key = config.get('DEFAULT', 'api_key')
output_path = config.get('DEFAULT', 'output_path')
region = config.get('DEFAULT', 'region')
secret_id = config.get('DEFAULT', 'secret_id')
secret_key = config.get('DEFAULT', 'secret_key')
bucket = config.get('DEFAULT', 'bucket')
imageprompt = config.get('DEFAULT', 'imageprompt')
textprompt = config.get('DEFAULT', 'textprompt')
# 配置参数
audiourl = config.get('AudioService', 'url')
package_id = config.get('AudioService', 'package_id')
model = config.get('AudioService', 'model')


app = FastAPI()

class GenerateImageRequest(BaseModel):
    prompt: str

class HiDreamE1Request(BaseModel): # 新增 Pydantic 模型
    prompt: str
    image_base64: Optional[str] = None # <--- 修改: 设置为可选
    imageurl: Optional[str] = None    # <--- 修改: 设置为可选

def generate_timestamp_filename(extension='png'):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    random_number = random.randint(1000, 9999)
    filename = f"{timestamp}_{random_number}.{extension}"
    return filename

def generate_timestamp_filenameforaudio(extension='mp3'):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    random_number = random.randint(1000, 9999)
    filename = f"{timestamp}_{random_number}.{extension}"
    return filename

def base64_to_image(base64_string, output_dir):
    filename = generate_timestamp_filename()
    output_path = os.path.join(output_dir, filename)
    image_data = base64.b64decode(base64_string)
    image = Image.open(io.BytesIO(image_data))
    image.save(output_path)
    print(f"图片已保存到 {output_path}")
    return filename, output_path

def image_to_base64(image_data: bytes) -> str:
    base64_data = base64.b64encode(image_data).decode('utf-8')
    return base64_data

def save_audio_file(audio_content, output_dir):
    # 生成文件名
    filename = generate_timestamp_filenameforaudio()
    # 组合完整的输出路径
    output_path = os.path.join(output_dir, filename)
    with open(output_path, 'wb') as file:
        file.write(audio_content)
    # 返回文件名和输出路径
    return filename, output_path

def upload_cos(env, file_name, base_path):
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

@app.post("/generate_image/")
async def generate_image(request: GenerateImageRequest):
    url = "https://ai.gitee.com/v1/images/generations"
    payload = {
        "model": "Kolors",
        "prompt": request.prompt,
        "n": 1,
        "response_format": "b64_json"
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    result = response.json()["data"][0]["b64_json"]
    filename, output_path2 = base64_to_image(result, output_path)
    etag = upload_cos('test', filename, output_path)
    return {
        "filename": filename,
        "output_path": output_path2,
        "etag": etag
    }

@app.post("/generate_image_to_image/")
async def generate_image_to_image(request: GenerateImageRequest):
    url = "https://ai.gitee.com/api/serverless/Kolors/image-to-image"
    payload = {
        "parameters": {
            "prompt": textprompt,
            "width": 1024,
            "height": 1024,
            "steps": 25,
            "guidance_scale": 6,
            "strength": 0.6,
            "scale": 0.5
        },
        "image": imageprompt,
        "inputs": request.prompt,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "X-Package": "1496"
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    image_data = response.content
    result = image_to_base64(image_data)
    filename, output_path2 = base64_to_image(result, output_path)
    etag = upload_cos('test', filename, output_path)
    return {
        "filename": filename,
        "output_path": output_path2,
        "etag": etag
    }

@app.post("/generate_image_to_imagefile/")
async def generate_image_to_imagefile(file: UploadFile = File(...)):
    file_content = await file.read()
    imageprompt_base64 = image_to_base64(file_content)
    url = "https://ai.gitee.com/api/serverless/Kolors/image-to-image"
    payload = {
        "parameters": {
            "prompt": textprompt,
            "width": 1024,
            "height": 1024,
            "steps": 25,
            "guidance_scale": 6,
            "strength": 0.6,
            "scale": 0.5
        },
        "image": imageprompt,
        "inputs": imageprompt_base64,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "X-Package": "1496"
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    image_data = response.content
    result = image_to_base64(image_data)
    filename, output_path2 = base64_to_image(result, output_path)
    etag = upload_cos('test', filename, output_path)
    return {
        "filename": filename,
        "output_path": output_path2,
        "etag": etag
    }

@app.post("/generate-audio/")
async def generate_audio(request: GenerateImageRequest):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-Package": package_id
    }
    data = {
        "model": model,
        "input": request.prompt
    }
    response = requests.post(audiourl, headers=headers, json=data)

    if response.status_code == 200:
        filename, output_path2 = save_audio_file(response.content, output_path)
        env = 'test'
        etag = upload_cos(env, filename, output_path)
        return {
            "filename": filename,
            "output_path": output_path2,
            "etag": etag
        }
    else:
        raise HTTPException(status_code=response.status_code, detail="请求失败")

@app.post("/generate-HiDream-E1/")
async def generate_hidream_e1(request: HiDreamE1Request):
    client = OpenAI(
            base_url="https://ai.gitee.com/v1",
            api_key=api_key, # 使用从配置文件读取的api_key
            timeout=300.0,  # <-- 修改: 设置请求超时时间为300秒
            max_retries=0  # <-- 新增: 禁用重试
            # http_client=http_client_with_proxy # <-- 新增: 如果使用代理，取消注释此行
     )
    logger.info(f"Received request with prompt: {request.prompt}, imageurl: {request.imageurl}, has_image_base64: {request.image_base64 is not None}")

    base64_encoded_content_to_process: Optional[str] = None

    if request.imageurl:
        logger.info(f"Attempting to process image from URL: {request.imageurl}")
        try:
            async with httpx.AsyncClient(timeout=30.0) as http_client: # 使用 httpx 进行异步 GET 请求
                response = await http_client.get(request.imageurl)
                response.raise_for_status() # 如果状态码是 4xx 或 5xx，则引发 HTTPStatusError
                image_bytes_from_url = response.content
                base64_encoded_content_to_process = base64.b64encode(image_bytes_from_url).decode('utf-8')
                logger.info(f"Successfully downloaded and base64 encoded image from URL: {request.imageurl}")
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error downloading image from {request.imageurl}: {e.response.status_code} - {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail=f"下载图片URL '{request.imageurl}' 时出错: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e: # 处理网络错误、DNS 失败等
            logger.error(f"Request error downloading image from {request.imageurl}: {str(e)}")
            raise HTTPException(status_code=503, detail=f"连接图片URL '{request.imageurl}' 时出错: {str(e)}") # 503 Service Unavailable
        except Exception as e: # 捕获其他意外错误
            logger.error(f"Unexpected error processing image URL {request.imageurl}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"处理图片URL '{request.imageurl}' 时发生意外错误: {str(e)}")
    elif request.image_base64:
        logger.info("Using provided image_base64 from request body.")
        base64_encoded_content_to_process = request.image_base64
    
    if not base64_encoded_content_to_process:
        logger.warning("No image data provided in request (neither imageurl nor image_base64).")
        raise HTTPException(
            status_code=400, 
            detail="未提供图像数据。请提供 'imageurl' 或 'image_base64'。"
        )

    logger.info(f"Proceeding with image processing. Base64 content length (approx): {len(base64_encoded_content_to_process) if base64_encoded_content_to_process else 0}")

    try:
        # 从请求体中获取 prompt (这部分逻辑不变)
        prompt_text = request.prompt
        
        # 将Base64字符串解码为字节
        # 使用 base64_encoded_content_to_process 替代原来的 request.image_base64
        try:
            image_bytes = base64.b64decode(base64_encoded_content_to_process.encode('utf-8'))
        except Exception as e:
            logger.error(f"解码提供的Base64图片数据时出错: {str(e)}") # 增加此处的日志记录
            raise HTTPException(status_code=400, detail=f"无法解码提供的Base64图片数据: {str(e)}")
        logger.info(f"Base64图片数据已成功解码。 Image byte length: {len(image_bytes)}")
        response = client.images.edit(
            model="HiDream-E1-Full",
            image=image_bytes, # 直接传递解码后的图片字节
            prompt=prompt_text, # 使用从请求体中获取的 prompt
            response_format="b64_json",
            extra_body={
                "steps": 28,
                "instruction_following_strength": 5,
                "image_preservation_strength": 3,
                "refinement_strength": 0.3,
                "seed": -1,
            }
        )
        logger.info(f"Received response from Gitee API: {response}")
        if not response.data or not response.data[0].b64_json:
            raise HTTPException(status_code=500, detail="从Gitee API响应中获取base64数据失败。格式不符合预期。")

        result_b64 = response.data[0].b64_json

        filename, output_path_local = base64_to_image(result_b64, output_path)
        logger.info(f"Image saved to {output_path_local}")
        etag = upload_cos('test', filename, output_path)
        logger.info(f"Image uploaded to COS with etag: {etag}")
        if not etag:
            raise HTTPException(status_code=500, detail="上传图片到COS失败。")

        return {
            "filename": filename,
            "output_path": output_path_local, # 保持字段名一致性或明确区分
            "etag": etag
        }
    except APIConnectionError as e: # <-- 新增: 更具体地捕获连接错误
        logger.error(f"Gitee API Connection Error: {e}")
        error_message = (
            f"无法连接到 Gitee API (请求URL: {e.request.url if hasattr(e, 'request') and e.request else 'N/A'}): {str(e)}. "
            "这通常是由于服务器的网络配置问题（例如防火墙、DNS解析、代理服务器设置）或目标服务暂时不可达。 "
            "请检查服务器的网络连通性，并确认是否需要为应用程序配置代理服务器。"
        )
        raise HTTPException(status_code=503, detail=f"Gitee API 连接错误: {error_message}") # 503 Service Unavailable
    except APIError as e:
        logger.error(f"Gitee API Error: {e}")
        error_detail = str(e)
        if hasattr(e, 'message') and e.message:
            error_detail = e.message
        elif hasattr(e, 'response') and e.response is not None:
            try:
                # 尝试解析JSON响应体中的错误信息
                error_content = e.response.json()
                error_detail = error_content.get("error", {}).get("message", str(e.response.content))
            except json.JSONDecodeError: # 如果响应不是有效的JSON
                error_detail = e.response.text # 使用原始文本响应
            except Exception: # 其他解析错误
                 error_detail = str(e.response.content) # Fallback to raw content as string
        # Gitee API 可能会在 status_code 为 4xx/5xx 时返回非 JSON 错误，例如纯文本或 HTML
        # 因此，直接使用 e.response.text 可能更稳妥，如果 JSON 解析失败
        status_code_to_return = e.status_code if hasattr(e, 'status_code') and e.status_code else 500
        raise HTTPException(status_code=status_code_to_return, detail=f"Gitee API 错误: {error_detail}")
    except HTTPException as e:
        logger.error(f"HTTPException: {e}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        # 对于其他未预料到的错误，记录日志并返回通用错误信息
        # import traceback; traceback.print_exc(); # 可选：在服务器端打印详细堆栈信息
        raise HTTPException(status_code=500, detail=f"发生意外错误: {type(e).__name__} - {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)
