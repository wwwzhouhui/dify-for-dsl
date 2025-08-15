import os
import sys
import logging
import gradio as gr
import requests
from pathlib import Path

# 将项目根目录添加到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# 确保能找到geekaiapp模块
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from geekaiapp.g_utils import upload_cos, tencent_region, tencent_secret_id, \
    tencent_secret_key, tencent_bucket, ip, \
    current_directory, valid_tokens1, ip_img, face_swapdownload_image, FaceSwapService

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def verify_auth_token(token):
    """验证认证令牌"""
    if not token:
        return False, "缺少认证令牌"
    
    if token not in valid_tokens1:
        return False, "无效或过期的令牌"
    
    return True, token


async def process_face_swap(source_image, target_image, auth_token):
    """处理换脸请求"""
    try:
        # 验证认证令牌
        is_valid, token_or_error = await verify_auth_token(auth_token)
        if not is_valid:
            return None, token_or_error
        
        # 读取上传的图片数据
        if source_image is None or target_image is None:
            return None, "请上传源图片和目标图片"
        
        # 将PIL图像转换为字节数据
        import io
        source_buffer = io.BytesIO()
        target_buffer = io.BytesIO()
        source_image.save(source_buffer, format="PNG")
        target_image.save(target_buffer, format="PNG")
        source_data = source_buffer.getvalue()
        target_data = target_buffer.getvalue()
        
        # 验证图片格式
        if not FaceSwapService._validate_image(source_data) or not FaceSwapService._validate_image(target_data):
            return None, "不支持的图片格式，请使用jpg/png/gif/webp/bmp格式"
        
        # 创建换脸任务
        job_id = await FaceSwapService.create_face_swap_job(source_data, target_data)
        if not job_id:
            return None, "创建任务失败"
        
        # 获取处理结果
        result_url = await FaceSwapService.get_face_swap_result(job_id)
        if not result_url:
            return None, "处理失败"
        
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
                return file_path, "处理成功"
            else:
                return None, "上传图片到 COS 失败"
        except Exception as e:
            logger.error(f"处理图片文件失败: {str(e)}")
            return None, f"处理图片文件失败: {str(e)}"
        
    except Exception as e:
        logger.error(f"处理失败: {str(e)}")
        return None, f"处理失败: {str(e)}"


def create_gradio_interface():
    """创建Gradio界面"""
    with gr.Blocks(title="BeArt AI 换脸系统") as demo:
        gr.Markdown("# BeArt AI 换脸系统")
        gr.Markdown("上传源图片（包含要提取的人脸）和目标图片（需要被替换人脸的图片），系统将自动进行换脸处理。")
        
        with gr.Row():
            with gr.Column():
                source_image = gr.Image(label="源图片（包含要提取的人脸）", type="pil")
            with gr.Column():
                target_image = gr.Image(label="目标图片（需要被替换人脸的图片）", type="pil")
        
        auth_token = gr.Textbox(label="认证令牌", placeholder="输入您的认证令牌", type="password")
        submit_btn = gr.Button("开始换脸")
        
        with gr.Row():
            output_image = gr.Image(label="处理结果")
            output_message = gr.Textbox(label="处理信息")
        
        submit_btn.click(
            fn=process_face_swap,
            inputs=[source_image, target_image, auth_token],
            outputs=[output_image, output_message]
        )
    
    return demo


if __name__ == "__main__":
    demo = create_gradio_interface()
    demo.launch(server_name="0.0.0.0", server_port=16001)