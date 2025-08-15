import os
import sys
import gradio as gr
import requests
import json
from PIL import Image
from io import BytesIO
import urllib3
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import ssl
from urllib3.poolmanager import PoolManager
import base64

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 自定义HTTPAdapter来处理SSL问题
class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        ctx.set_ciphers('DEFAULT@SECLEVEL=1')
        kwargs['ssl_context'] = ctx
        return super().init_poolmanager(*args, **kwargs)

# 将项目根目录添加到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from geekaiapp.g_model import JMRequest
from config import config

# 获取当前程序运行目录并创建必要的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
temp_dir = os.path.join(current_dir, 'temp')
static_dir = os.path.join(current_dir, 'static')
os.makedirs(temp_dir, exist_ok=True)
os.makedirs(static_dir, exist_ok=True)

def images_to_html(image_urls):
    """
    将图像URL列表转换为高级HTML显示格式，支持预览、下载和放大功能
    """
    if not image_urls:
        return "<div style='text-align: center; padding: 20px; color: #666;'>暂无图片</div>"
    
    # 生成唯一ID避免冲突
    import time
    import json
    unique_id = str(int(time.time() * 1000))
    
    html_parts = []
    
    # 添加CSS样式和JavaScript功能
    html_parts.append(f"""
    <style>
        .gallery-container-{unique_id} {{
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }}
        
        .gallery-grid-{unique_id} {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 20px;
        }}
        
        .gallery-item-{unique_id} {{
            position: relative;
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .gallery-item-{unique_id}:hover {{
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 20px 40px rgba(0,0,0,0.25);
        }}
        
        .gallery-image-{unique_id} {{
            width: 100%;
            height: 200px;
            object-fit: cover;
            cursor: pointer;
            transition: transform 0.3s ease;
        }}
        
        .gallery-item-{unique_id}:hover .gallery-image-{unique_id} {{
            transform: scale(1.05);
        }}
        
        .gallery-overlay-{unique_id} {{
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: linear-gradient(transparent, rgba(0,0,0,0.8));
            padding: 15px;
            transform: translateY(100%);
            transition: transform 0.3s ease;
        }}
        
        .gallery-item-{unique_id}:hover .gallery-overlay-{unique_id} {{
            transform: translateY(0);
        }}
        
        .gallery-title-{unique_id} {{
            color: white;
            font-size: 14px;
            margin-bottom: 10px;
            font-weight: 500;
        }}
        
        .gallery-buttons-{unique_id} {{
            display: flex;
            gap: 10px;
        }}
        
        .gallery-btn-{unique_id} {{
            flex: 1;
            padding: 8px 16px;
            border: none;
            border-radius: 6px;
            font-size: 12px;
            cursor: pointer;
            transition: all 0.2s ease;
            font-weight: 500;
        }}
        
        .gallery-btn-preview-{unique_id} {{
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
        }}
        
        .gallery-btn-preview-{unique_id}:hover {{
            background: linear-gradient(45deg, #5a6fd8, #6a4190);
            transform: translateY(-1px);
        }}
        
        .gallery-btn-download-{unique_id} {{
            background: linear-gradient(45deg, #f093fb, #f5576c);
            color: white;
        }}
        
        .gallery-btn-download-{unique_id}:hover {{
            background: linear-gradient(45deg, #e081e9, #e3455a);
            transform: translateY(-1px);
        }}
        
        .gallery-modal-{unique_id} {{
            display: none;
            position: fixed;
            z-index: 10000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.9);
            backdrop-filter: blur(5px);
        }}
        
        .gallery-modal-content-{unique_id} {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            max-width: 90%;
            max-height: 90%;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 25px 50px rgba(0,0,0,0.5);
        }}
        
        .gallery-modal-image-{unique_id} {{
            width: 100%;
            height: auto;
            display: block;
        }}
        
        .gallery-modal-close-{unique_id} {{
            position: absolute;
            top: 15px;
            right: 25px;
            color: white;
            font-size: 35px;
            font-weight: bold;
            cursor: pointer;
            z-index: 10001;
            background: rgba(0,0,0,0.5);
            border-radius: 50%;
            width: 50px;
            height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
        }}
        
        .gallery-modal-close-{unique_id}:hover {{
            background: rgba(255,255,255,0.2);
            transform: scale(1.1);
        }}
    </style>
    """)
    
    # 图片容器开始
    html_parts.append(f'<div class="gallery-container-{unique_id}">')
    html_parts.append(f'<div class="gallery-grid-{unique_id}">')
    
    # 生成图片项
    for i, url in enumerate(image_urls):
        img_html = f"""
        <div class="gallery-item-{unique_id}">
            <img class="gallery-image-{unique_id}" 
                 src="{url}" 
                 alt="图片 {i+1}" 
                 onclick="window.openGalleryModal_{unique_id}({i})" />
            <div class="gallery-overlay-{unique_id}">
                <div class="gallery-title-{unique_id}">图片 {i+1}</div>
                <div class="gallery-buttons-{unique_id}">
                    <button class="gallery-btn-{unique_id} gallery-btn-preview-{unique_id}" 
                            onclick="window.openGalleryModal_{unique_id}({i})">🔍 预览</button>
                    <button class="gallery-btn-{unique_id} gallery-btn-download-{unique_id}" 
                            onclick="window.downloadGalleryImage_{unique_id}({i})">📥 下载</button>
                </div>
            </div>
        </div>
        """
        html_parts.append(img_html)
    
    # 图片容器结束
    html_parts.append('</div>')
    html_parts.append('</div>')
    
    # 添加模态框
    html_parts.append(f"""
    <div id="galleryModal_{unique_id}" class="gallery-modal-{unique_id}">
        <span class="gallery-modal-close-{unique_id}" onclick="window.closeGalleryModal_{unique_id}()">&times;</span>
        <div class="gallery-modal-content-{unique_id}">
            <img id="galleryModalImage_{unique_id}" class="gallery-modal-image-{unique_id}" />
        </div>
    </div>
    """)
    
    # 将图片URL列表转换为JSON字符串
    image_urls_json = json.dumps(image_urls)
    
    # 添加JavaScript功能 - 使用事件委托和DOMContentLoaded
    html_parts.append(f"""
    <script>
        (function() {{
            // 图片URL数组
            const imageUrls_{unique_id} = {image_urls_json};
            
            // 确保在DOM完全加载后执行
            function initGallery_{unique_id}() {{
                // 定义函数到window对象
                window.openGalleryModal_{unique_id} = function(index) {{
                    const modal = document.getElementById('galleryModal_{unique_id}');
                    const modalImg = document.getElementById('galleryModalImage_{unique_id}');
                    
                    if (modal && modalImg && imageUrls_{unique_id}[index]) {{
                        modal.style.display = 'block';
                        modalImg.src = imageUrls_{unique_id}[index];
                        document.body.style.overflow = 'hidden';
                    }}
                }};
                
                window.closeGalleryModal_{unique_id} = function() {{
                    const modal = document.getElementById('galleryModal_{unique_id}');
                    if (modal) {{
                        modal.style.display = 'none';
                        document.body.style.overflow = 'auto';
                    }}
                }};
                
                window.downloadGalleryImage_{unique_id} = function(index) {{
                    if (imageUrls_{unique_id}[index]) {{
                        const link = document.createElement('a');
                        link.href = imageUrls_{unique_id}[index];
                        link.download = `image_${{index + 1}}.jpg`;
                        link.target = '_blank';
                        document.body.appendChild(link);
                        link.click();
                        document.body.removeChild(link);
                    }}
                }};
                
                // 添加事件监听器
                document.addEventListener('keydown', function(event) {{
                    if (event.key === 'Escape') {{
                        window.closeGalleryModal_{unique_id}();
                    }}
                }});
                
                document.addEventListener('click', function(event) {{
                    const modal = document.getElementById('galleryModal_{unique_id}');
                    if (event.target === modal) {{
                        window.closeGalleryModal_{unique_id}();
                    }}
                }});
            }}
            
            // 多重初始化策略
            if (document.readyState === 'loading') {{
                document.addEventListener('DOMContentLoaded', initGallery_{unique_id});
            }} else {{
                initGallery_{unique_id}();
            }}
            
            // 备用延迟初始化
            setTimeout(initGallery_{unique_id}, 1000);
            setTimeout(initGallery_{unique_id}, 2000);
        }})();
    </script>
    """)
    
    return "".join(html_parts)

