import os
import subprocess
import sys
import time

from fastapi import Request

from geekaiapp.g_model import TTSRequest

# 将项目根目录添加到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.routing import APIRoute, Mount
from openai import OpenAI

from geekaiapp.g_utils import upload_cos, tencent_region, tencent_secret_id, \
    tencent_secret_key, tencent_bucket, ip_md, microsoft_api_key, microsoft_base_url, save_audio_file, \
    current_directory, ip_tts, ip

app = FastAPI(debug=True)

router = APIRouter()

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 微软服务
client = OpenAI(
    api_key=microsoft_api_key,
    base_url=microsoft_base_url
)


# g微软的文生音，并上传到腾讯oss
@router.post("/edge/tts12")
async def generate_tts12(request_body: TTSRequest):
    """
    Generates text-to-speech audio using the edge tts API and uploads it to Tencent Cloud COS.
    """
    try:
        data = {
            'model': request_body.model,
            'input': request_body.input,
            'voice': request_body.voice,
            'response_format': request_body.response_format,
            'speed': request_body.speed,
        }
        response = client.audio.speech.create(
            **data
        )
        # Save the audio file
        filename, output_path2 = save_audio_file(response.content, tts_dir)
        audio_url = f"{ip}{ip_tts}/{filename}"
        # Upload to COS
        etag = upload_cos('text1', tencent_region, tencent_secret_id, tencent_secret_key, tencent_bucket, filename,
                          tts_dir)
        if etag:
            audio_url2 = f"https://{tencent_bucket}.cos.{tencent_region}.myqcloud.com/{filename}"
            return {
                "audio_url": audio_url2,
                "filename": filename,
                "output_path": audio_url,
                "etag": etag
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to upload audio to COS")
    except Exception as e:
        print(f"An error occurred: {e}")
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
    uvicorn.run(app, host="0.0.0.0", port=16003)
