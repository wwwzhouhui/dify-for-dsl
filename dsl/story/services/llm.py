from openai import OpenAI
from loguru import logger
from typing import List, Dict, Any
import json
from http import HTTPStatus
from pathlib import PurePosixPath
import requests
from urllib.parse import urlparse, unquote
import random

from models.const import LANGUAGE_NAMES, Language
from exceptions import LLMResponseValidationError
import dashscope

from dashscope import ImageSynthesis
from schemas.llm import (
    StoryGenerationRequest,
)
import configparser

# 读取配置文件中的API密钥
config = configparser.ConfigParser()
#windows (windows下的路径)
config.read('f:\\work\\code\\2024pythontest\\story\\config.ini', encoding='utf-8')
#linux  (linux下的路径)
#config.read('config.ini', encoding='utf-8')

# # 创建全局配置实例
# settings = Config()
# llm_config = settings.llm_config
openai_api_key = config.get('llm', 'openai_api_key')
openai_base_url = config.get('llm', 'openai_base_url')
aliyun_api_key = config.get('llm', 'aliyun_api_key')
aliyun_base_url = config.get('llm', 'aliyun_base_url')
deepseek_api_key = config.get('llm', 'deepseek_api_key')
deepseek_base_url = config.get('llm', 'deepseek_base_url')
ollama_api_key = config.get('llm', 'ollama_api_key')
ollama_base_url = config.get('llm', 'ollama_base_url')
siliconflow_api_key = config.get('llm', 'siliconflow_api_key')
siliconflow_base_url = config.get('llm','siliconflow_base_url')
intern_base_url = config.get('llm', 'intern_base_url')
intern_api_key = config.get('llm', 'intern_api_key')
text_llm_model = config.get('llm', 'text_llm_model')
image_llm_model = config.get('llm', 'image_llm_model')

# 打印配置信息
print("OpenAI API Key:", openai_api_key)
print("OpenAI Base URL:", openai_base_url)
print("Aliyun API Key:", aliyun_api_key)
print("Aliyun Base URL:", aliyun_base_url)
print("Deepseek API Key:", deepseek_api_key)
print("Deepseek Base URL:", deepseek_base_url)
print("Ollama API Key:", ollama_api_key)
print("Ollama Base URL:", ollama_base_url)
print("Siliconflow API Key:", siliconflow_api_key)
print("Siliconflow Base URL:", siliconflow_base_url)
print("Text LLM Model:", text_llm_model)
print("Image LLM Model:", image_llm_model)
print("intern API Key:", intern_api_key)
print("intern Base URL:", intern_base_url)


openai_client = None
if openai_api_key:
   openai_client = OpenAI(api_key=openai_api_key, base_url=openai_base_url)

aliyun_text_client = None
if aliyun_api_key:
    dashscope.api_key = aliyun_api_key
    aliyun_text_client = OpenAI(base_url=aliyun_base_url, api_key=aliyun_api_key) 

if deepseek_api_key:
    deepseek_client = OpenAI(api_key=deepseek_api_key, base_url=deepseek_base_url)

if ollama_api_key:
    ollama_client = OpenAI(api_key=ollama_api_key, base_url=ollama_base_url)

if siliconflow_api_key:
    siliconflow_client = OpenAI(api_key=siliconflow_api_key, base_url=siliconflow_base_url)

if intern_api_key:
    intern_client = OpenAI(api_key=intern_api_key, base_url=intern_base_url)

