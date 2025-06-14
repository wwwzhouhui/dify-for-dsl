# mcp_ai_server.py
import time
import base64
import requests
import asyncio
from typing import Any, Dict, Optional, Union
from openai import OpenAI
from mcp.server.fastmcp import FastMCP

# 创建MCP服务器实例
mcp = FastMCP("AI Generation Server")

# 全局配置
API_KEY = None
BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"

def initialize_client():
    """初始化OpenAI客户端"""
    if not API_KEY:
        raise ValueError("API key is required")
    return OpenAI(api_key=API_KEY, base_url=BASE_URL)

@mcp.tool()
def set_api_key(api_key: str) -> str:
    """设置豆包API密钥"""
    global API_KEY
    API_KEY = api_key
    return "API密钥设置成功"

@mcp.tool()
def text_to_image(
    prompt: str, 
    size: str = "1024x1024", 
    model: str = "doubao-seedream-3-0-t2i-250415"
) -> Dict[str, Any]:
    """
    文生图功能 - 根据文本描述生成图片
    
    Args:
        prompt: 图片描述提示词
        size: 图片尺寸，格式为"宽x高"，如"1024x1024"
        model: 使用的模型名称
    
    Returns:
        包含图片URL或错误信息的字典
    """
    try:
        client = initialize_client()
        
        params = {
            "model": model,
            "prompt": prompt,
            "size": size,
            "response_format": "url",
            "n": 1,
        }
        
        response = client.images.generate(**params)
        
        if response.data and len(response.data) > 0:
            return {
                "success": True,
                "image_url": response.data[0].url,
                "message": "图片生成成功"
            }
        else:
            return {
                "success": False,
                "error": "未返回图片数据"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"生成图片时出错: {str(e)}"
        }

@mcp.tool()
def image_to_video(
    prompt: str,
    image_base64: str,
    duration: str = "5",
    ratio: str = "16:9",
    model: str = "doubao-seedance-1-0-lite-i2v-250428"
) -> Dict[str, Any]:
    """
    图生视频功能 - 根据图片和文本描述生成视频
    
    Args:
        prompt: 视频描述提示词
        image_base64: 图片的base64编码字符串
        duration: 视频时长（秒）
        ratio: 视频比例，如"16:9"
        model: 使用的模型名称
    
    Returns:
        包含视频URL或错误信息的字典
    """
    try:
        # 构造图片数据URL
        image_data_url = f"data:image/jpeg;base64,{image_base64}"
        
        # 自动添加参数到提示词
        if ratio and "--ratio" not in prompt:
            prompt += f" --ratio adaptive"
        if duration and "--duration" not in prompt and "--dur" not in prompt:
            prompt += f" --duration {duration}"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        
        # 构造请求内容
        content = [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": image_data_url}}
        ]
        
        request_data = {
            "model": model,
            "content": content
        }
        
        # 创建视频生成任务
        response = requests.post(
            f"{BASE_URL}/contents/generations/tasks",
            headers=headers,
            json=request_data
        )
        
        if response.status_code != 200:
            return {
                "success": False,
                "error": f"创建视频生成任务失败，状态码: {response.status_code}, 信息: {response.text}"
            }
        
        task_id = response.json().get("id")
        if not task_id:
            return {
                "success": False,
                "error": "未获取到任务ID"
            }
        
        # 轮询等待任务完成
        max_retries = 60
        for retry in range(max_retries):
            time.sleep(5)
            
            task_resp = requests.get(
                f"{BASE_URL}/contents/generations/tasks/{task_id}",
                headers=headers
            )
            
            if task_resp.status_code != 200:
                return {
                    "success": False,
                    "error": f"查询任务失败，状态码: {task_resp.status_code}"
                }
            
            task_data = task_resp.json()
            status = task_data.get("status")
            
            if status == "succeeded":
                video_url = task_data.get("content", {}).get("video_url")
                return {
                    "success": True,
                    "video_url": video_url,
                    "message": "视频生成成功",
                    "task_id": task_id
                }
            elif status in ("failed", "canceled"):
                return {
                    "success": False,
                    "error": f"任务{status}"
                }
        
        return {
            "success": False,
            "error": "视频生成超时"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"生成视频时出错: {str(e)}"
        }

