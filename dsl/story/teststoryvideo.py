import requests
import json
from typing import Optional, Dict, Any
import configparser
import os
import time

class StoryVideoClient:
    def __init__(self, base_url: str = "http://192.168.1.3:8085", api_token: str = None):
        self.base_url = base_url.rstrip('/')
        self.api_token = "zhouhui-1258720957"

    async def generate_video(self, 
        story_prompt: Optional[str] = None,
        segments: int = 3,
        language: str = "zh-CN",
        test_mode: bool = False,
        task_id: Optional[str] = None,
        voice_name: str = "zh-CN-XiaoxiaoNeural",
        voice_rate: float = 1.0,
        resolution: str = "1024*1024",
        # 添加 LLM 提供商和模型参数
        text_llm_provider: Optional[str] = "siliconflow",
        image_llm_provider: Optional[str] = "siliconflow",
        text_llm_model: Optional[str] = "Qwen/QwQ-32B",
        image_llm_model: Optional[str] = "black-forest-labs/FLUX.1-schnell"
    ) -> Dict[str, Any]:
        # 记录开始时间
        start_time = time.time()
        
        url = f"{self.base_url}/story/generatestory"
        
        data = {
            "story_prompt": story_prompt,
            "segments": segments,
            "language": language,
            "test_mode": test_mode,
            "task_id": task_id,
            "voice_name": voice_name,
            "voice_rate": voice_rate,
            "resolution": resolution,
            "text_llm_provider": text_llm_provider,
            "image_llm_provider": image_llm_provider,
            "text_llm_model": text_llm_model,
            "image_llm_model": image_llm_model
        }
        
        # 添加授权头
        headers = {}
        if self.api_token:
            headers["Authorization"] = f"Bearer {self.api_token}"
        else:
            print("警告: 未提供API令牌，请求可能会被拒绝")

        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            result = response.json()
            
            # 记录结束时间并计算耗时
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"视频生成总耗时: {elapsed_time:.2f} 秒")
            
            return result
        except requests.exceptions.RequestException as e:
            # 发生异常时也记录耗时
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"请求失败，总耗时: {elapsed_time:.2f} 秒")
            raise Exception(f"Failed to generate video: {str(e)}")

# 使用示例
async def main():
    # 记录主函数开始时间
    main_start_time = time.time()
    
    # 可以在创建客户端时直接提供API令牌
    client = StoryVideoClient(api_token="your_api_token_here")
    try:
        result = await client.generate_video(
            story_prompt="讲一个机器猫的故事",
            segments=3,
            voice_name="zh-CN-XiaoxiaoNeural",
            voice_rate=1.0,
            text_llm_provider="siliconflow",
            #text_llm_provider="intern",
            image_llm_provider="siliconflow",
            text_llm_model="Qwen/QwQ-32B",
            #text_llm_model="internlm3-latest",
            image_llm_model="black-forest-labs/FLUX.1-schnell"
        )
        if result["success"]:
            print(f"视频生成成功: {result['data']['video_url']}")
        else:
            print(f"视频生成失败: {result.get('message', '未知错误')}")
    except Exception as e:
        print(f"发生错误: {str(e)}")
    finally:
        # 计算并打印主函数总耗时
        main_end_time = time.time()
        main_elapsed_time = main_end_time - main_start_time
        print(f"程序总执行时间: {main_elapsed_time:.2f} 秒")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())