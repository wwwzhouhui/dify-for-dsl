# 1.代码

   目前把gitee平台上实现的功能整合到一个叫做giteeapiforall.py 代码中 本次 多模态图像编辑HiDream-E1接口代码

 

```python
@app.post("/generate-HiDream-E1/")
async def generate_hidream_e1(request: HiDreamE1Request):
    client = OpenAI(
            base_url="https://ai.gitee.com/v1",
            api_key=api_key, # 使用从配置文件读取的api_key
            timeout=300.0,  # <-- 修改: 设置请求超时时间为300秒
            max_retries=0  # <-- 新增: 禁用重试
            # http_client=http_client_with_proxy # <-- 新增: 如果使用代理，取消注释此行
     )
    logger.info(f"Received request with prompt: {request.prompt}, imageurl: {request.imageurl}, has_image_base64: {request.image_base64 is not None}")

    base64_encoded_content_to_process: Optional[str] = None

    if request.imageurl:
        logger.info(f"Attempting to process image from URL: {request.imageurl}")
        try:
            async with httpx.AsyncClient(timeout=30.0) as http_client: # 使用 httpx 进行异步 GET 请求
                response = await http_client.get(request.imageurl)
                response.raise_for_status() # 如果状态码是 4xx 或 5xx，则引发 HTTPStatusError
                image_bytes_from_url = response.content
                base64_encoded_content_to_process = base64.b64encode(image_bytes_from_url).decode('utf-8')
                logger.info(f"Successfully downloaded and base64 encoded image from URL: {request.imageurl}")
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error downloading image from {request.imageurl}: {e.response.status_code} - {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail=f"下载图片URL '{request.imageurl}' 时出错: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e: # 处理网络错误、DNS 失败等
            logger.error(f"Request error downloading image from {request.imageurl}: {str(e)}")
            raise HTTPException(status_code=503, detail=f"连接图片URL '{request.imageurl}' 时出错: {str(e)}") # 503 Service Unavailable
        except Exception as e: # 捕获其他意外错误
            logger.error(f"Unexpected error processing image URL {request.imageurl}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"处理图片URL '{request.imageurl}' 时发生意外错误: {str(e)}")
    elif request.image_base64:
        logger.info("Using provided image_base64 from request body.")
        base64_encoded_content_to_process = request.image_base64
    
    if not base64_encoded_content_to_process:
        logger.warning("No image data provided in request (neither imageurl nor image_base64).")
        raise HTTPException(
            status_code=400, 
            detail="未提供图像数据。请提供 'imageurl' 或 'image_base64'。"
        )

    logger.info(f"Proceeding with image processing. Base64 content length (approx): {len(base64_encoded_content_to_process) if base64_encoded_content_to_process else 0}")

    try:
        # 从请求体中获取 prompt (这部分逻辑不变)
        prompt_text = request.prompt
        
        # 将Base64字符串解码为字节
        # 使用 base64_encoded_content_to_process 替代原来的 request.image_base64
        try:
            image_bytes = base64.b64decode(base64_encoded_content_to_process.encode('utf-8'))
        except Exception as e:
            logger.error(f"解码提供的Base64图片数据时出错: {str(e)}") # 增加此处的日志记录
            raise HTTPException(status_code=400, detail=f"无法解码提供的Base64图片数据: {str(e)}")
        logger.info(f"Base64图片数据已成功解码。 Image byte length: {len(image_bytes)}")
        response = client.images.edit(
            model="HiDream-E1-Full",
            image=image_bytes, # 直接传递解码后的图片字节
            prompt=prompt_text, # 使用从请求体中获取的 prompt
            response_format="b64_json",
            extra_body={
                "steps": 28,
                "instruction_following_strength": 5,
                "image_preservation_strength": 3,
                "refinement_strength": 0.3,
                "seed": -1,
            }
        )
        logger.info(f"Received response from Gitee API: {response}")
        if not response.data or not response.data[0].b64_json:
            raise HTTPException(status_code=500, detail="从Gitee API响应中获取base64数据失败。格式不符合预期。")

        result_b64 = response.data[0].b64_json

        filename, output_path_local = base64_to_image(result_b64, output_path)
        logger.info(f"Image saved to {output_path_local}")
        etag = upload_cos('test', filename, output_path)
        logger.info(f"Image uploaded to COS with etag: {etag}")
        if not etag:
            raise HTTPException(status_code=500, detail="上传图片到COS失败。")

        return {
            "filename": filename,
            "output_path": output_path_local, # 保持字段名一致性或明确区分
            "etag": etag
        }
    except APIConnectionError as e: # <-- 新增: 更具体地捕获连接错误
        logger.error(f"Gitee API Connection Error: {e}")
        error_message = (
            f"无法连接到 Gitee API (请求URL: {e.request.url if hasattr(e, 'request') and e.request else 'N/A'}): {str(e)}. "
            "这通常是由于服务器的网络配置问题（例如防火墙、DNS解析、代理服务器设置）或目标服务暂时不可达。 "
            "请检查服务器的网络连通性，并确认是否需要为应用程序配置代理服务器。"
        )
        raise HTTPException(status_code=503, detail=f"Gitee API 连接错误: {error_message}") # 503 Service Unavailable
    except APIError as e:
        logger.error(f"Gitee API Error: {e}")
        error_detail = str(e)
        if hasattr(e, 'message') and e.message:
            error_detail = e.message
        elif hasattr(e, 'response') and e.response is not None:
            try:
                # 尝试解析JSON响应体中的错误信息
                error_content = e.response.json()
                error_detail = error_content.get("error", {}).get("message", str(e.response.content))
            except json.JSONDecodeError: # 如果响应不是有效的JSON
                error_detail = e.response.text # 使用原始文本响应
            except Exception: # 其他解析错误
                 error_detail = str(e.response.content) # Fallback to raw content as string
        # Gitee API 可能会在 status_code 为 4xx/5xx 时返回非 JSON 错误，例如纯文本或 HTML
        # 因此，直接使用 e.response.text 可能更稳妥，如果 JSON 解析失败
        status_code_to_return = e.status_code if hasattr(e, 'status_code') and e.status_code else 500
        raise HTTPException(status_code=status_code_to_return, detail=f"Gitee API 错误: {error_detail}")
    except HTTPException as e:
        logger.error(f"HTTPException: {e}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        # 对于其他未预料到的错误，记录日志并返回通用错误信息
        # import traceback; traceback.print_exc(); # 可选：在服务器端打印详细堆栈信息
        raise HTTPException(status_code=500, detail=f"发生意外错误: {type(e).__name__} - {str(e)}")
```

