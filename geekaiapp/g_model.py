from fastapi import UploadFile, File
from pydantic import BaseModel


class VideoSubmission(BaseModel):
    prompt: str
    model: str


class AudioSubmission(BaseModel):
    input: str
    model: str
    voice: str


class TTSRequest(BaseModel):
    input: str = "测试"
    voice: str = "zh-CN-XiaoxiaoNeural"
    model: str = "tts-1"
    speed: float = 1.0
    response_format: str = "mp3"


class Item1(BaseModel):
    description: str
    prompt: str
    text_snippet: str
    importance: str


class VideoRequest3(BaseModel):
    source_image: UploadFile = File(...)
    target_image: UploadFile = File(...)


class VideoRequest2(BaseModel):
    prompt: str
    aspect_ratio: str = "16:9"
    duration_ms: int = 5000
    fps: int = 24


# 定义 Pydantic 模型用于请求体验证
class VideoRequest(BaseModel):
    prompt: str  # 文本提示
    with_audio: bool = True  # 是否包含音频，默认为 True


# 定义 Pydantic 模型用于响应体
class VideoResponse(BaseModel):
    video_url: str  # 视频 URL
    cover_image_url: str  # 封面图片 URL


class JMRequest(BaseModel):
    image_api_key: str = "image_api_key"
    image_generation_url: str = "image_generation_url"
    model: str = "jimeng-2.1"
    prompt: str = "皮卡丘抱着埃菲尔铁塔"
    negativePrompt: str = ""
    width: int = 1080
    height: int = 720
    sample_strength: float = 0.5
