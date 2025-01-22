前面给大家介绍过使用dify 调用第三方平台提供的文生图模型、图生图模型API 接口实现AI绘画功能，前面我们也整合硅基流动提供的flux绘画，gitee AI 提供的Kolors模型，那么之前的方案中通过接口调用只能生成单一的图片生成功能，而且每个API 厂商接口可能不一样

需要编写接口的代码调用，对普通小白来说还是有一点难度的。后来我们在dify 中找到了comfui工具，目前来说它是可以实现comfui和dify的整合的。

 ![image-20250122103239448](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250122103239448.png)

仔细研究发现这个comfui 自定义工具是需要第三方comfui提供接口服务的，我们知道搭建comfui也是GPU算力的，搭建起来也是有一点的难度。有没有办法实现免费使用comfui 呢,当然答案是有的。我提出一套解决方案使用硅基流动提供的bizyair+dify整合从而实现dify+免费版本comfui_bizyair解决方案。 话不多说，下面给大家介绍这套解决方案。

# 1.下载部署comfui_bizyair

   关于部署comfui_bizyair 可以看我之前的文章《**[免费使用容器版bizyair](https://aqma351r01f.feishu.cn/wiki/NMnnwojxziCTIlkCg9bcioANnef)**》这里详细介绍了windows 上部署bizyair.

comfui_bizyair 最新版本0.4.0我已经上传到docker hub 镜像托管仓库了，大家可以使用任何支持docker 操作系统（windows、linux、MAC）部署安装comfui_bizyair 。

![image-20250122104605448](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250122104605448.png)

​    下载comfui_bizyair镜像，输入如下命令下载镜像

```
docker pull wwwzhouhui569/comfyui_bizyair:v0.4.0
```

​    ![image-20250122104705973](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250122104705973.png)

因为我已经下载好了，所以直接出现下载完成界面，下载完成后，我们可以在Docker Desktop查看下载好的镜像

![image-20250119104238074](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250119104238074.png)

  接下来我们启动这个镜像，输入如下命令

  

```
  docker run -d -p 8188:8188 -v "D:/tmp/20250118/models:/app/models" -v "D:/tmp/20250118/input:/app/input" -v "D:/tmp/20250118/temp:/app/output/temp" -v "D:/tmp/20250118/output:/app/output" -v "D:/tmp/20250118/user:/app/user"  --name comfyui-container2 wwwzhouhui569/comfyui_bizyair:v0.4.0
```

   其中D:/tmp/20250118 是我们需要挂卷的文件，指的是docker宿主机挂着文件，我们这里在D盘新建文件夹，主要是方便生成图片输出

  ![image-20250119104541737](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250119104541737.png)

![image-20250119104551701](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250119104551701.png)

运行上面命令完成镜像启动

![image-20250119104650209](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250119104650209.png)

可以查看到启动日志 

![image-20250119104733031](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250119104733031.png)

​       容器内部日志显示http://0.0.0.0:8188 说明启动完成。 我们可以点击容器链接地址访问

![image-20250119104830011](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250119104830011.png)

![image-20250119105309089](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250119105309089.png)

 这个时候我们就看到bizyair界面了。第一次进入，需要 bizyair_api_key. 这个从哪获取呢。可以从硅基流动的中获取。

![image-20250119105713498](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250119105713498.png)

如果大家没有硅基流动的账号，可以点击https://cloud.siliconflow.cn/i/e0f6GCrN        地址来注册，目前硅基的政策是新户注册送14块钱。

14块钱可以用其他更高级的模型，目前bizyair目前用到的文生图，图生图模型是免费的，主要开通账号即可。

![image-20250119105922266](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250119105922266.png)

  输入api key 完成注册登录。

![image-20250119110002038](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250119110002038.png)

 下面我们就可以在本地电脑上体验 AI 绘画了。

 ![image-20250119110125358](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250119110125358.png)

# 2.编写comfui_bizyair api 接口

 以上步骤操作完成后，我们就已经使用使用本地电脑（没有显卡也可以）愉快的跑comfui了。如果我们需要对外提供API接口，这里需要

comfui_bizyair 设置下对外的访问接口。这个服务部署最好放到局域网，不要开发端口映射到公网，否自非常不安全。

## 2.1设置comfui_bizyair 

   打开http://192.168.1.13:8188  (我本地电脑IP),点击左下角设置-弹出对话框,开发模型打开 启用开发模型选项，如下图。

![image-20250122105551908](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250122105551908.png)

  以上设置完成后，我们后面就可以编写接口代码调用comfui api 了

##  2.2 comfui_bizyair 接口代码

 我们使用python fastapi 将要comfui 封装一下对外提供api 接口服务，这个接口服务的目的是和dify 进行整合，对外提供出图URL地址信息，图片存储我这里使用腾讯云的OSS 存储。

```python
import json
import websocket  # NOTE: websocket-client (https://github.com/websocket-client/websocket-client)
import uuid
import urllib.request
import urllib.parse
import random
from datetime import datetime
from fastapi import FastAPI, File, UploadFile,HTTPException,Form
from pydantic import BaseModel
import configparser
import logging
import os
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

# 读取配置文件
config = configparser.ConfigParser()
# 读取配置文件，指定编码为 utf-8
config.read('config.ini', encoding='utf-8')

# 获取配置项
output_path = config.get('DEFAULT', 'output_path')
workflowfile = config.get('DEFAULT', 'workflowfile')
comfyui_endpoit = config.get('DEFAULT', 'comfyui_endpoit')
region = config.get('DEFAULT', 'region')
secret_id = config.get('DEFAULT', 'secret_id')
secret_key = config.get('DEFAULT', 'secret_key')
bucket = config.get('DEFAULT', 'bucket')
OSSPICURL=""
# 初始化 FastAPI 应用
app = FastAPI()

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 定义一个函数来显示GIF图片
def show_gif(fname):
    import base64
    from IPython import display
    with open(fname, 'rb') as fd:
        b64 = base64.b64encode(fd.read()).decode('ascii')
    return display.HTML(f'<img src="data:image/gif;base64,{b64}" />')

# 定义一个函数向服务器队列发送提示信息
def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request(f"http://{server_address}/prompt", data=data)
    return json.loads(urllib.request.urlopen(req).read())

# 定义一个函数来获取图片
def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen(f"http://{server_address}/view?{url_values}") as response:
        return response.read()

# 定义一个函数来获取历史记录
def get_history(prompt_id):
    with urllib.request.urlopen(f"http://{server_address}/history/{prompt_id}") as response:
        return json.loads(response.read())

# 定义一个函数来获取图片，这涉及到监听WebSocket消息
def get_images(ws, prompt):
    prompt_id = queue_prompt(prompt)['prompt_id']
    logger.info(f"Prompt ID: {prompt_id}")
    output_images = {}
    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    logger.info("Execution completed")
                    break  # 执行完成
        else:
            continue  # 预览为二进制数据

    history = get_history(prompt_id)[prompt_id]
    logger.info(f"History: {history}")
    for node_id in history['outputs']:
        node_output = history['outputs'][node_id]
        # 图片分支
        if 'images' in node_output:
            images_output = []
            for image in node_output['images']:
                image_data = get_image(image['filename'], image['subfolder'], image['type'])
                images_output.append(image_data)
            output_images[node_id] = images_output
        # 视频分支
        if 'videos' in node_output:
            videos_output = []
            for video in node_output['videos']:
                video_data = get_image(video['filename'], video['subfolder'], video['type'])
                videos_output.append(video_data)
            output_images[node_id] = videos_output

    logger.info("Images retrieved successfully")
    return output_images

# 解析工作流并获取图片
def parse_worflow(ws, prompt, seed, workflowfile):
    logger.info(f"Workflow file: {workflowfile}")
    # with open(workflowfile, 'r', encoding="utf-8") as workflow_api_txt2gif_file:
    #     prompt_data = json.load(workflow_api_txt2gif_file)
    # 设置文本提示
    workflowfile["80"]["inputs"]["text"] = prompt
    return get_images(ws, workflowfile)


def upload_cos(env, file_name, base_path):
    config = CosConfig(
        Region=region,
        SecretId=secret_id,
        SecretKey=secret_key
    )
    client = CosS3Client(config)
    file_path = os.path.join(base_path, file_name)
    response = client.upload_file(
        Bucket=bucket,
        LocalFilePath=file_path,
        Key=file_name,
        PartSize=10,
        MAXThread=10,
        EnableMD5=False
    )
    if response['ETag']:
        url = f"https://{bucket}.cos.{region}.myqcloud.com/{file_name}"
        return url
    else:
        return None
# 生成图像并显示
def generate_clip(prompt, seed, workflowfile, idx):
    logger.info(f"Seed: {seed}")
    ws = websocket.WebSocket()
    try:
        ws.connect(f"ws://{server_address}/ws?clientId={client_id}")
        logger.info("WebSocket connected successfully")
    except Exception as e:
        logger.error(f"WebSocket connection failed: {e}")
        raise

    images = parse_worflow(ws, prompt, seed, workflowfile)

    for node_id in images:
        for image_data in images[node_id]:
            # 获取当前时间，并格式化为 YYYYMMDDHHMMSS 的格式
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename=f"{idx}_{seed}_{timestamp}.png"
            # 使用格式化的时间戳在文件名中
            GIF_LOCATION = os.path.join(output_path, filename)

            logger.info(f"Saving image to: {GIF_LOCATION}")
            with open(GIF_LOCATION, "wb") as binary_file:
                # 写入二进制文件
                binary_file.write(image_data)

            show_gif(GIF_LOCATION)
            # 上传腾讯oss存储
            etag = upload_cos('test', filename, output_path)
            logger.info(f"{GIF_LOCATION} DONE!!!")
            logger.info(f"{etag} DONE!!!")
    return filename,output_path,etag

# FastAPI 路由
@app.post("/comfyui_bizyairapi/")
#async def generate_clip_endpoint(request: GenerateClipRequest,file: UploadFile = File(...)):
async def generate_clip_endpoint(prompt: str = Form(...), seed: int = Form(...), idx: int = Form(...), workflowfile: UploadFile = File(...)):
    try:
        #logger.info(f"Received request: {request}")
        logger.info(f"Received request: prompt={prompt}, seed={seed}, idx={idx}, workflowfile={workflowfile.filename}")
        #读取上传的文件内容
        workflow_content  = await workflowfile.read()
        # 将文件内容转换为json
        workflow_data = json.loads(workflow_content)
        filename, output_path, etag = generate_clip(
            prompt,
            seed,
            workflow_data,
            idx
        )
        return {
            "filename": filename,
            "output_path": output_path,
            "etag": etag
        }
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# 设置工作目录和项目相关的路径
WORKING_DIR = output_path
SageMaker_ComfyUI = WORKING_DIR
workflowfile = workflowfile
COMFYUI_ENDPOINT = comfyui_endpoit

server_address = COMFYUI_ENDPOINT
client_id = str(uuid.uuid4())  # 生成一个唯一的客户端ID

# 启动 FastAPI 应用程序
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8082)

```

 代码中用到的配置文件

 config.ini

```ini
[DEFAULT]
output_path = D:\\工作临时\\2025\\1月\\2025年1月20日\\output
#output_path = /home/python/difyforgitee/pictures
workflowfile= D:\\工作临时\\2025\\1月\\2025年1月17日\\workflow_api111.json
#workflowfile= /home/python/difyforgitee/workflow_api111.json
comfyui_endpoit=192.168.1.13:8188
region = ap-nanjing              腾讯云OSS存储Region
secret_id = xxxxxx               腾讯云OSS存储SecretId
secret_key = xxxxx               腾讯云OSS存储SecretKey
bucket = dify-1258720957         腾讯云OSS存储bucket
```

 python 运行依赖包 requirements.txt

```ini
uvicorn== 0.34.0
fastapi== 0.115.6
cos-python-sdk-v5==1.9.33
python-multipart
pydantic
ipython==8.31.0
websocket-client==1.8.0
```

编写好代码 可以部署本地或则服务器上。这里我们只需要python 运行环境即可，建议使用python3.10 +环境，程序发布后，对外提供一个8082的接口服务。发布的接口服务为：http://192.168.1.13:8082/comfyui_bizyairapi/

#  3.dify工作流

​    下面就是dify工作流部分，这个工作流相对比较简单，主要分为4个部分。开始，HTTP 请求，代码执行，直接回复

   ![image-20250122110658876](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250122110658876.png)

##   3.1开始

​       这个地方重点就是接受2个参数，一个是用户输入的prompt提示词，一个是comfui工作流json文件

​       ![image-20250122110853584](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250122110853584.png)

prompt 是一个文本变量。

 ![image-20250122110925745](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250122110925745.png)

workflowfile 是一个文件类型文件，这里需要注意我们需要自定义文件格式。

 ![image-20250122111025564](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250122111025564.png)

##  3.2 http请求

​    这个地方定义了http请求调用上面的comfui_bizyair 接口。 请求地址 http://192.168.1.13:8082/comfyui_bizyairapi/，使用post方式

 ![image-20250122111347501](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250122111347501.png)

body部分这里我们需要注意，使用form-data 格式

1.prompt   开始节点用户输入的 提示词参数

2.seed 种子数，这个地方可以写死

3.idx    这里填写1

4.workflowfile   这里是file 文件类型，开始节点中上传的json文件

##  3.3 代码执行

 这代码转换主要目的是处理comfui_bizyair 接口生成图片URL 地址处理，代码如下

```python
def main(arg1: str) -> str:
    import json
    data = json.loads(arg1)
    filename=data['filename']
    url=data['etag']
    markdown_result = f"![{filename}]({url})"
    return {"result": markdown_result}
```

请求参数就是上面http请求输出的结果

![image-20250122111807922](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250122111807922.png)

##  3.4 直接回复

  这个直接输出就比较简单就是代码处理后的信息返回即可。

 ![image-20250122111912506](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250122111912506.png)

以上就完成dify工作流的配置，这个工作流比较简单主要目的就是帮助大家理解和调用comfui_bizyair接口。

#  4.验证及测试

   这个验证测试我们需要分2个部分，第一部分 验证测试一下免费容器版comfui_bizyair

##     4.1 comfui_bizyair测试

​    打开comfui_bizyair，第一次我们需要用硅基流动API登录，上面已经提到，这里就不展开介绍了。点击社区，进入社区列表选择界面

 ![image-20250122112314169](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250122112314169.png)

![image-20250122112351134](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250122112351134.png)

我们在工作流列表中选择一个可图文生图。（这个支持中文），点击右边的load

![image-20250122112447078](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250122112447078.png)

这个时候工作流加载了我们刚才选定的工作流了。 

 ![image-20250122112537390](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250122112537390.png)

 我们点击工作流下方 执行按钮 开始出图了。点击执行几秒钟之后，工作流已经出现了文生图结果了。

![image-20250122112658451](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250122112658451.png)

 我们点左上角 工作流-导出api

![image-20250122112749967](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250122112749967.png)

![image-20250122112819807](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250122112819807.png)

把这个工作流保存我们电脑中。以上步骤完成了免费容器版comfui_bizyair验证性测试。

## 4.2 dify整合comfui_bizyair测试

接下来我们打开上面配置好的工作流。

点击预览，输入用户提示词和上传刚才导出的工作流json格式文件

 ![image-20250122113145019](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250122113145019.png)

点击执行按钮就可以测试了

 ![image-20250122113238927](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250122113238927.png)

这个时候我们看到了dify 通过接口实现了comfui_bizyair的接口调用了。

# 5.注意事项

 因为考虑到comfui生成节点内容不同，尤其是提示词传入参数和替换的部分代码可能是需要根据实际工作流json格式文件修改。比如

 打开导出的workflow_api112.json

```json
{
  "70": {
    "inputs": {
      "unet_name": "kolors/Kolors.safetensors"
    },
    "class_type": "BizyAir_MZ_KolorsUNETLoaderV2",
    "_meta": {
      "title": "☁️BizyAir MinusZone - KolorsUNETLoaderV2"
    }
  },
  "73": {
    "inputs": {
      "seed": 20,
      "steps": 20,
      "cfg": 4.5,
      "sampler_name": "dpmpp_sde_gpu",
      "scheduler": "karras",
      "denoise": 1,
      "model": [
        "70",
        0
      ],
      "positive": [
        "80",
        0
      ],
      "negative": [
        "81",
        0
      ],
      "latent_image": [
        "85",
        0
      ]
    },
    "class_type": "BizyAir_KSampler",
    "_meta": {
      "title": "☁️BizyAir KSampler"
    }
  },
  "75": {
    "inputs": {
      "vae_name": "sdxl/sdxl_vae.safetensors"
    },
    "class_type": "BizyAir_VAELoader",
    "_meta": {
      "title": "☁️BizyAir Load VAE"
    }
  },
  "76": {
    "inputs": {
      "samples": [
        "73",
        0
      ],
      "vae": [
        "75",
        0
      ]
    },
    "class_type": "BizyAir_VAEDecode",
    "_meta": {
      "title": "☁️BizyAir VAE Decode"
    }
  },
  "80": {
    "inputs": {
      "text": "真实的照片,20岁女生,红色外套,城市夜景"
    },
    "class_type": "BizyAir_MinusZoneChatGLM3TextEncode",
    "_meta": {
      "title": "☁️BizyAir MinusZone ChatGLM3 Text Encode"
    }
  },
  "81": {
    "inputs": {
      "text": "nsfw，脸部阴影，低分辨率，jpeg伪影、模糊、糟糕，黑脸，霓虹灯"
    },
    "class_type": "BizyAir_MinusZoneChatGLM3TextEncode",
    "_meta": {
      "title": "☁️BizyAir MinusZone ChatGLM3 Text Encode"
    }
  },
  "85": {
    "inputs": {
      "width": 1024,
      "height": 1024,
      "batch_size": 1
    },
    "class_type": "EmptyLatentImage",
    "_meta": {
      "title": "空Latent图像"
    }
  },
  "86": {
    "inputs": {
      "images": [
        "76",
        0
      ]
    },
    "class_type": "PreviewImage",
    "_meta": {
      "title": "预览图像"
    }
  }
}
```

这个工作流json 文件中 66- 68行内容是

```
  "80": {
    "inputs": {
      "text": "真实的照片,20岁女生,红色外套,城市夜景"
    },
```

对应接口代码这块

![image-20250122113643899](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250122113643899.png)

  这个提示词替换部分需要注意提示词替换的部分节点需要和工作流导出的节点内容保持一致。

# 6.总结

   本次我们给大家介绍了免费版comfui_bizyair容器部署以及介绍了这个comfui_bizyair的使用，另外介绍了comfui_bizyair接口的编写，以及如何搭建dify工作流和comfui_bizyair整合，从而实现免费体验comfui AI绘画。今天的分享就到这里结束了，小伙伴可以留言和关注我们下个文章见。