# 2.客户端测试代码

   我们使用test_hidream_e1_client2.py 作为客户端测试代码。

   具体使用，先把服务端启动起来

```shell
python giteeapiforall.py
```

 ![QQ20250510-234634](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/QQ20250510-234634.png)

客户端代码test_hidream_e1_client2.py

 

```python
import requests
import os
import base64
import io
import json # 确保导入 json 模块

# FastAPI 服务器地址
server_url = "http://127.0.0.1:8081"
#server_url = "http://14.103.204.132:8080"
# 测试的 API 接口路径
api_path = "/generate-HiDream-E1/"
full_url = f"{server_url}{api_path}"

# --- 用户配置区域 ---
# 请将此变量替换为你的图片的Base64编码字符串
# 例如: image_base64_input = "iVBORw0KGgoAAAANSUhEUgAAAAUA..." (这是一个非常短的示例，实际Base64会很长)
image_base64_input = "/9j/4AAQSkZJRgABAQAAAQABAAD...."  # 示例值，请替换
#image_base64_input =""
# 或者，提供图片的 URL
#image_url_input = "https://dify-1258720957.cos.ap-nanjing.myqcloud.com/20250510142044_8739.png"  # 例如: "http://example.com/your_image.jpg" , 如果提供了 image_url, 将优先使用它
image_url_input =""
# 测试用的提示词
prompt = "请将图片转成吉卜力风格"
# 新增：测试用的 extra_body 参数
# 你可以根据需要修改这些值，或者不发送 extra_body 来测试服务端的默认值
extra_body_payload = {
    "steps": 15,
    "instruction_following_strength": 2.5,
    "image_preservation_strength": 3.5,
    "refinement_strength": 0.4,
    "seed": 98765,
}
# ---

if __name__ == "__main__":
    print(f"正在尝试连接到: {full_url}")

    payload = {
        "prompt": prompt,
        "extra_body": extra_body_payload
    }
    image_source_info = ""

    # 优先使用 image_url_input
    if image_url_input:
        print(f"使用 image_url: {image_url_input}")
        payload["imageurl"] = image_url_input
        image_source_info = f"图片通过 URL 发送: {image_url_input}"
        # 清除可能存在的 image_base64，确保服务端不会混淆
        if "image_base64" in payload:
            del payload["image_base64"]
    # 如果 image_url_input 未提供，则检查 image_base64_input
    elif image_base64_input :
        print("使用 image_base64")
        payload["image_base64"] = image_base64_input
        image_source_info = "图片以Base64编码形式通过JSON负载的 'image_base64' 字段发送。"
        # 清除可能存在的 imageurl
        if "imageurl" in payload:
            del payload["imageurl"]
    else:
        print("错误：未提供图片来源。请在脚本中设置 `image_url_input` 或 `image_base64_input`。")
        print("\n测试脚本执行完毕。")
        exit()

    try:
        # 设置请求头
        headers = {
            "Content-Type": "application/json"
        }

        print(f"发送JSON请求到 {full_url}...")
        print(f"提示词: {prompt}")
        print(f"自定义 Extra Body: {json.dumps(extra_body_payload, indent=4, ensure_ascii=False)}")
        print(image_source_info)

        # 发送 POST 请求，使用 json 参数传递数据，并设置 headers
        response = requests.post(full_url, json=payload, headers=headers, timeout=300) # 设置较长的超时时间

        # 检查响应状态码
        if response.status_code == 200:
            print("请求成功！")
            try:
                响应内容 = response.json()
                print("服务器响应:")
                # import json # json 模块已在文件顶部导入
                print(json.dumps(响应内容, indent=4, ensure_ascii=False))
            except requests.exceptions.JSONDecodeError:
                print("错误：无法解析服务器响应为JSON格式。")
                print(f"原始响应内容: {response.text}")
        else:
            print(f"请求失败，状态码: {response.status_code}")
            try:
                错误详情 = response.json() # 尝试解析错误详情
                print("错误详情:")
                # import json # json 模块已在文件顶部导入
                print(json.dumps(错误详情, indent=4, ensure_ascii=False))
            except requests.exceptions.JSONDecodeError:
                print(f"服务器返回的原始错误信息: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"请求过程中发生错误: {e}")
        print("请确保 FastAPI 服务正在运行，并且网络连接正常。")
    except Exception as e:
        print(f"发生未知错误: {e}")

    print("\n测试脚本执行完毕。")
```

  启动

