import os
import sys
from pathlib import Path

# 将项目根目录添加到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, HTTPException, APIRouter, UploadFile, File, Depends
from fastapi.routing import APIRoute, Mount

from geekaiapp.g_utils import upload_cos, tencent_region, tencent_secret_id, \
    tencent_secret_key, tencent_bucket, ip, \
    current_directory, verify_auth_token, ip_img, face_swapdownload_image, FaceSwapService

app = FastAPI(debug=True)

router = APIRouter()

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# 修改face_swap接口，添加鉴权
@router.post("/beartAI/face-swap")
async def face_swap(source_image: UploadFile = File(...), target_image: UploadFile = File(...),
                    auth_token: str = Depends(verify_auth_token)):
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
                raise HTTPException(status_code=500, detail="上传图片到 COS 失败")
        except Exception as e:
            logger.error(f"处理图片文件失败: {str(e)}")
            raise HTTPException(status_code=500, detail=f"处理图片文件失败: {str(e)}")

    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"处理失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")


app.include_router(router, prefix="/api")

# 打印所有路由
for route in app.routes:
    if isinstance(route, APIRoute):  # 检查是否为路由
        print(f"Path: {route.path}, Methods: {route.methods}")
    elif isinstance(route, Mount):  # 检查是否为挂载点
        print(f"Mount: {route.path} -> {route.name}")

if __name__ == '__main__':
    import uvicorn

    # 修改启动配置 # 禁用热重载以避免初始化问题
    uvicorn.run(app, host="0.0.0.0", port=16001, log_level="info", reload=False)
