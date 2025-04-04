import requests
from pathlib import Path

url = "http://192.168.1.4:8080/beartAI/face-swap"

# 只保留认证头
headers = {
    "Authorization": "Bearer sk-zhouhui111111"  # 替换为实际的认证token
}

# 使用 Path 对象处理路径，避免转义字符问题
source_path = Path(r"D:\\临时\\2025\\2025-4\\2025年4月4日\\1.png")
target_path = Path(r"D:\\临时\\2025\\2025-4\\2025年4月4日\\2.jpeg")

files = {
    "source_image": ("source.jpg", open(source_path, "rb")),
    "target_image": ("target.png", open(target_path, "rb"))
}

response = requests.post(url, files=files, headers=headers)
print(response.json())