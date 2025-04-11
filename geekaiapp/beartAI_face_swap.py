import logging
import os
import random
import time
from typing import Optional

import requests
import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Header
from fastapi_mcp import add_mcp_server

from geekaiapp.g_model import VideoRequest3
from geekaiapp.g_utils import verify_auth_token, product_serial, download_image, ip_img, current_directory, upload_cos, \
    tencent_region, tencent_secret_id, tencent_secret_key, tencent_bucket, ip

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="BeArt AI Face Swap API",
    description="AI换脸服务API",
    version="0.1"
)

# 修改 MCP 服务器配置
mcp_server = add_mcp_server(
    app,
    mount_path="/mcp",
    name="BeArt Image MCP",
    description="集成了照片视频换脸功能的 MCP 服务",
    base_url="http://localhost:15124"
)


# 添加自定义 MCP 工具
@mcp_server.tool()
async def generate_mcp(
        source_image: UploadFile = File(...),
        target_image: UploadFile = File(...),
        authorization: str = Header(...)
) -> dict:
    """
    换脸工具。

    Args:
        source_image: 源图片（包含要提取的人脸）
        target_image: 目标图片（需要被替换人脸的图片）

    Returns:
        dict: 包含以下字段的字典：
            - success: 接口返回成功是否,true是成功，false是失败
            - image_url: 图片的远程地址
            - original_url: 视频预览的 markdown 代码
    """
    request = VideoRequest3(
        source_image=source_image,
        target_image=target_image
    )
    return await face_swap(request, auth_token=verify_auth_token(authorization))


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
    PRODUCT_SERIAL = product_serial

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

            logger.info(f"等待处理结果，最多等待 {max_retries * interval} 秒...")
            for attempt in range(1, max_retries + 1):
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
            # output_path = config.get('common', 'image_output_path')
            output_path = current_directory / ip_img
            if not os.path.exists(output_path):
                os.makedirs(output_path)

            # 下载图片
            filename, file_path = download_image(result_url, current_directory / ip_img)
            logger.info(f"图片已下载到本地: {file_path}")

            # 上传到腾讯 COS
            cos_url = upload_cos('test', tencent_region, tencent_secret_id, tencent_secret_key,
                                 tencent_bucket, filename,
                                 current_directory / ip_img)
            local_url = f"{ip}{ip_img}/{filename}"
            if cos_url:
                logger.info(f"图片已上传到 COS: {cos_url}")
                # 删除本地文件
                # os.remove(file_path)
                return {
                    "success": True,
                    "image_url": cos_url,
                    "original_url": local_url
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
    uvicorn.run(app, host="0.0.0.0", port=15124)
