import json

def main(arg1: str) -> dict:
    try:
        # 解析外层的 JSON 字符串
        data = json.loads(arg1)
        
        # 检查 success 字段是否为 True
        if not data.get("success", False):
            return {"error": "操作失败，'success' 字段为 False"}
        
        # 提取 data 字段中的 video_url
        video_data = data.get("data")
        if not video_data or "video_url" not in video_data:
            return {"error": "JSON 中缺少 'data.video_url' 字段"}
        
        video_url = video_data["video_url"]
        
        # 定义文件名（可以根据需要调整）
        filename = "生成视频"
        
        # 生成 Markdown 格式的 HTML <video> 标签
        markdown_result = f"<video controls><source src='{video_url}' type='video/mp4'>{filename}</video>"
        
        # 返回结果字典
        return {"result": markdown_result}
    
    except json.JSONDecodeError:
        return {"error": "无效的 JSON 字符串"}
    except Exception as e:
        return {"error": f"发生未知错误: {str(e)}"}
arg1 = '{"success":true,"data":{"video_url":"https://dify-1258720957.cos.ap-nanjing.myqcloud.com/videos/video20250318220955.mp4"},"message":null}'
zz=main(arg1)
print(zz)