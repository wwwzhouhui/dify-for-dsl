dify使用自定义工具可以参考[[Dify中创建并使用自定义工具]]

飞书文章https://aqma351r01f.feishu.cn/wiki/YGQKw5W71iFs0Hkaua8c64Tvn1b

首先我们需要保证对外提供ai 绘画的fastapi接口可以对外提供服务。我这里就华为云为案例将giteeapifordify.py 发布成对外提供的服务，并上传到华为云服务器上。

![image-20241218135608657](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20241218135608657.png)

对外提供的接口服务

http://111.119.215.74:8081/generate_image/

![image-20241218135717008](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20241218135717008.png)

发布好服务后，我们可以通过postman 客户端调用一下这个接口服务

![image-20241218135809837](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20241218135809837.png)

返回200后我们就可以获取到生成图片的URL链接。这里我们把图片上传到腾讯云OSS存储上方便查询和管理。

# 1.创建自定义工具

##   OpenAPI-Swagger规范

 dify提供了创建自定义工具，不过这个自定义工具是需要遵循OpenAPI-Swagger规范。

   规范的空模版的例子如下

```
 {
      "openapi": "3.1.0",
      "info": {
        "title": "Untitled",
        "description": "Your OpenAPI specification",
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
```

## 	生成OpenAPI-Swagger规范

我们使用gpt 帮我把postman 客户端调用curl 命令转换成openapi schema，提示词如下

```
请把curl请求命令转成openapi 3.1.0 版本的json schema，不需要包含response信息
<curl>
curl --location 'http://111.119.215.74:8081/generate_image/'
--header 'Content-Type: application/json'
--data '{"prompt": "一只可爱的小花猫，时尚，头上戴着彩色波点蝴蝶结三角头巾，大大的腮红，很可爱，高饱和度，可爱嘟嘟，毛绒绒且柔软，身穿头巾撞色系旗袍，羊毛毡风格，脖子带你呼应色围巾，非常可爱，怀里抱一束花，上半身肖像，送给你的姿势，卡哇伊，画面简约，高饱和度，轻松气氛，丝滑的画质，中景视角，标准镜头，简约风格，32k高清图，萌态十足，蓝天白云背景，精妙无双"}'
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

![image-20241218141857595](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20241218141857595.png)

生成的结果如下

```
{
  "openapi": "3.1.0",
  "info": {
    "title": "Generate Image API",
    "description": "API to generate an image based on a given prompt.",
    "version": "v1.0.0"
  },
  "servers": [
    {
      "url": "http://111.119.215.74:8081"
    }
  ],
  "paths": {
    "/generate_image/": {
      "post": {
        "summary": "Generate an image based on a prompt",
        "operationId": "generateImage",
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/GenerateImageRequest"
              }
            }
          }
        },
        "responses": {}
      }
    }
  },
  "components": {
    "schemas": {
      "GenerateImageRequest": {
        "type": "object",
        "properties": {
          "prompt": {
            "type": "string",
            "description": "The prompt describing the image to be generated."
          }
        },
        "required": [
          "prompt"
        ]
      }
    }
  }
}

```

## 验证测试自定义第三方接口

接下来我们验证一下，将以上生成好的代码复制到dify 创建自定义工具中

 ![image-20240719143902939](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20240719143902939.png)

![image-20241218142213460](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20241218142213460.png)

测试验证一下接口

![image-20241218142316483](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20241218142316483.png)

![image-20241218142402675](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20241218142402675.png)

   我们通过测试结果返回窗口中查看到3个返回值，这个3个返回值和我们之前posman返回类似，说明我们自定义第三方接口API给dify 提供的接口服务是OK的了。

# 2 .工作流应用

## 1.工作流创建

工作室页面->创建空白应用->选择聊天助手->选择工作流编排->输入名称，工具调用-giteeapiKolors

![image-20241218142723089](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20241218142723089.png)

开始 添加自定义工具

![image-20241218142932351](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20241218142932351.png)

后面的相关流程配置这里就不做详细展开大家可以看一下主要的工作流。

![image-20241218153341190](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20241218153341190.png)

完整的工作流如下：

```yaml
app:
  description: ''
  icon: 🤖
  icon_background: '#FFEAD5'
  mode: advanced-chat
  name: giteeKolors工作流
  use_icon_as_answer_icon: false
