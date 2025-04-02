from fastapi import FastAPI, HTTPException,Depends, Header
from pydantic import BaseModel
import logging
import time
import requests
import uuid
import configparser
import json
import os
import datetime
import random
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from fastapi_mcp import add_mcp_server

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Jimeng Video Service API",
    description="一个用于生成AI视频的服务 API",
    version="1.0.0",
)

# 读取配置文件
config = configparser.ConfigParser()
# 在读取配置文件部分添加 COS 配置
#windows 路径(改成你直接的程序目录)
#config.read('e:\\work\\code\\2024pythontest\\jimeng\\config.ini', encoding='utf-8')
config.read('E:\\work\\code\\2025dify-dsl\\dify-for-dsl\\mcp\\fastapi-mcp-server\\jimeng\\config.ini', encoding='utf-8')

#linux 路径
config.read('config.ini', encoding='utf-8')
# 添加 COS 配置读取
region = config.get('common', 'region')
secret_id = config.get('common', 'secret_id')
secret_key = config.get('common', 'secret_key')
bucket = config.get('common', 'bucket')
# 在读取 video_output_path 后添加目录检查和创建逻辑
video_output_path = config.get('common', 'video_output_path')
if not os.path.exists(video_output_path):
    os.makedirs(video_output_path)
    logger.info(f"创建视频输出目录: {video_output_path}")

class VideoRequest(BaseModel):
    prompt: str
    aspect_ratio: str = "16:9"
    duration_ms: int = 5000
    fps: int = 24

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

# 修改视频生成接口，添加鉴权依赖
# 添加新的辅助函数
def generate_timestamp_filename_for_video(extension='mp4'):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    random_number = random.randint(1000, 9999)
    filename = f"video_{timestamp}_{random_number}.{extension}"
    return filename

def download_video(url, output_path):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    filename = generate_timestamp_filename_for_video()
    file_path = os.path.join(output_path, filename)
    
    with open(file_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)
    
    return filename, file_path

def upload_to_cos(region, secret_id, secret_key, bucket, file_name, base_path):
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
    return None