```shell
python test_hidream_e1_client2.py
```

启动后就等待请求

![QQ20250510-234905](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/QQ20250510-234905.png)

# 3 curl 命令

```shell
curl --location --request POST 'http://14.103.204.132:8080/difyforgitee/generate-HiDream-E1/' \
--header 'Content-Type: application/json' \
--data-raw '{"prompt": " 请将图片转成吉卜力风格", "imageurl": "http://example.com/your_image.jpg"}'
```

```shell
curl --location --request POST 'http://14.103.204.132:8080/difyforgitee/generate-HiDream-E1/' \
--header 'Content-Type: application/json' \
--data-raw '{"prompt": " 请将图片转成吉卜力风格", "image_base64": "/9j/4AAQSkZJRgAB...}'
```

# 4.openapi 3.1.0 版本的json schema 提示词转换脚本

  HiDream E1图像生成_forbase64

```json
请把curl请求命令转成openapi 3.1.0 版本的json schema，不需要包含response信息
<curl>
curl --location --request POST 'http://14.103.204.132:8080/difyforgitee/generate-HiDream-E1/' \
--header 'Content-Type: application/json' \
--data-raw '{"prompt": " 请将图片转成吉卜力风格", "image_base64": "/9j/4AAQSkZJRgAB...}'
</curl>
json schema请参照下面的例子
<json-schema>
{
      "openapi": "3.1.0",
      "info": {
        "title": "Get weather data",
        "description": "Retrieves current weather data for a location.",
        "version": "v1.0.0"
      },
      "servers": [
        {
          "url": ""
        }
      ],
      "paths": {},
      "components": {
        "schemas": {}
      }
    }
</json-schema>
```

  HiDream E1图像生成_forbase64

```json
请把curl请求命令转成openapi 3.1.0 版本的json schema，不需要包含response信息
<curl>
curl --location --request POST 'http://14.103.204.132:8080/difyforgitee/generate-HiDream-E1/' \
--header 'Content-Type: application/json' \
--data-raw '{"prompt": " 请将图片转成吉卜力风格", "imageurl": "http://example.com/your_image.jpg"}'
</curl>

json schema请参照下面的例子
<json-schema>
{
      "openapi": "3.1.0",
      "info": {
        "title": "Get weather data",
        "description": "Retrieves current weather data for a location.",
        "version": "v1.0.0"
      },
      "servers": [
        {
          "url": ""
        }
      ],
      "paths": {},
      "components": {
        "schemas": {}
      }
    }
</json-schema>
```