kind: app
version: 0.1.3
workflow:
  conversation_variables: []
  environment_variables: []
  features:
    file_upload:
      allowed_file_extensions:
      - .JPG
      - .JPEG
      - .PNG
      - .GIF
      - .WEBP
      - .SVG
      allowed_file_types:
      - image
      allowed_file_upload_methods:
      - local_file
      - remote_url
      enabled: false
      fileUploadConfig:
        audio_file_size_limit: 50
        batch_count_limit: 5
        file_size_limit: 15
        image_file_size_limit: 10
        video_file_size_limit: 100
        workflow_file_upload_limit: 10
      image:
        enabled: false
        number_limits: 3
        transfer_methods:
        - local_file
        - remote_url
      number_limits: 3
    opening_statement: ''
    retriever_resource:
      enabled: true
    sensitive_word_avoidance:
      enabled: false
    speech_to_text:
      enabled: false
    suggested_questions: []
    suggested_questions_after_answer:
      enabled: false
    text_to_speech:
      enabled: false
      language: ''
      voice: ''
  graph:
    edges:
    - data:
        isInIteration: false
        sourceType: start
        targetType: tool
      id: 1734503281575-source-1734503376625-target
      source: '1734503281575'
      sourceHandle: source
      target: '1734503376625'
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInIteration: false
        sourceType: tool
        targetType: code
      id: 1734503376625-source-1734505657943-target
      source: '1734503376625'
      sourceHandle: source
      target: '1734505657943'
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInIteration: false
        sourceType: code
        targetType: answer
      id: 1734505657943-source-1734505427122-target
      source: '1734505657943'
      sourceHandle: source
      target: '1734505427122'
      targetHandle: target
      type: custom
      zIndex: 0
    nodes:
    - data:
        desc: ''
        selected: false
        title: 开始
        type: start
        variables:
        - label: prompt
          max_length: 256
          options: []
          required: true
          type: text-input
          variable: prompt
      height: 89
      id: '1734503281575'
      position:
        x: 92
        y: 292
      positionAbsolute:
        x: 92
        y: 292
      selected: true
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 244
    - data:
        desc: ''
        provider_id: 29303358-86a5-4a38-a3dc-5691788732d4
        provider_name: giteeapiKolors
        provider_type: api
        selected: false
        title: generateImage
        tool_configurations: {}
        tool_label: generateImage
        tool_name: generateImage
        tool_parameters:
          prompt:
            type: mixed
            value: '{{#1734503281575.prompt#}}'
        type: tool
      height: 53
      id: '1734503376625'
      position:
        x: 384
        y: 282
      positionAbsolute:
        x: 384
        y: 282
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 244
    - data:
        answer: '{{#1734505657943.result#}}'
        desc: ''
        selected: false
        title: 直接回复
        type: answer
        variables: []
      height: 102
      id: '1734505427122'
      position:
        x: 1038
        y: 270
      positionAbsolute:
        x: 1038
        y: 270
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 244
    - data:
        code: "def main(arg1: str) -> str:\n    import json\n    data = json.loads(arg1)\n\
          \    filename=data['filename']\n    url=data['etag']\n    markdown_result\
          \ = f\"![{filename}]({url})\"\n    return {\"result\": markdown_result}"
        code_language: python3
        desc: ''
        outputs:
          result:
            children: null
            type: string
        selected: false
        title: 代码执行
        type: code
        variables:
        - value_selector:
          - '1734503376625'
          - text
          variable: arg1
      height: 53
      id: '1734505657943'
      position:
        x: 714
        y: 276
      positionAbsolute:
        x: 714
        y: 276
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 244
    viewport:
      x: 53
      y: 157
      zoom: 1

