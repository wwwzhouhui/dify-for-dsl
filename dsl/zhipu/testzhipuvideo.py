import requests
import time

# 配置服务端 API 地址
BASE_URL = "http://127.0.0.1:8080"  # 替换为您的服务端地址
VIDEO_ENDPOINT = f"{BASE_URL}/zhipuai/video/"

def submit_video_task(prompt: str, with_audio: bool = True):
    """
    提交文生视频任务到服务端。
    :param prompt: 文本提示
    :param with_audio: 是否包含音频，默认为 True
    :return: 视频 URL 和封面图片 URL
    """
    payload = {
        "prompt": prompt,
        "with_audio": with_audio
    }

    try:
        # 发送 POST 请求提交任务
        response = requests.post(VIDEO_ENDPOINT, json=payload)
        if response.status_code != 200:
            print(f"Failed to submit video task. Status code: {response.status_code}, Response: {response.text}")
            return None
        
        result = response.json()
        print("Video task submitted successfully.")
        return result  # 返回视频 URL 和封面图片 URL
    
    except Exception as e:
        print(f"An unexpected error occurred while submitting the video task: {e}")
        return None

def main():
    # 示例：提交一个文生视频任务
    prompt = "比得兔开小汽车，游走在马路上，脸上的表情充满开心喜悦。"
    with_audio = True

    print("Submitting video generation task...")
    result = submit_video_task(prompt, with_audio)

    if result:
        print("Task completed successfully!")
        print(f"Video URL: {result.get('video_url')}")
        print(f"Cover Image URL: {result.get('cover_image_url')}")
    else:
        print("Failed to generate video.")

if __name__ == "__main__":
    main()