@mcp.tool()
def text_to_video(
    prompt: str,
    duration: str = "5",
    ratio: str = "16:9",
    model: str = "doubao-seedance-1-0-lite-t2v-250428"
) -> Dict[str, Any]:
    """
    文生视频功能 - 根据文本描述生成视频
    
    Args:
        prompt: 视频描述提示词
        duration: 视频时长（秒）
        ratio: 视频比例，如"16:9"
        model: 使用的模型名称
    
    Returns:
        包含视频URL或错误信息的字典
    """
    try:
        # 自动添加参数到提示词
        if ratio and "--ratio" not in prompt:
            prompt += f" --ratio {ratio}"
        if duration and "--duration" not in prompt and "--dur" not in prompt:
            prompt += f" --duration {duration}"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        
        request_data = {
            "model": model,
            "content": [{"type": "text", "text": prompt}]
        }
        
        # 创建视频生成任务
        response = requests.post(
            f"{BASE_URL}/contents/generations/tasks",
            headers=headers,
            json=request_data
        )
        
        if response.status_code != 200:
            return {
                "success": False,
                "error": f"创建视频生成任务失败，状态码: {response.status_code}, 信息: {response.text}"
            }
        
        task_id = response.json().get("id")
        if not task_id:
            return {
                "success": False,
                "error": "未获取到任务ID"
            }
        
        # 轮询等待任务完成
        max_retries = 60
        for retry in range(max_retries):
            time.sleep(5)
            
            task_resp = requests.get(
                f"{BASE_URL}/contents/generations/tasks/{task_id}",
                headers=headers
            )
            
            if task_resp.status_code != 200:
                return {
                    "success": False,
                    "error": f"查询任务失败，状态码: {task_resp.status_code}"
                }
            
            task_data = task_resp.json()
            status = task_data.get("status")
            
            if status == "succeeded":
                video_url = task_data.get("content", {}).get("video_url")
                return {
                    "success": True,
                    "video_url": video_url,
                    "message": "视频生成成功",
                    "task_id": task_id
                }
            elif status in ("failed", "canceled"):
                return {
                    "success": False,
                    "error": f"任务{status}"
                }
        
        return {
            "success": False,
            "error": "视频生成超时"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"生成视频时出错: {str(e)}"
        }

@mcp.tool()
def encode_image_to_base64(image_path: str) -> Dict[str, Any]:
    """
    将本地图片文件编码为base64字符串
    
    Args:
        image_path: 图片文件路径
    
    Returns:
        包含base64编码字符串或错误信息的字典
    """
    try:
        with open(image_path, 'rb') as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            return {
                "success": True,
                "base64_string": encoded_string,
                "message": "图片编码成功"
            }
    except Exception as e:
        return {
            "success": False,
            "error": f"编码图片失败: {str(e)}"
        }

@mcp.resource("config://models")
def get_available_models() -> str:
    """获取可用的AI模型列表"""
    models = {
        "text_to_image": [
            "doubao-seedream-3-0-t2i-250415"
        ],
        "image_to_video": [
            "doubao-seedance-1-0-lite-i2v-250428"
        ],
        "text_to_video": [
            "doubao-seedance-1-0-lite-t2v-250428"
        ]
    }
    return f"可用模型列表: {models}"

@mcp.resource("config://settings")
def get_server_settings() -> str:
    """获取服务器配置信息"""
    settings = {
        "base_url": BASE_URL,
        "api_key_set": bool(API_KEY),
        "supported_image_sizes": ["512x512", "768x768", "1024x1024", "1024x1792", "1792x1024"],
        "supported_video_ratios": ["16:9", "9:16", "1:1"],
        "max_video_duration": "10s"
    }
    return f"服务器配置: {settings}"

if __name__ == "__main__":
    mcp.settings.host  = "0.0.0.0"
    mcp.settings.port = 8002
    mcp.run(transport="sse")
