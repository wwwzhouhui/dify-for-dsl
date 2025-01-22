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

# # 解析工作流并获取图片
# def parse_worflow(ws, prompt, seed, workflowfile):
#     logger.info(f"Workflow file: {workflowfile}")
#     if os.path.isfile(workflowfile):
#         # If it's a file path, open and load the JSON
#         print("文件路径")
#         with open(workflowfile, 'r', encoding="utf-8") as workflow_api_txt2gif_file:
#             prompt_data = json.load(workflow_api_txt2gif_file)
#     else:
#         # If it's a JSON string, parse it directly
#         print("json字符串")
#         try:
#             prompt_data = json.loads(workflowfile)
#         except json.JSONDecodeError as e:
#             logger.error(f"Failed to parse JSON string: {e}")
#             raise
#     prompt_data["80"]["inputs"]["text"] = prompt
#     return get_images(ws, prompt_data)
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

# 定义请求模型
# class GenerateClipRequest(BaseModel):
#     prompt: str
#     seed: int
#     idx: int

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
