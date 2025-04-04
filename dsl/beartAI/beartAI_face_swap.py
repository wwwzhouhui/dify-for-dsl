import os
import json
import time
import random
import requests
import configparser
from fastapi import FastAPI, UploadFile, File, HTTPException,Depends,Header
from fastapi.responses import JSONResponse
import uvicorn
import datetime
import random
from typing import Optional
import logging
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 读取配置文件
config = configparser.ConfigParser()
# windows (windows下的路径)
config.read('e:\\work\\code\\2024pythontest\\beartAi\\config.ini', encoding='utf-8')
# linux (linux下的路径)
#config.read('config.ini', encoding='utf-8')

# 添加 COS 配置读取
region = config.get('common', 'region')
secret_id = config.get('common', 'secret_id')
secret_key = config.get('common', 'secret_key')
bucket = config.get('common', 'bucket')

app = FastAPI(
    title="BeArt AI Face Swap API",
    description="AI换脸服务API",
    version="0.1"
)

class FaceSwapService:
    # 默认请求头
    API_HEADERS = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9",
        "origin": "https://beart.ai",
        "priority": "u=1, i",
        "product-code": "067003",
        "referer": "https://beart.ai/",
        "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    }

    # 从配置文件获取产品序列号
    PRODUCT_SERIAL = config.get('beart', 'product_serial')

    @staticmethod
    def _validate_image(image_data: bytes) -> bool:
        """验证图片格式"""
        try:
            header = image_data[:12]
            if any([
                header.startswith(b'\xFF\xD8\xFF'),  # JPEG
                header.startswith(b'\x89PNG\r\n\x1a\n'),  # PNG
                header.startswith(b'GIF87a') or header.startswith(b'GIF89a'),  # GIF
                header.startswith(b'RIFF') and header[8:12] == b'WEBP',  # WEBP
                header.startswith(b'BM')  # BMP
            ]):
                return True
            return False
        except:
            return False

    @staticmethod
    def _get_mime_type(image_data: bytes) -> str:
        """获取图片MIME类型"""
        header = image_data[:12]
        if header.startswith(b'\xFF\xD8\xFF'):
            return 'image/jpeg'
        elif header.startswith(b'\x89PNG\r\n\x1a\n'):
            return 'image/png'
        elif header.startswith(b'GIF87a') or header.startswith(b'GIF89a'):
            return 'image/gif'
        elif header.startswith(b'RIFF') and header[8:12] == b'WEBP':
            return 'image/webp'
        elif header.startswith(b'BM'):
            return 'image/bmp'
        return 'image/jpeg'

    @classmethod
    async def create_face_swap_job(cls, source_image: bytes, target_image: bytes) -> Optional[str]:
        """创建换脸任务"""
        try:
            url = "https://api.beart.ai/api/beart/face-swap/create-job"
            headers = cls.API_HEADERS.copy()
            headers.update({
                "product-serial": cls.PRODUCT_SERIAL
            })

            # 获取MIME类型
            source_mime = cls._get_mime_type(source_image)
            target_mime = cls._get_mime_type(target_image)

            # 生成随机文件名
            source_name = f"n_v{random.getrandbits(64):016x}.jpg"
            target_name = f"n_v{random.getrandbits(64):016x}.jpg"

            # 构建multipart/form-data请求
            files = {
                "target_image": (target_name, source_image, target_mime),
                "swap_image": (source_name, target_image, source_mime)
            }

            logger.info("开始上传图片...")
            response = requests.post(url, headers=headers, files=files, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("code") == 100000:
                    job_id = data["result"]["job_id"]
                    logger.info(f"任务创建成功: {job_id}")
                    return job_id
                else:
                    logger.error(f"服务器返回错误: {data.get('message', {}).get('zh', '未知错误')}")
            else:
                logger.error(f"创建任务失败: HTTP {response.status_code}")
            return None
            
        except Exception as e:
            logger.error(f"创建任务失败: {e}")
            return None

    @classmethod
    async def get_face_swap_result(cls, job_id: str, max_retries: int = 30, interval: int = 2) -> Optional[str]:
        """获取换脸结果"""
        try:
            url = f"https://api.beart.ai/api/beart/face-swap/get-job/{job_id}"
            headers = cls.API_HEADERS.copy()
            headers["content-type"] = "application/json; charset=UTF-8"
            
            logger.info(f"等待处理结果，最多等待 {max_retries*interval} 秒...")
            for attempt in range(1, max_retries+1):
                try:
                    response = requests.get(url, headers=headers, timeout=15)
                    if response.status_code == 200:
                        data = response.json()
                        if data.get("code") == 100000:
                            logger.info("处理完成")
                            return data["result"]["output"][0]
                        elif data.get("code") == 300001:  # 处理中
                            logger.info(f"处理中... {attempt}/{max_retries}")
                            time.sleep(interval)
                            continue
                    
                    logger.error(f"获取结果失败: {response.text}")
                    return None
                    
                except Exception as e:
                    logger.error(f"获取结果出错: {e}")
                    time.sleep(interval)
            
            logger.error("超过最大重试次数")
            return None
            
        except Exception as e:
            logger.error(f"获取结果失败: {e}")
            return None

# 添加新的辅助函数
def verify_auth_token(authorization: str = Header(None)):
    """验证 Authorization Header 中的 Bearer Token"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization Header")
    
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid Authorization Scheme")
    
    # 从配置文件读取有效token列表
    valid_tokens = json.loads(config.get('auth', 'valid_tokens'))
    if token not in valid_tokens:
        raise HTTPException(status_code=403, detail="Invalid or Expired Token")
    
    return token

def generate_timestamp_filename_for_image(extension='jpg'):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    random_number = random.randint(1000, 9999)
    filename = f"faceswap_{timestamp}_{random_number}.{extension}"
    return filename

def download_image(url, output_path):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    filename = generate_timestamp_filename_for_image()
    file_path = os.path.join(output_path, filename)
    
    with open(file_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)
    
    return filename, file_path

def upload_to_cos(region, secret_id, secret_key, bucket, file_name, base_path):
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
    return None

# 修改face_swap接口，添加鉴权
@app.post("/beartAI/face-swap")
async def face_swap(
    source_image: UploadFile = File(...),
    target_image: UploadFile = File(...),
    auth_token: str = Depends(verify_auth_token)
):
    """
    换脸API接口
    - source_image: 源图片（包含要提取的人脸）
    - target_image: 目标图片（需要被替换人脸的图片）
    """
    try:
        # 读取上传的图片数据
        source_data = await source_image.read()
        target_data = await target_image.read()
        
        # 验证图片格式
        if not FaceSwapService._validate_image(source_data) or not FaceSwapService._validate_image(target_data):
            raise HTTPException(
                status_code=400,
                detail="不支持的图片格式，请使用jpg/png/gif/webp/bmp格式"
            )
        
        # 创建换脸任务
        job_id = await FaceSwapService.create_face_swap_job(source_data, target_data)
        if not job_id:
            raise HTTPException(status_code=500, detail="创建任务失败")
        
        # 获取处理结果
        result_url = await FaceSwapService.get_face_swap_result(job_id)
        if not result_url:
            raise HTTPException(status_code=500, detail="处理失败")
        
        # 下载图片并上传到COS
        try:
            # 确保输出目录存在
            output_path = config.get('common', 'image_output_path')
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            
            # 下载图片
            filename, file_path = download_image(result_url, output_path)
            logger.info(f"图片已下载到本地: {file_path}")
            
            # 上传到腾讯 COS
            cos_url = upload_to_cos(region, secret_id, secret_key, bucket, filename, output_path)
            if cos_url:
                logger.info(f"图片已上传到 COS: {cos_url}")
                # 删除本地文件
                os.remove(file_path)
                return {
                    "success": True,
                    "image_url": cos_url,
                    "original_url": result_url
                }
            else:
                raise HTTPException(status_code=500, detail="上传图片到 COS 失败")
        except Exception as e:
            logger.error(f"处理图片文件失败: {str(e)}")
            raise HTTPException(status_code=500, detail=f"处理图片文件失败: {str(e)}")
            
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"处理失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8089)