def generate_image(api_key, api_url, model, prompt, negative_prompt, width, height, sample_strength):
    """
    调用即梦API生成图像 - 增强版本，支持多URL重试和更好的错误处理
    """
    config.log_info(f"开始生成图像，提示词: {prompt[:50]}...")
    
    # 创建请求对象
    request_data = JMRequest(
        image_api_key=api_key,
        image_generation_url=api_url,
        model=model,
        prompt=prompt,
        negativePrompt=negative_prompt,
        width=int(width),
        height=int(height),
        sample_strength=float(sample_strength)
    )
    
    # 准备请求数据
    data = {
        "model": request_data.model,
        "prompt": request_data.prompt,
        "negativePrompt": request_data.negativePrompt,
        "width": request_data.width,
        "height": request_data.height,
        "sample_strength": request_data.sample_strength,
    }
    
    # 获取要尝试的URL列表
    urls_to_try = [api_url] + [url for url in config.get_api_urls() if url != api_url]
    
    last_error = None
    
    for attempt, url in enumerate(urls_to_try, 1):
        try:
            config.log_info(f"尝试第 {attempt} 个URL: {url}")
            result = _make_api_request(url, api_key, data)
            if result:
                return result
        except Exception as e:
            last_error = e
            config.log_error(e, f"URL {url} 请求失败")
            continue
    
    # 所有URL都失败了
    error_msg = f'<div style="padding: 10px; border: 1px solid #ddd; border-radius: 5px; background-color: #ffe6e6;">❌ 所有API地址都无法访问<br/>最后一个错误: {str(last_error)}</div>'
    config.log_error(Exception(f"所有API地址都无法访问。最后一个错误: {str(last_error)}"), "API请求完全失败")
    error_html = "<div style='text-align: center; padding: 40px; color: #ff6b6b; font-size: 16px;'>❌ 所有API地址都无法访问</div>"
    return error_html, error_msg, str(last_error)

