import requests
from PIL import Image
from io import BytesIO
import base64

#def generate_image(prompt: str, api_key: str, server_url: str = "http://111.119.215.74:8080"):
def generate_image(prompt: str, api_key: str, server_url: str = "http://127.0.0.1:9090"):
    # 构建请求数据
    payload = {
        "prompt": prompt,
        "model": "gemini-2.0-flash-exp-image-generation",
        "api_key": api_key
    }

    try:
        # 发送请求
        response = requests.post(f"{server_url}/gemini/generate-image", json=payload)
        response.raise_for_status()
        
        # 处理响应
        result = response.json()
        
        if result["success"]:
            for item in result["data"]:
                if item["type"] == "text":
                    print(item["content"])
                elif item["type"] == "image":
                    print(f"图片URL: {item['url']}")
                    print(f"图片文件名: {item['filename']}")
        
        return result
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
        return None

#def edit_image(prompt: str, image_url: str, api_key: str, server_url: str = "http://111.119.215.74:8080"):
def edit_image(prompt: str, image_url: str, api_key: str, server_url: str = "http://127.0.0.1:9090"):
    # 构建请求数据
    payload = {
        "prompt": prompt,
        "image_url": image_url,
        "model": "gemini-2.0-flash-exp-image-generation",
        "api_key": api_key
    }

    try:
        # 发送请求
        response = requests.post(f"{server_url}/gemini/generate-editimage", json=payload)
        response.raise_for_status()
        
        # 处理响应
        result = response.json()
        
        if result["success"]:
            for item in result["data"]:
                if item["type"] == "text":
                    print(item["content"])
                elif item["type"] == "image":
                    print(f"编辑后的图片URL: {item['url']}")
                    print(f"编辑后的图片文件名: {item['filename']}")
        
        return result
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
        return None

if __name__ == "__main__":
    # 使用示例 - 生成图片
    prompt = ('Two crabs fighting on the beach')
    api_key = 'xxxxxxx'  # 替换为你的API密钥
    
    result = generate_image(prompt, api_key)
    
    # 使用示例 - 编辑图片
    if result and result["success"] and any(item["type"] == "image" for item in result["data"]):
        # 获取生成的图片URL
        image_url = next(item["url"] for item in result["data"] if item["type"] == "image")
        
        edit_prompt = "There was a little boy by the sea"
        edit_image(edit_prompt, image_url, api_key)
