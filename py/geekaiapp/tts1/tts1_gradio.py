import os
import sys
import gradio as gr
import requests
import json
from pathlib import Path

# 将项目根目录添加到 Python 路径
sys.path.append(str(Path(__file__).parent.parent.parent))

from geekaiapp.g_utils import (
    upload_cos, tencent_region, tencent_secret_id,
    tencent_secret_key, tencent_bucket, microsoft_api_key, 
    microsoft_base_url, save_audio_file, ip_tts, ip
)
from openai import OpenAI

# 微软服务客户端
client = OpenAI(
    api_key=microsoft_api_key,
    base_url=microsoft_base_url
)

# 获取当前程序运行目录并创建必要的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
temp_dir = os.path.join(current_dir, 'temp')
output_dir = os.path.join(current_dir, 'static')
tts_dir = os.path.join(output_dir, 'tts')
os.makedirs(temp_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)
os.makedirs(tts_dir, exist_ok=True)

# 支持的语音选项
VOICE_OPTIONS = {
    "中文女声-晓晓": "zh-CN-XiaoxiaoNeural",
    "中文男声-云扬": "zh-CN-YunyangNeural",
    "中文女声-晓伊": "zh-CN-XiaoyiNeural",
    "中文男声-云希": "zh-CN-YunxiNeural",
    "英文女声-Aria": "en-US-AriaNeural",
    "英文男声-Davis": "en-US-DavisNeural",
    "英文女声-Jenny": "en-US-JennyNeural",
    "英文男声-Guy": "en-US-GuyNeural"
}

# 支持的音频格式
FORMAT_OPTIONS = ["mp3", "wav", "flac", "aac"]

# TTS模型选项
MODEL_OPTIONS = ["tts-1", "tts-1-hd"]

def generate_tts(text, voice_name, model, speed, format_type, upload_to_cos):
    """
    生成文本转语音音频
    """
    try:
        if not text.strip():
            return None, "请输入要转换的文本", "", ""
        
        # 获取语音代码
        voice_code = VOICE_OPTIONS.get(voice_name, "zh-CN-XiaoxiaoNeural")
        
        # 准备请求数据
        data = {
            'model': model,
            'input': text,
            'voice': voice_code,
            'response_format': format_type,
            'speed': speed,
        }
        
        # 调用OpenAI TTS API
        response = client.audio.speech.create(**data)
        
        # 保存音频文件
        filename, output_path = save_audio_file(response.content, tts_dir)
        local_audio_url = f"{ip}{ip_tts}/{filename}"
        
        success_msg = f"✅ 音频生成成功！\n文件名: {filename}"
        
        # 如果选择上传到COS
        cos_url = ""
        if upload_to_cos:
            try:
                etag = upload_cos(
                    'text1', tencent_region, tencent_secret_id, 
                    tencent_secret_key, tencent_bucket, filename, tts_dir
                )
                if etag:
                    cos_url = f"https://{tencent_bucket}.cos.{tencent_region}.myqcloud.com/{filename}"
                    success_msg += f"\n☁️ 已上传到腾讯云COS\nCOS链接: {cos_url}"
                else:
                    success_msg += "\n⚠️ COS上传失败"
            except Exception as e:
                success_msg += f"\n⚠️ COS上传出错: {str(e)}"
        
        return output_path, success_msg, local_audio_url, cos_url
        
    except Exception as e:
        error_msg = f"❌ 生成失败: {str(e)}"
        return None, error_msg, "", ""

