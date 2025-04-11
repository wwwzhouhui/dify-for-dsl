import configparser
import json

from fastapi import APIRouter, HTTPException, Header, Depends
from loguru import logger

from yewu2story.schemas.video import VideoGenerateRequest, VideoGenerateResponse
from yewu2story.services.video import generate_video

router = APIRouter()

# 读取配置文件中的API密钥
config = configparser.ConfigParser()
# windows (windows下的路径)
# config.read('f:\\work\\code\\2024pythontest\\story\\config.ini', encoding='utf-8')
config.read('./config.ini', encoding='utf-8')


# linux  (linux下的路径)
# config.read('config.ini', encoding='utf-8')

def verify_auth_token(authorization: str = Header(None)):
    """验证 Authorization Header 中的 Bearer Token"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization Header")

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid Authorization Scheme")

    # 从配置文件读取有效token列表
    try:
        valid_tokens = json.loads(config.get('auth', 'valid_tokens'))
        if token not in valid_tokens:
            raise HTTPException(status_code=403, detail="Invalid or Expired Token")
    except (configparser.NoSectionError, configparser.NoOptionError):
        logger.error("配置文件中缺少auth部分或valid_tokens选项")
        raise HTTPException(status_code=500, detail="Server configuration error")

    return token


@router.post("/story/generatestory")
async def generate_video_endpoint(
        request: VideoGenerateRequest,
        auth_token: str = Depends(verify_auth_token)
):
    """生成视频"""
    try:
        result = await generate_video(request)
        # print("video_url::::" + video_url)
        # return VideoGenerateResponse(
        #     success=True,
        #     data={"video_url": video_url,"本地路径":local_url}
        # )
        logger.info(f"接口: {result}")
        return result
    except Exception as e:
        logger.error(f"Failed to generate video: {str(e)}")
        return VideoGenerateResponse(
            success=False,
            message=str(e)
        )
