import os
import sys

import requests

from geekaiapp.g_model import JMRequest

# 将项目根目录添加到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
from fastapi import FastAPI, APIRouter
from fastapi.routing import APIRoute, Mount

app = FastAPI(debug=True)

router = APIRouter()

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# g即梦-文生图的接口 https://github.com/LLM-Red-Team/jimeng-free-api
@router.post("/jimeng/img")
async def jm_image(request1: JMRequest):
    headers = {
        "Authorization": f"Bearer {request1.image_api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "model": request1.model,
        "prompt": request1.prompt,
        "negativePrompt": request1.negativePrompt,
        "width": request1.width,
        "height": request1.height,
        "sample_strength": request1.sample_strength,
    }
    try:
        response = requests.post(request1.image_generation_url, headers=headers, json=data)
        response.raise_for_status()  # 检查 HTTP 状态码
        result = response.json()
        return {
            # "url": result["data"][0]["url"]
            "url": result
        }
    except requests.exceptions.RequestException as e:
        raise Exception(f"图像生成 API 请求失败: {e}")
    except (KeyError, IndexError) as e:
        raise Exception(f"图像生成 API 响应解析失败: {e}")


app.include_router(router, prefix="/api")

# 打印所有路由
for route in app.routes:
    if isinstance(route, APIRoute):  # 检查是否为路由
        print(f"Path: {route.path}, Methods: {route.methods}")
    elif isinstance(route, Mount):  # 检查是否为挂载点
        print(f"Mount: {route.path} -> {route.name}")

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=16004)
