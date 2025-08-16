import os
import sys
import json
import requests
import time

from openai import OpenAI

from geekaiapp.g_model import JMRequest
from geekaiapp.g_utils import ai_api_key, ai_base_url, ai_model, system_prompt

# 将项目根目录添加到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
from fastapi import FastAPI, APIRouter, Request, HTTPException
from fastapi.routing import APIRoute, Mount

app = FastAPI(debug=True)

router = APIRouter()

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 获取当前程序运行目录并创建必要的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
temp_dir = os.path.join(current_dir, 'temp')
output_dir = os.path.join(current_dir, 'static')
filters_dir = os.path.join(current_dir, 'filters')
tts_dir = os.path.join(output_dir, 'tts')  # 创建tts子目录
os.makedirs(temp_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)
os.makedirs(tts_dir, exist_ok=True)  # 确保tts目录存在


# 硅基流动大模型服务
client2 = OpenAI(
    api_key=ai_api_key,
    base_url=ai_base_url
)

# g单词比对
@router.post("/dcbd1")
async def get_dps123(request: Request):
    try:
        data = await request.json()
        # print(f'data ={data}')
        text = data.get('content')
        # print(f'text ={text}')
        response = client2.chat.completions.create(
            model=ai_model,
            # messages=messages,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": json.dumps(text, ensure_ascii=False)
                }
            ],
            response_format={
                'type': 'json_object'
            }
        )
        # print(json.loads(response.choices[0].message.content))
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



app.include_router(router, prefix="/api")

# 打印所有路由
for route in app.routes:
    if isinstance(route, APIRoute):  # 检查是否为路由
        print(f"Path: {route.path}, Methods: {route.methods}")
    elif isinstance(route, Mount):  # 检查是否为挂载点
        print(f"Mount: {route.path} -> {route.name}")

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=16005)


# 测试
# curl --location 'http://localhost:16005/api/dcbd1' \
# --header 'Content-Type: application/json' \
# --data '{
#   "content": [
#     {
#       "序号": 1,
#       "汉语": "n.哨兵 n./vt.守卫,保卫,看守",
#       "英语": "guard"
#     },
#     {
#       "序号": 9,
#       "汉语": "n.报酬,奖赏 vt.奖励,奖赏,报答",
#       "英语": "reward"
#     },
#     {
#       "序号": 10,
#       "汉语": "n.保证(书),保修单 vt.保证,提供(产品)保修单",
#       "英语": "quarter"
#     },
#     {
#       "序号": 11,
#       "汉语": "vt.保证 n.令状,凭单,正当理由",
#       "英语": "warrant"
#     },
#     {
#       "序号": 50,
#       "汉语": "n.面纱,遮蔽物 vt.掩饰;[文]遮掩",
#       "英语": "veil"
#     }
#   ]
# }'