from fastapi import FastAPI, HTTPException, Query
import json
import requests
import time
from pydantic import BaseModel, ValidationError
import datetime
import random
import os
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
app = FastAPI()

class VideoSubmission(BaseModel):
    prompt: str
    model: str


class AudioSubmission(BaseModel):
    input: str
    model: str
    voice: str

def load_config(config_file):
    with open(config_file, 'r', encoding='utf-8') as file:
       return json.load(file)

config = load_config('config.json')
api_url = config["api_url"]
auth_token = config["authorization_token"]
region = config["region"]
secret_id = config["secret_id"]
secret_key = config["secret_key"]
bucket = config["bucket"]
output_path = config["output_path"]
audiomodel = config["audiomodel"]
voice=config["voice"]

def submit_video_job(api_url, auth_token, model, prompt):
    submit_url = f"{api_url}/video/submit"
    payload = json.dumps({
        "model": model,
        "prompt": prompt
    })
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(submit_url, headers=headers, data=payload)
    return response.json()

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
def check_video_status(api_url, auth_token, request_id, timeout=200):
    status_url = f"{api_url}/video/status"
    payload = json.dumps({"requestId": request_id})
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json'
    }
    start_time = time.time()
    while True:
        response = requests.post(status_url, headers=headers, data=payload)
        status_response = response.json()
        if status_response.get("status") == "Succeed":
            return status_response
        elif status_response.get("status") == "InProgress":
            if time.time() - start_time > timeout:
                print("Timeout waiting for video status.")
                return None
            time.sleep(5)
        else:
            print("Unexpected status:", status_response.get("status"))
            return None


@app.post("/submit-video/")
async def submit_video(video_submission: VideoSubmission):
    # Use the model from the user input if provided, otherwise use the default from config
    model = video_submission.model if video_submission.model else config["model"]

    submit_response = submit_video_job(api_url, auth_token, model, video_submission.prompt)
    if "error" in submit_response:
        raise HTTPException(status_code=500, detail=submit_response["error"])

    request_id = submit_response.get("requestId")
    if not request_id:
        raise HTTPException(status_code=500, detail="Failed to get requestId from submit response.")

    status_response = check_video_status(api_url, auth_token, request_id)
    if status_response and status_response.get("status") == "Succeed" and status_response.get("results") and status_response["results"].get("videos") and len(status_response["results"]["videos"]) > 0:
        video_url = status_response['results']['videos'][0]['url']
        return {"video_url": video_url}
    else:
        raise HTTPException(status_code=500, detail="Invalid status response or missing video URL.")

@app.post("/generate-audio/")
async def generate_audio(audio_Submission: AudioSubmission):
    audiourl=api_url+"/audio/speech"
    audiomodel2 = audio_Submission.model if audio_Submission.model else audiomodel
    voice2 = audio_Submission.voice if audio_Submission.voice else voice
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
    data = {
        "model": audiomodel2,
        "input": audio_Submission.input,
        "voice": voice2,
        "response_format": "mp3",
        "sample_rate": 32000,
        "stream": True,
        "speed": 1,
        "gain": 0
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
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8084)