class LLMService:
    def __init__(self):
        self.openai_client = openai_client
        self.aliyun_text_client = aliyun_text_client
        self.text_llm_model = text_llm_model
        self.image_llm_model = image_llm_model
    
    async def generate_story(self, request: StoryGenerationRequest) -> List[Dict[str, Any]]:
        """生成故事场景
        Args:
            story_prompt (str, optional): 故事提示. Defaults to None.
            segments (int, optional): 故事分段数. Defaults to 3.

        Returns:
            List[Dict[str, Any]]: 故事场景列表
        """
        
        messages = [
            {"role": "system", "content": "你是一个专业的故事创作者，善于创作引人入胜的故事。请只返回JSON格式的内容。"},
            {"role": "user", "content": await self._get_story_prompt(request.story_prompt, request.language, request.segments)}
        ]
        logger.info(f"prompt messages: {json.dumps(messages, indent=4, ensure_ascii=False)}")
        response = await self._generate_response(text_llm_provider = request.text_llm_provider or None, text_llm_model = request.text_llm_model or None, messages=messages, response_format="json_object")
        response = response["list"]
        response = self.normalize_keys(response)

        logger.info(f"Generated story: {json.dumps(response, indent=4, ensure_ascii=False)}")
        # 验证响应格式
        self._validate_story_response(response)
        
        return response
    def normalize_keys(self, data):
        """
        阿里云和 openai 的模型返回结果不一致，处理一下
        修改对象中非 `text` 的键为 `image_prompt`
        - 如果是字典，替换 `text` 以外的单个键为 `image_prompt`
        - 如果是列表，对列表中的每个对象递归处理
        """
        if isinstance(data, dict):
            # 如果是字典，处理键值
            if "text" in data:
                # 找到非 `text` 的键
                other_keys = [key for key in data.keys() if key != "text"]
                # 确保只处理一个非 `text` 键的情况
                if len(other_keys) == 1:
                    data["image_prompt"] = data.pop(other_keys[0])
                elif len(other_keys) > 1:
                    raise ValueError(f"Unexpected extra keys: {other_keys}. Only one non-'text' key is allowed.")
            return data
        elif isinstance(data, list):
            # 如果是列表，递归处理每个对象
            return [self.normalize_keys(item) for item in data]
        else:
            raise TypeError("Input must be a dict or list of dicts")

    def generate_image(self, *, prompt: str, image_llm_provider: str = None, image_llm_model: str = None, resolution: str = "1024x1024") -> str:
        # return "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/1d/56/20250118/3c4cc727/4fc622b5-54a6-484c-bf1f-f1cfb66ace2d-1.png?Expires=1737290655&OSSAccessKeyId=LTAI5tQZd8AEcZX6KZV4G8qL&Signature=W8D4CN3uonQ2pL1e9xGMWufz33E%3D"
        """生成图片

        Args:
            prompt (str): 图片描述
            resolution (str): 图片分辨率，默认为 1024x1024

        Returns:
            str: 图片URL
        """

        try:
            # 添加安全提示词
            safe_prompt = f"Create a safe, family-friendly illustration. {prompt} The image should be appropriate for all ages, non-violent, and non-controversial."
            
            if image_llm_provider == "aliyun":
                rsp = ImageSynthesis.call(model=image_llm_model,
                              prompt=prompt,
                              size=resolution,)
                if rsp.status_code == HTTPStatus.OK:
                    # print("aliyun image response", rsp.output)
                    for result in rsp.output.results:
                        return result.url
                else:
                    error_message = f'Failed, status_code: {rsp.status_code}, code: {rsp.code}, message: {rsp.message}'
                    logger.error(error_message)
                    raise Exception(error_message)
            elif image_llm_provider == "openai":
                if (resolution != None):
                    resolution = resolution.replace("*", "x")
                response = self.openai_client.images.generate(
                    model=image_llm_model,
                    prompt=safe_prompt,
                    size=resolution,
                    quality="standard",
                    n=1
                )
                logger.info("image generate res", response.data[0].url)
                return response.data[0].url
            elif image_llm_provider == "siliconflow":
                if (resolution != None):
                    resolution = resolution.replace("*", "x")
                payload = {
                    "model": image_llm_model,
                    "prompt": safe_prompt,
                    "seed": random.randint(1000000, 4999999999),
                    "image_size": resolution,
                    "guidance_scale": 7.5,
                    "batch_size": 1,
                }
                headers = {
                    "Authorization": "Bearer " + siliconflow_api_key,
                    "Content-Type": "application/json"
                }
                # 使用配置中的 URL 或默认值
                response = requests.request("POST", "https://api.siliconflow.cn/v1/images/generations", json=payload, headers=headers)
                
                if response.text != None:
                    response = json.loads(response.text)
                    return response["images"][0]["url"]
                else:
                    raise Exception(response.text)
        except Exception as e:
            logger.error(f"Failed to generate image: {e}")
            return ""

    async def generate_story_with_images(self, request: StoryGenerationRequest) -> List[Dict[str, Any]]:
        """生成故事和配图
        Args:
            story_prompt (str, optional): 故事提示. Defaults to None.
            language (Language, optional): 语言. Defaults to Language.CHINESE.
            segments (int, optional): 故事分段数. Defaults to 3.

        Returns:
            List[Dict[str, Any]]: 故事场景列表，每个场景包含文本、图片提示词和图片URL
        """
        # 先生成故事
        story_segments = await self.generate_story(
            request,
        )

        # 为每个场景生成图片
        for segment in story_segments:
            try:
                image_url = self.generate_image(prompt=segment["image_prompt"], resolution=request.resolution, image_llm_provider=request.image_llm_provider, image_llm_model=request.image_llm_model)
                segment["url"] = image_url
            except Exception as e:
                logger.error(f"Failed to generate image for segment: {e}")
                segment["url"] = None

        return story_segments
    
    def get_llm_providers(self) -> Dict[str, List[str]]:
        imgLLMList = []
        textLLMList = []
        if openai_api_key:
            textLLMList.append("openai")
            imgLLMList.append("openai")
        if aliyun_api_key:
            textLLMList.append("aliyun")
            imgLLMList.append("aliyun")
        if deepseek_api_key:
            textLLMList.append("deepseek")
        if ollama_api_key:
            textLLMList.append("ollama")
        if siliconflow_api_key:
            textLLMList.append("siliconflow")
            imgLLMList.append("siliconflow")
        if intern_api_key:
            textLLMList.append("intern")
        return { "textLLMProviders": textLLMList, "imageLLMProviders": imgLLMList }

    def _validate_story_response(self, response: any) -> None:
        """验证故事生成响应

        Args:
            response: LLM 响应

        Raises:
            LLMResponseValidationError: 响应格式错误
        """
        if not isinstance(response, list):
            raise LLMResponseValidationError("Response must be an array")

        for i, scene in enumerate(response):
            if not isinstance(scene, dict):
                raise LLMResponseValidationError(f"story item {i} must be an object")
            
            if "text" not in scene:
                raise LLMResponseValidationError(f"Scene {i} missing 'text' field")
            
            if "image_prompt" not in scene:
                raise LLMResponseValidationError(f"Scene {i} missing 'image_prompt' field")
            
            if not isinstance(scene["text"], str):
                raise LLMResponseValidationError(f"Scene {i} 'text' must be a string")
            
            if not isinstance(scene["image_prompt"], str):
                raise LLMResponseValidationError(f"Scene {i} 'image_prompt' must be a string")

    async def _generate_response(self, *, text_llm_provider: str = None, text_llm_model: str = None, messages: List[Dict[str, str]], response_format: str = "json_object") -> any:
        """生成 LLM 响应

        Args:
            messages: 消息列表
            response_format: 响应格式，默认为 json_object

        Returns:
            Dict[str, Any]: 解析后的响应

        Raises:
            Exception: 请求失败或解析失败时抛出异常
        """
        if text_llm_provider == None:
            text_llm_provider = text_llm_provider
        if text_llm_provider == "aliyun":
            text_client = self.aliyun_text_client
        elif text_llm_provider == "openai":
            text_client = self.openai_client
        elif text_llm_provider == "deepseek":
            text_client = deepseek_client
        elif text_llm_provider == "ollama":
            text_client = ollama_client
        elif text_llm_provider == "siliconflow":
            text_client = siliconflow_client
        elif text_llm_provider == "intern":
            text_client = intern_client
        if text_llm_model == None:
            text_llm_model = text_llm_model
            
        # 根据不同的提供商设置参数
        completion_params = {
            "model": text_llm_model,
            "messages": messages,
        }
        
        # 只为支持的提供商添加 response_format
        if text_llm_provider in ["openai"]:
            completion_params["response_format"] = {"type": response_format}
            
        response = text_client.chat.completions.create(**completion_params)
        try:
            content = response.choices[0].message.content
            result = json.loads(content)
            return result
        except Exception as e:
            logger.error(f"Failed to parse response: {e}")
            raise e

    async def _get_story_prompt(self, story_prompt: str = None, language: Language = Language.CHINESE_CN, segments: int = 3) -> str:
        """生成故事提示词

        Args:
            story_prompt (str, optional): 故事提示. Defaults to None.
            segments (int, optional): 故事分段数. Defaults to 3.

        Returns:
            str: 完整的提示词
        """

        languageValue = LANGUAGE_NAMES[language]
        if story_prompt:
            base_prompt = f"讲一个故事，主题是：{story_prompt}"
        
        return f"""
        {base_prompt}. The story needs to be divided into {segments} scenes, and each scene must include descriptive text and an image prompt.

        Please return the result in the following JSON format, where the key `list` contains an array of objects:

        **Expected JSON format**:
        {{
            "list": [
                {{
                    "text": "Descriptive text for the scene",
                    "image_prompt": "Detailed image generation prompt, described in English"
                }},
                {{
                    "text": "Another scene description text",
                    "image_prompt": "Another detailed image generation prompt in English"
                }}
            ]
        }}

        **Requirements**:
        1. The root object must contain a key named `list`, and its value must be an array of scene objects.
        2. Each object in the `list` array must include:
            - `text`: A descriptive text for the scene, written in {languageValue}.
            - `image_prompt`: A detailed prompt for generating an image, written in English.
        3. Ensure the JSON format matches the above example exactly. Avoid extra fields or incorrect key names like `cimage_prompt` or `inage_prompt`.

        **Important**:
        - If there is only one scene, the array under `list` should contain a single object.
        - The output must be a valid JSON object. Do not include explanations, comments, or additional content outside the JSON.

        Example output:
        {{
            "list": [
                {{
                    "text": "Scene description text",
                    "image_prompt": "Detailed image generation prompt in English"
                }}
            ]
        }}
        """

    

# 创建服务实例
llm_service = LLMService()