def _make_api_request(url, api_key, data):
    """
    执行单个API请求
    """
    try:
        # 获取请求头
        headers = config.get_headers(api_key)
        
        # 创建会话并配置重试策略和SSL处理
        session = requests.Session()
        retry_strategy = Retry(
            total=config.max_retries,
            backoff_factor=config.backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST"]
        )
        
        # 使用自定义SSL适配器
        ssl_adapter = SSLAdapter(max_retries=retry_strategy)
        session.mount("http://", ssl_adapter)
        session.mount("https://", ssl_adapter)
        
        # 发送请求，使用多种SSL配置
        response = session.post(
            url, 
            headers=headers, 
            json=data, 
            verify=config.verify_ssl,
            timeout=(config.connect_timeout, config.read_timeout),
            stream=False
        )
        response.raise_for_status()
        
        result = response.json()
        config.log_info(f"API响应成功: {url}")
        
        # 处理响应结果
        if "data" in result and len(result["data"]) > 0:
            images = []
            image_urls = []
            
            # 处理所有图片
            for item in result["data"]:
                if "url" in item:
                    image_url = item["url"]
                    image_urls.append(image_url)
                    config.log_info(f"获取到图像URL: {image_url}")
                    
                    try:
                        # 下载图像
                        img_response = session.get(image_url, verify=config.verify_ssl, timeout=(config.connect_timeout, config.read_timeout))
                        img_response.raise_for_status()
                        
                        # 转换为PIL图像
                        image = Image.open(BytesIO(img_response.content))
                        images.append(image)
                    except Exception as e:
                        config.log_error(e, f"下载图像失败: {image_url}")
                        continue
            
            if images:
                # 格式化图像URL为可点击的超链接，每个URL一行
                url_links = []
                for i, img_url in enumerate(image_urls, 1):
                    url_links.append(f'<div style="margin: 5px 0;">图片{i}: <a href="{img_url}" target="_blank" style="color: #007bff; text-decoration: none;">{img_url}</a></div>')
                formatted_urls = "".join(url_links)
                
                success_msg = f'<div style="padding: 10px; border: 1px solid #ddd; border-radius: 5px; background-color: #f0f8ff;">✅ 图像生成成功！共生成 {len(images)} 张图片<br/>🔗 图像URL:<br/>{formatted_urls}<br/>📊 使用API: {url}</div>'
                html_content = images_to_html(image_urls)
                return html_content, success_msg, json.dumps(result, indent=2, ensure_ascii=False)
            else:
                error_msg = f'<div style="padding: 10px; border: 1px solid #ddd; border-radius: 5px; background-color: #ffe6e6;">❌ 图像下载失败：所有图片都无法下载<br/>🔗 API: {url}</div>'
                config.log_error(Exception("图像下载失败"), f"URL: {url}")
                no_image_html = "<div style='text-align: center; padding: 40px; color: #ff6b6b; font-size: 16px;'>❌ 图像下载失败</div>"
                return no_image_html, error_msg, json.dumps(result, indent=2, ensure_ascii=False)
        else:
            error_msg = f'<div style="padding: 10px; border: 1px solid #ddd; border-radius: 5px; background-color: #ffe6e6;">❌ 图像生成失败：API响应格式异常<br/>🔗 API: {url}</div>'
            config.log_error(Exception("API响应格式异常"), f"URL: {url}, Response: {result}")
            error_html = "<div style='text-align: center; padding: 40px; color: #ff6b6b; font-size: 16px;'>❌ API响应格式异常</div>"
            return error_html, error_msg, json.dumps(result, indent=2, ensure_ascii=False)
            
    except requests.exceptions.RequestException as e:
        config.log_error(e, f"请求异常 - URL: {url}")
        raise e
    except Exception as e:
        config.log_error(e, f"未知错误 - URL: {url}")
        raise e