def create_interface():
    """
    创建Gradio界面
    """
    with gr.Blocks(title="文本转语音 TTS 系统", theme=gr.themes.Soft()) as interface:
        gr.Markdown(
            """
            # 🎵 文本转语音 TTS 系统
            
            基于Microsoft Edge TTS API的高质量语音合成服务
            
            ### 功能特点:
            - 🌍 支持中英文多种语音
            - 🎛️ 可调节语速
            - 📁 多种音频格式
            - ☁️ 可选腾讯云COS存储
            """
        )
        
        with gr.Row():
            with gr.Column(scale=2):
                # 输入区域
                gr.Markdown("### 📝 输入设置")
                
                text_input = gr.Textbox(
                    label="输入文本",
                    placeholder="请输入要转换为语音的文本...",
                    lines=4,
                    max_lines=10
                )
                
                with gr.Row():
                    voice_dropdown = gr.Dropdown(
                        choices=list(VOICE_OPTIONS.keys()),
                        value="中文女声-晓晓",
                        label="选择语音"
                    )
                    
                    model_dropdown = gr.Dropdown(
                        choices=MODEL_OPTIONS,
                        value="tts-1",
                        label="TTS模型"
                    )
                
                with gr.Row():
                    speed_slider = gr.Slider(
                        minimum=0.25,
                        maximum=4.0,
                        value=1.0,
                        step=0.25,
                        label="语速"
                    )
                    
                    format_dropdown = gr.Dropdown(
                        choices=FORMAT_OPTIONS,
                        value="mp3",
                        label="音频格式"
                    )
                
                upload_checkbox = gr.Checkbox(
                    label="上传到腾讯云COS",
                    value=False
                )
                
                generate_btn = gr.Button(
                    "🎵 生成语音",
                    variant="primary",
                    size="lg"
                )
            
            with gr.Column(scale=2):
                # 输出区域
                gr.Markdown("### 🎧 输出结果")
                
                status_output = gr.Textbox(
                    label="状态信息",
                    lines=6,
                    interactive=False
                )
                
                audio_output = gr.Audio(
                    label="生成的音频",
                    type="filepath"
                )
                
                with gr.Row():
                    local_url_output = gr.Textbox(
                        label="本地访问链接",
                        interactive=False
                    )
                
                with gr.Row():
                    cos_url_output = gr.Textbox(
                        label="COS云存储链接",
                        interactive=False
                    )
        
        # 示例文本
        gr.Markdown("### 📋 示例文本")
        with gr.Row():
            example_texts = [
                "你好，欢迎使用文本转语音系统！",
                "Hello, welcome to our text-to-speech system!",
                "今天天气真不错，适合出去走走。",
                "The quick brown fox jumps over the lazy dog."
            ]
            
            for i, example in enumerate(example_texts):
                gr.Button(
                    f"示例{i+1}",
                    size="sm"
                ).click(
                    lambda x=example: x,
                    outputs=text_input
                )
        
        # 绑定生成按钮事件
        generate_btn.click(
            fn=generate_tts,
            inputs=[
                text_input,
                voice_dropdown,
                model_dropdown,
                speed_slider,
                format_dropdown,
                upload_checkbox
            ],
            outputs=[
                audio_output,
                status_output,
                local_url_output,
                cos_url_output
            ]
        )
        
        # 添加使用说明
        gr.Markdown(
            """
            ### 📖 使用说明
            
            1. **输入文本**: 在文本框中输入要转换的文字
            2. **选择语音**: 根据需要选择中文或英文语音
            3. **调整参数**: 设置语速、模型和音频格式
            4. **生成语音**: 点击生成按钮开始转换
            5. **播放试听**: 在音频播放器中试听生成的语音
            6. **获取链接**: 复制本地或云存储链接用于其他用途
            
            ### ⚙️ 参数说明
            
            - **TTS模型**: `tts-1`(标准质量，速度快) / `tts-1-hd`(高清质量，速度慢)
            - **语速**: 0.25x - 4.0x，1.0为正常语速
            - **音频格式**: 支持mp3、wav、flac、aac格式
            - **COS上传**: 可选择将音频文件上传到腾讯云对象存储
            """
        )
    
    return interface

if __name__ == "__main__":
    # 创建并启动界面
    interface = create_interface()
    interface.launch(
        server_name="0.0.0.0",
        server_port=16003,
        share=False,
        show_error=True
    )