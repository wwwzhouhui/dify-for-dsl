import os
import sys
import base64
import io
from pathlib import Path

# 将项目根目录添加到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
from mcp.server.fastmcp import FastMCP
from PIL import Image

from geekaiapp.g_utils import upload_cos, tencent_region, tencent_secret_id, \
    tencent_secret_key, tencent_bucket, ip, \
    current_directory, verify_auth_token, ip_img, face_swapdownload_image, FaceSwapService

# 初始化MCP服务器
mcp = FastMCP("BeartAIServer", port=16001)

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@mcp.tool()
async def face_swap(source_image_base64: str, target_image_base64: str, auth_token: str = None):
    """
    换脸API接口
    - source_image_base64: 源图片的Base64编码（包含要提取的人脸）
    - target_image_base64: 目标图片的Base64编码（需要被替换人脸的图片）
    - auth_token: 可选的认证令牌
    """
    try:
        # 验证认证令牌（如果提供）
        if auth_token:
            try:
                verify_auth_token(auth_token)
            except Exception as e:
                return {"success": False, "error": f"认证失败: {str(e)}"}
        
        # 解码Base64图片数据
        try:
            source_data = base64.b64decode(source_image_base64)
            target_data = base64.b64decode(target_image_base64)
        except Exception as e:
            return {"success": False, "error": f"图片解码失败: {str(e)}"}

        # 验证图片格式
        if not FaceSwapService._validate_image(source_data) or not FaceSwapService._validate_image(target_data):
            return {
                "success": False,
                "error": "不支持的图片格式，请使用jpg/png/gif/webp/bmp格式"
            }

        # 创建换脸任务
        job_id = await FaceSwapService.create_face_swap_job(source_data, target_data)
        if not job_id:
            return {"success": False, "error": "创建任务失败"}

        # 获取处理结果
        result_url = await FaceSwapService.get_face_swap_result(job_id)
        if not result_url:
            return {"success": False, "error": "处理失败"}

        # 下载图片并上传到COS
        try:
            # 确保输出目录存在
            output_path = current_directory / ip_img
            if not os.path.exists(output_path):
                os.makedirs(output_path)

            # 下载图片
            filename, file_path = face_swapdownload_image(result_url, current_directory / ip_img)
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
                return {"success": False, "error": "上传图片到 COS 失败"}
        except Exception as e:
            logger.error(f"处理图片文件失败: {str(e)}")
            return {"success": False, "error": f"处理图片文件失败: {str(e)}"}

    except Exception as e:
        logger.error(f"处理失败: {str(e)}")
        return {"success": False, "error": f"处理失败: {str(e)}"}


# 辅助函数：将图片转换为Base64编码
def image_to_base64(image_path):
    """
    将图片文件转换为Base64编码字符串
    :param image_path: 图片文件路径
    :return: Base64编码字符串
    """
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            return encoded_string
    except Exception as e:
        logger.error(f"图片转Base64失败: {str(e)}")
        return None

# 辅助函数：将PIL图像对象转换为Base64编码
def pil_image_to_base64(pil_image, format="JPEG"):
    """
    将PIL图像对象转换为Base64编码字符串
    :param pil_image: PIL图像对象
    :param format: 图像格式，默认为JPEG
    :return: Base64编码字符串
    """
    try:
        buffer = io.BytesIO()
        pil_image.save(buffer, format=format)
        encoded_string = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return encoded_string
    except Exception as e:
        logger.error(f"PIL图像转Base64失败: {str(e)}")
        return None

# 打印所有工具
for tool_name in mcp.tools:
    print(f"Tool: {tool_name}")

if __name__ == '__main__':
    # 配置MCP服务器
    mcp.settings.host = "0.0.0.0"
    mcp.settings.port = 16001
    
    # 启动MCP服务器，使用SSE传输模式
    mcp.run(transport="sse")
