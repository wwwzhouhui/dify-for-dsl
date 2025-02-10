from fastapi import APIRouter, HTTPException
from openai import OpenAI
import os
from pydantic import BaseModel
from utils.cos_utils import generate_timestamp_filenameforaudio, save_audio_file, upload_cos
from utils.config import load_edgetts_config, common_config

router = APIRouter()

# Load configuration
config = load_edgetts_config()
configcommon = common_config()
api_key = config["openai_api_key"]  # Default to "zhouhuizhou" if not found
base_url = config["openai_base_url"]  # Default URL
output_path = config["output_path"]  # Default output path

# Tencent Cloud COS configuration
region = configcommon["region"]
secret_id = configcommon["secret_id"]
secret_key = configcommon["secret_key"]
bucket = configcommon["bucket"]

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

@router.post("/edgetts/generate-tts/")
async def generate_tts(request_body: TTSRequest):
    """
    Generates text-to-speech audio using the edge tts API and uploads it to Tencent Cloud COS.
    """
    try:
        data = {
            'model': request_body.model,
            'input': request_body.input_text,
            'voice': request_body.voice,
            'response_format': request_body.response_format,
            'speed': request_body.speed,
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
            return {
                "audio_url": audio_url,
                "filename": filename,
                "output_path": output_path2,
                "etag": etag
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to upload audio to COS")
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))