```

## 工作流测试

![image-20241218153852515](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20241218153852515.png)

# 3 .自定义工具代码

 config.ini

```
[DEFAULT]
api_key = XXXXX                  gitee Serverless API key
output_path = D:\\tmp\\zz        生成图片的服务临时存储的图片路径
region = ap-nanjing              腾讯云OSS存储Region
secret_id = xxxxxx               腾讯云OSS存储SecretId
secret_key = xxxxx               腾讯云OSS存储SecretKey
bucket = dify-1258720957         腾讯云OSS存储bucket
```

## 1.Serverless API 

 api_key  如何获取 登录https://ai.gitee.com/ 平台，点击资源模型包，目前gitee提供以下几个厂商的模型资源包

 包

![image-20241218154532689](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20241218154532689.png)

我这里就选择天数智芯为案例，因为它家的模型Serverless API 模型最多。

我们选择[Kolors](https://ai.gitee.com/serverless-api/packages/1496?model=Kolors&package=1496&operation=70) 这个模型点击体验-点击右边api

 ![image-20241218154801306](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20241218154801306.png)



   勾选右上角以下添加令牌，生成API key，这个就是我们上面配置文件用到的API key

![image-20241218154930308](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20241218154930308.png)

 目前gitee 平台在推广期，每天可以使用以上任意厂商的Serverless API 100次请求，如果您觉得不够用，可以充值购买他们的家的服务。

## 2.腾讯云OSS存储

 gitee 平台提供Serverless API 在文生图模型（stable-diffusion-3.5-large-turbo、Kolors）返回的图片是base64的，在dify 平台上不能直接使用，所以我们借用腾讯OSS存储实现图片上传和存储，方便dify后面的显示。

关于 腾讯云OSS存储 这里就不做详细展开，我这里为了该项目单独建立了bucket

![image-20241218160453773](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20241218160453773.png)

## 3 核心代码

 该代码主要功能是调用Serverless API 返回文生图base64，然后我们在通过腾讯云OSS存储实现base64转换成图片然后上传到腾讯云OSS存储上。

![image-20241218160747488](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20241218160747488.png)

giteeapifordify.py

```python
import requests
import json
import base64
from PIL import Image
import io
import os
import sys
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import datetime
import random
import configparser
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

# 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')

# 从配置文件中读取参数
api_key = config.get('DEFAULT', 'api_key')
output_path = config.get('DEFAULT', 'output_path')
region = config.get('DEFAULT', 'region')
secret_id = config.get('DEFAULT', 'secret_id')
secret_key = config.get('DEFAULT', 'secret_key')
bucket = config.get('DEFAULT', 'bucket')

app = FastAPI()

class GenerateImageRequest(BaseModel):
    prompt: str
def generate_timestamp_filename(extension='png'):
    # 获取当前时间的时间戳
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    # 生成一个随机数
    random_number = random.randint(1000, 9999)
    # 组合生成文件名
    filename = f"{timestamp}_{random_number}.{extension}"
    return filename

def base64_to_image(base64_string, output_dir):
    # 生成文件名
    filename = generate_timestamp_filename()
    # 组合完整的输出路径
    output_path = os.path.join(output_dir, filename)

    # 解码Base64字符串
    image_data = base64.b64decode(base64_string)

    # 将解码后的数据转换为图像
    image = Image.open(io.BytesIO(image_data))

    # 保存图像到指定路径
    image.save(output_path)

    print(f"图片已保存到 {output_path}")
    # 返回文件名和输出路径
    return filename, output_path

def upload_cos(env, file_name, base_path):
    # 读取配置文件
    config = CosConfig(
        Region=region,  # 替换为你的Region
        SecretId=secret_id,  # 替换为你的SecretId
        SecretKey=secret_key  # 替换为你的SecretKey
    )
    client = CosS3Client(config)

    # 构造上传文件的完整路径
    file_path = os.path.join(base_path, file_name)

    # 上传文件
    response = client.upload_file(
        Bucket=bucket,  # 替换为你的Bucket名称
        LocalFilePath=file_path,
        Key=file_name,
        PartSize=10,
        MAXThread=10,
        EnableMD5=False
    )

    if response['ETag']:
        print(f"文件 {file_name} 上传成功")
        # 构造并返回图片的URL
        url = f"https://{bucket}.cos.{region}.myqcloud.com/{file_name}"
        return url
    else:
        print(f"文件 {file_name} 上传失败")
        return None

@app.post("/generate_image/")
async def generate_image(request: GenerateImageRequest):
    url = "https://ai.gitee.com/v1/images/generations"

    payload = {
        "model": "Kolors",
        "prompt": request.prompt,
        "n": 1,
        "response_format": "b64_json"
    }
    # print(prompt)
    # print(api_key)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    result = response.json()["data"][0]["b64_json"]

    # 输出图片路径
    filename, output_path2 = base64_to_image(result, output_path)

    print(f"图片已保存到 {output_path2}")

    env = 'test'  # 或 'prod'
    etag = upload_cos(env, filename, output_path)

    return {
        "filename": filename,
        "output_path": output_path2,
        "etag": etag
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)

```

程序依赖包

requirements.txt

```
uvicorn== 0.34.0
fastapi== 0.115.6
cos-python-sdk-v5==1.9.33
```

完整的代码上传github 大家可以获取

https://github.com/wwwzhouhui/dify-for-dsl/tree/main/dsl/difyforgitee
