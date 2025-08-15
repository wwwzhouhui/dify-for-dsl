import json
import requests
from typing import Any, List, Dict
from mcp.server.fastmcp import FastMCP
from openai import OpenAI
#from zhipuai import ZhipuAI pip install --upgrade "volcengine-python-sdk[ark]"
from volcenginesdkarkruntime import Ark
import os

# 初始化MCP服务器
mcp = FastMCP("ZhongyiServer", port=8001)
client = OpenAI(api_key="sk-c4c99fecf0bb4a09bd5b74d21a728ef5", base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

# 初始化Ark客户端（建议将API Key存储在环境变量 ARK_API_KEY 中）
clientArk = Ark(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=os.getenv("ARK_API_KEY", "d160b0a1-ca46-43d0-8b0d-4b143ed65ae8")  # 建议安全存储
)
#clientZhiPu = ZhipuAI(api_key="b750e148b313df42eef2e96d40174f8b.L10cZAGfaDkzclN2")
@mcp.tool()
async def get_yaocaiInfo(yaocai: str):
    """
    输入指定药材的名称，返回当前药材信息
    :param yaocai: 药材名称
    :return: json格式的药材信息
    """
    try:
        # 构建提示词
        prompt = f"""请以JSON格式返回关于"{yaocai}"的中药材信息，包含以下字段：
        1. name: 药材名称
        2. property: 药性（寒、热、温、凉）
        3. taste: 药味（酸、苦、甘、辛、咸）
        4. meridian: 归经
        5. function: 功效主治
        6. usage: 用法用量
        请确保返回的是合法的JSON格式。
        """
        
        # 调用DeepSeek API
        response = client.chat.completions.create(
            model="qwen-plus-1220",
            messages=[
                {"role": "system", "content": "你是一个专业的中医药专家，请提供准确的中药材信息。"},
                {"role": "user", "content": prompt}
            ],
            stream=False
        )
        
        # 获取回复并确保是JSON格式
        result = response.choices[0].message.content
        # 尝试解析JSON，如果失败则返回原始文本
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return {"error": "无法解析为JSON格式", "raw_content": result}
            
    except Exception as e:
        return {"error": f"获取药材信息出错：{str(e)}"}

# 添加一个工具,获取药材的图片
@mcp.tool()
async def get_yaocai_image(yaocai: str):
    """
    输入指定药材的名称，返回当前药材的图片
    :param yaocai: 药材名称
    :return: 药材的图片URL
    """
    try:
        # 构建提示词
        prompt = f"高清晰度的{yaocai}中药材实物图片，清晰展示其外观特征，包括颜色、形状和质地，白色背景，专业医药参考图"
        
        # 调用火山方舟 Doubao Seedream 图像生成API
        imagesResponse = clientArk.images.generate(
            model="doubao-seedream-3-0-t2i-250415",
            prompt=prompt
        )
        
        # 返回生成的图片URL
        return {
            "success": True,
            "image_url": imagesResponse.data[0].url,
            "yaocai": yaocai
        }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"获取药材图片出错：{str(e)}",
            "yaocai": yaocai
        }

# http://14.103.204.132:8003/sse
# http://192.168.31.115:15501/sse
if __name__ == "__main__":
    mcp.settings.host  = "0.0.0.0"
    mcp.settings.port = 15803
    mcp.run(transport="sse")