# 修改 generate_video 函数中的返回部分
@app.post("/jimeng/generate_video/")
async def generate_video(request: VideoRequest, auth_token: str = Depends(verify_auth_token)):
    try:
        logger.info(f"generate_video API 调用开始，提示词: {request.prompt}")
        start_time = time.time()
        
        # 从配置文件中获取视频API相关配置
        video_api_cookie = config.get('video_api', 'cookie')
        video_api_sign = config.get('video_api', 'sign')
        
        # 初始化视频生成API相关配置
        video_api_headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'app-sdk-version': '48.0.0',
            'appid': '513695',
            'appvr': '5.8.0',
            'content-type': 'application/json',
            'cookie': video_api_cookie,
            'device-time': str(int(time.time())),
            'lan': 'zh-Hans',
            'loc': 'cn',
            'origin': 'https://jimeng.jianying.com',
            'pf': '7',
            'priority': 'u=1, i',
            'referer': 'https://jimeng.jianying.com/ai-tool/video/generate',
            'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sign': video_api_sign,
            'sign-ver': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
        }
        video_api_base = "https://jimeng.jianying.com/mweb/v1"
        
        # 生成唯一的submit_id
        submit_id = str(uuid.uuid4())
        
        # 准备请求数据
        generate_video_payload = {
            "submit_id": submit_id,
            "task_extra": "{\"promptSource\":\"custom\",\"originSubmitId\":\"0340110f-5a94-42a9-b737-f4518f90361f\",\"isDefaultSeed\":1,\"originTemplateId\":\"\",\"imageNameMapping\":{},\"isUseAiGenPrompt\":false,\"batchNumber\":1}",
            "http_common_info": {"aid": 513695},
            "input": {
                "video_aspect_ratio": request.aspect_ratio,
                "seed": 2934141961,
                "video_gen_inputs": [
                    {
                        "prompt": request.prompt,
                        "fps": request.fps,
                        "duration_ms": request.duration_ms,
                        "video_mode": 2,
                        "template_id": ""
                    }
                ],
                "priority": 0,
                "model_req_key": "dreamina_ic_generate_video_model_vgfm_lite"
            },
            "mode": "workbench",
            "history_option": {},
            "commerce_info": {
                "resource_id": "generate_video",
                "resource_id_type": "str",
                "resource_sub_type": "aigc",
                "benefit_type": "basic_video_operation_vgfm_lite"
            },
            "client_trace_data": {}
        }

        # 发送生成视频请求
        generate_video_url = f"{video_api_base}/generate_video?aid=513695"
        logger.info(f"发送视频生成请求...")
        
        response = requests.post(generate_video_url, headers=video_api_headers, json=generate_video_payload)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail=f"视频生成请求失败，状态码：{response.status_code}")
            
        response_data = response.json()
        if not response_data or "data" not in response_data or "aigc_data" not in response_data["data"]:
            raise HTTPException(status_code=500, detail="视频生成接口返回格式错误")
            
        task_id = response_data["data"]["aigc_data"]["task"]["task_id"]
        logger.info(f"视频生成任务已创建，任务ID: {task_id}")
        
        # 轮询检查视频生成状态
        mget_generate_task_url = f"{video_api_base}/mget_generate_task?aid=513695"
        mget_generate_task_payload = {"task_id_list": [task_id]}
        
        # 最多尝试30次，每次间隔2秒
        for attempt in range(30):
            time.sleep(2)
            logger.info(f"检查视频状态，第 {attempt + 1} 次尝试...")
            
            response = requests.post(mget_generate_task_url, headers=video_api_headers, json=mget_generate_task_payload)
            if response.status_code != 200:
                logger.warning(f"状态检查失败，状态码：{response.status_code}")
                continue
            
            response_data = response.json()
            if not response_data or "data" not in response_data or "task_map" not in response_data["data"]:
                logger.warning("状态检查返回格式错误")
                continue
            
            task_data = response_data["data"]["task_map"].get(task_id)
            if not task_data:
                logger.warning(f"未找到任务 {task_id} 的状态信息")
                continue
            
            task_status = task_data.get("status")
            logger.info(f"任务状态: {task_status}")
            
            if task_status == 50:  # 视频生成完成
                if "item_list" in task_data and task_data["item_list"] and "video" in task_data["item_list"][0]:
                    video_data = task_data["item_list"][0]["video"]
                    if "transcoded_video" in video_data and "origin" in video_data["transcoded_video"]:
                        video_url = video_data["transcoded_video"]["origin"]["video_url"]
                        elapsed_time = time.time() - start_time
                        logger.info(f"视频生成成功，耗时 {elapsed_time:.2f} 秒，URL: {video_url}")
                        
                        # 下载视频到本地
                        try:
                            filename, file_path = download_video(video_url, video_output_path)
                            logger.info(f"视频已下载到本地: {file_path}")
                            
                            # 上传到腾讯 COS
                            cos_url = upload_to_cos(region, secret_id, secret_key, bucket, filename, video_output_path)
                            if cos_url:
                                logger.info(f"视频已上传到 COS: {cos_url}")
                                # 删除本地文件
                                os.remove(file_path)
                                return {
                                    "video_url": cos_url,
                                    "task_id": task_id,
                                    "markdown": f"<video controls><source src='{cos_url}' type='video/mp4'>视频预览</video>"
                                }
                            else:
                                raise HTTPException(status_code=500, detail="上传视频到 COS 失败")
                        except Exception as e:
                            logger.error(f"处理视频文件失败: {str(e)}")
                            raise HTTPException(status_code=500, detail=f"处理视频文件失败: {str(e)}")

                raise HTTPException(status_code=500, detail="视频生成完成但未找到下载地址")
                
        raise HTTPException(status_code=500, detail="视频生成超时")
        
    except Exception as e:
        logger.error(f"视频生成失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# 修改 MCP 服务器配置
mcp_server = add_mcp_server(
    app,
    mount_path="/mcp",
    name="Jimeng Video MCP",
    description="集成了智能视频生成功能的 MCP 服务",
    base_url="http://localhost:8088"
)

# 添加自定义 MCP 工具
@mcp_server.tool()
async def generate_video_mcp(
    prompt: str,
    aspect_ratio: str = "16:9",
    duration_ms: int = 5000,
    fps: int = 24,
    authorization: str = Header(...)
) -> dict:
    """
    生成一个基于文本提示的 AI 视频。

    Args:
        prompt: 用于生成视频的文本提示词
        aspect_ratio: 视频宽高比，默认为 "16:9"
        duration_ms: 视频时长（毫秒），默认为 5000
        fps: 视频帧率，默认为 24
        authorization: Bearer token 用于认证（必填）

    Returns:
        dict: 包含以下字段的字典：
            - video_url: 生成视频的 URL
            - task_id: 任务 ID
            - markdown: 视频预览的 markdown 代码
    """
    request = VideoRequest(
        prompt=prompt,
        aspect_ratio=aspect_ratio,
        duration_ms=duration_ms,
        fps=fps
    )
    return await generate_video(request, auth_token=verify_auth_token(authorization))

if __name__ == "__main__":
    import uvicorn
    # 修改启动配置
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8088,
        log_level="info",
        reload=False  # 禁用热重载以避免初始化问题
    )