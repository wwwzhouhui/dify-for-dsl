import requests
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time
import logging

# 加载配置文件
zhipu_api_key = "b750e148b313df42eef2e96d40174f8b.L10cZAGfaDkzclN2"
zhipu_api_url = "https://open.bigmodel.cn/api/paas/v4"

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 定义 Pydantic 模型用于请求体验证
class VideoRequest(BaseModel):
    prompt: str  # 文本提示
    with_audio: bool = True  # 是否包含音频，默认为 True

# 定义 Pydantic 模型用于响应体
class VideoResponse(BaseModel):
    video_url: str  # 视频 URL
    cover_image_url: str  # 封面图片 URL

# 提交文生视频任务的函数
def submit_video_job(prompt: str, with_audio: bool = True):
    headers = {
        "Authorization": f"Bearer {zhipu_api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "cogvideox-flash",
        "prompt": prompt,
        "with_audio": with_audio
    }
    try:
        response = requests.post(f"{zhipu_api_url}/videos/generations", headers=headers, json=payload, timeout=300)
        if response.status_code != 200:
            logger.error(f"Failed to submit video job. Status code: {response.status_code}, Response: {response.text}")
            raise HTTPException(status_code=response.status_code, detail=f"Failed to submit video job: {response.text}")
        
        submit_response = response.json()
        task_id = submit_response.get("id")
        if not task_id:
            raise HTTPException(status_code=500, detail="Failed to get taskId from submit response.")
        
        logger.info(f"Video generation task submitted successfully. Task ID: {task_id}")
        return task_id
    
    except Exception as e:
        logger.error(f"An unexpected error occurred while submitting the video job: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

# 查询文生视频任务状态的函数
def check_video_status(task_id: str):
    # 正确的请求地址
    status_url = f"https://open.bigmodel.cn/api/paas/v4/async-result/{task_id}"
    headers = {
        "Authorization": f"Bearer {zhipu_api_key}",
        "Content-Type": "application/json",
    }
    
    start_time = time.time()  # 记录开始时间
    logger.info(f"Checking video status for task ID: {task_id}")
    
    while True:
        try:
            # 使用 GET 方法，并通过 URL 参数传递 task_id
            response = requests.get(status_url, headers=headers, timeout=300)
            response.raise_for_status()  # 检查请求是否成功
            status_response = response.json()
            
            task_status = status_response.get("task_status")
            
            if task_status == "SUCCESS":
                logger.info("Task completed successfully.")
                video_result = status_response.get("video_result", [])
                if video_result:
                    video_url = video_result[0].get("url")
                    cover_image_url = video_result[0].get("cover_image_url")
                    return {"video_url": video_url, "cover_image_url": cover_image_url}
                else:
                    raise HTTPException(status_code=500, detail="Missing video result in SUCCESS response.")
            
            elif task_status == "PROCESSING":
                elapsed_time = time.time() - start_time  # 计算已处理时间
                logger.info(f"Task is still in progress. Time elapsed: {int(elapsed_time)} seconds.")
                time.sleep(5)  # 等待 5 秒后再次检查
            
            elif task_status == "FAIL":
                logger.error(f"Task failed. Response: {status_response}")
                raise HTTPException(status_code=500, detail="Task failed during processing.")
            
            else:
                logger.warning(f"Unexpected status: {task_status}")
                raise HTTPException(status_code=500, detail=f"Unexpected task status: {task_status}")
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            time.sleep(5)  # 请求失败时也等待 5 秒再重试

app = FastAPI()

# 提交文生视频任务的接口
@app.post("/zhipuai/video/")
async def submit_video(video_request: VideoRequest):
    """Submits a text-to-video generation job using the ZhipuAI API."""
    try:
        task_id = submit_video_job(video_request.prompt, video_request.with_audio)
        logger.info(f"Video generation task submitted successfully. Task ID: {task_id}")
        
        # 检查任务状态并返回结果
        status_response = check_video_status(task_id)
        return VideoResponse(**status_response)
    
    except HTTPException as err:
        raise err
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

        
# 运行 FastAPI 应用
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)