def create_gradio_interface():
    """
    创建Gradio界面
    """
    # 自定义CSS样式
    custom_css = """
    .scrollable-textbox textarea {
        max-height: 300px !important;
        overflow-y: auto !important;
        resize: vertical !important;
    }
    
    #gallery, .image-gallery {
        min-height: 400px !important;
    }
    
    #gallery .gallery-item, .image-gallery .gallery-item {
        width: 100% !important;
        height: auto !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }
    
    /* 高级图像显示样式 */
    #advanced-image-display {
        min-height: 400px;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        background: #f8f9fa;
    }
    
    .advanced-image-gallery {
        padding: 16px;
    }
    
    .image-gallery-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 20px;
        padding: 20px;
        background: #f8f9fa;
        border-radius: 12px;
    }
    
    .image-item {
        position: relative;
        background: white;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .image-item:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .image-preview {
        width: 100%;
        height: 200px;
        object-fit: cover;
        cursor: pointer;
    }
    
    .image-controls {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(transparent, rgba(0,0,0,0.7));
        padding: 15px;
        display: flex;
        gap: 10px;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .image-item:hover .image-controls {
        opacity: 1;
    }
    
    .control-btn {
        flex: 1;
        padding: 8px 12px;
        border: none;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .preview-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .preview-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    .download-btn {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
    }
    
    .download-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(245, 87, 108, 0.4);
    }
    
    /* 模态框样式 */
    .modal {
        display: none;
        position: fixed;
        z-index: 10000;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.9);
        backdrop-filter: blur(10px);
    }
    
    .modal-content {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        max-width: 90%;
        max-height: 90%;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 20px 60px rgba(0,0,0,0.5);
    }
    
    .modal-image {
        width: 100%;
        height: auto;
        display: block;
    }
    
    .close {
        position: absolute;
        top: 20px;
        right: 30px;
        color: white;
        font-size: 40px;
        font-weight: bold;
        cursor: pointer;
        z-index: 10001;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    .close:hover {
        color: #f093fb;
        transform: scale(1.1);
    }
    """
    
    with gr.Blocks(title="即梦文生图 - Gradio界面", theme=gr.themes.Soft(), css=custom_css) as demo:
        gr.Markdown("# 🎨 即梦文生图生成器")
        gr.Markdown("使用即梦API生成高质量的AI图像")
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("## 📝 配置参数")
                
                # API配置
                with gr.Group():
                    gr.Markdown("### 🔑 API配置")
                    api_key = gr.Textbox(
                        label="API Key",
                        placeholder="请输入您的API密钥",
                        type="password",
                        value="77368c766017f0b5afe148bb744e7c8b"
                    )
                    api_url = gr.Textbox(
                        label="API URL",
                        placeholder="请输入API地址",
                        value="http://g10.geekaiapp.icu/v1/images/generations"
                    )
                
                # 模型配置
                with gr.Group():
                    gr.Markdown("### 🤖 模型配置")
                    model = gr.Dropdown(
                        label="模型",
                        choices=["jimeng-2.1", "jimeng-2.0", "jimeng-1.4"],
                        value="jimeng-2.1"
                    )
                
                # 提示词配置
                with gr.Group():
                    gr.Markdown("### 💭 提示词配置")
                    prompt = gr.Textbox(
                        label="正向提示词",
                        placeholder="描述您想要生成的图像...",
                        lines=3,
                        value="皮卡丘抱着埃菲尔铁塔"
                    )
                    negative_prompt = gr.Textbox(
                        label="负向提示词",
                        placeholder="描述您不想要的元素...",
                        lines=2,
                        value=""
                    )
                
                # 图像参数配置
                with gr.Group():
                    gr.Markdown("### 🖼️ 图像参数")
                    with gr.Row():
                        width = gr.Slider(
                            label="宽度",
                            minimum=512,
                            maximum=2048,
                            step=64,
                            value=1080
                        )
                        height = gr.Slider(
                            label="高度",
                            minimum=512,
                            maximum=2048,
                            step=64,
                            value=720
                        )
                    
                    sample_strength = gr.Slider(
                        label="采样强度",
                        minimum=0.1,
                        maximum=1.0,
                        step=0.1,
                        value=0.5
                    )
                
                # 生成按钮
                generate_btn = gr.Button(
                    "🎨 生成图像",
                    variant="primary",
                    size="lg"
                )
            
            with gr.Column(scale=1):
                gr.Markdown("## 🖼️ 生成结果")
                
                # 高级图像显示区域
                output_images = gr.HTML(
                    value="<div style='text-align: center; padding: 40px; color: #666; font-size: 16px;'>🎨 点击生成按钮开始创作...</div>",
                    elem_id="advanced-image-display",
                    elem_classes="advanced-image-gallery"
                )
                
                # 状态信息
                status_text = gr.HTML(
                    value="<div style='padding: 10px; border: 1px solid #ddd; border-radius: 5px; background-color: #f9f9f9;'>等待生成图像...</div>",
                    label="状态信息"
                )
                
                # API响应详情
                with gr.Accordion("📋 API响应详情", open=False):
                    api_response = gr.Textbox(
                        label="完整响应",
                        lines=15,
                        interactive=False,
                        show_copy_button=True,
                        elem_classes="scrollable-textbox"
                    )
        
        # 示例
        gr.Markdown("## 💡 示例提示词")
        with gr.Row():
            example_prompts = [
                "一只可爱的小猫咪坐在彩虹上",
                "未来科技城市的夜景，霓虹灯闪烁",
                "古代中国山水画风格的风景",
                "宇宙中的星云和行星"
            ]
            
            for example in example_prompts:
                gr.Button(example, size="sm").click(
                    lambda x=example: x,
                    outputs=prompt
                )
        
        # 绑定生成按钮事件
        generate_btn.click(
            fn=generate_image,
            inputs=[
                api_key,
                api_url,
                model,
                prompt,
                negative_prompt,
                width,
                height,
                sample_strength
            ],
            outputs=[output_images, status_text, api_response]
        )
        
        # 添加使用说明
        with gr.Accordion("📖 使用说明", open=True):
            gr.Markdown("""
            ### 如何使用：
            1. **配置API**: 输入您的API密钥和API地址
            2. **选择模型**: 选择合适的即梦模型版本
            3. **编写提示词**: 在正向提示词中描述您想要的图像
            4. **设置参数**: 调整图像尺寸和采样强度
            5. **生成图像**: 点击生成按钮开始创作
            
            ### 提示词技巧：
            - 使用具体、详细的描述
            - 包含风格、颜色、构图等信息
            - 负向提示词用于排除不想要的元素
            
            ### 参数说明：
            - **采样强度**: 控制生成的随机性，值越高越随机
            - **图像尺寸**: 建议使用16:9或4:3比例
            """)
    
    return demo

if __name__ == "__main__":
    # 创建并启动Gradio界面
    demo = create_gradio_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=16014,
        share=True,
        debug=True
    )