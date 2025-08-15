import os
import sys
import json
import gradio as gr
from openai import OpenAI
import logging
from typing import List, Dict, Any

# 将项目根目录添加到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from geekaiapp.g_model import JMRequest
from geekaiapp.g_utils import ai_api_key, ai_base_url, ai_model, system_prompt

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 获取当前程序运行目录并创建必要的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
temp_dir = os.path.join(current_dir, 'temp')
output_dir = os.path.join(current_dir, 'static')
filters_dir = os.path.join(current_dir, 'filters')
tts_dir = os.path.join(output_dir, 'tts')
os.makedirs(temp_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)
os.makedirs(tts_dir, exist_ok=True)

# 硅基流动大模型服务
client2 = OpenAI(
    api_key=ai_api_key,
    base_url=ai_base_url
)

def process_word_comparison(input_text: str) -> str:
    """
    处理单词比对功能
    """
    try:
        # 解析输入的JSON文本
        if not input_text.strip():
            return "请输入有效的JSON格式数据"
        
        try:
            data = json.loads(input_text)
        except json.JSONDecodeError:
            return "输入格式错误，请确保是有效的JSON格式"
        
        logger.info(f"处理单词比对请求，数据长度: {len(data) if isinstance(data, list) else 1}")
        
        # 调用AI模型进行处理
        response = client2.chat.completions.create(
            model=ai_model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": json.dumps(data, ensure_ascii=False)
                }
            ],
            response_format={
                'type': 'json_object'
            }
        )
        
        result = json.loads(response.choices[0].message.content)
        return json.dumps(result, ensure_ascii=False, indent=2)
        
    except Exception as e:
        logger.error(f"处理单词比对时发生错误: {str(e)}")
        return f"处理失败: {str(e)}"

def create_demo_data() -> str:
    """
    创建示例数据
    """
    demo_data = [
        {
            "序号": 1,
            "汉语": "n.哨兵 n./vt.守卫,保卫,看守",
            "英语": "guard"
        },
        {
            "序号": 9,
            "汉语": "n.报酬,奖赏 vt.奖励,奖赏,报答",
            "英语": "reward"
        },
        {
            "序号": 10,
            "汉语": "n.保证(书),保修单 vt.保证,提供(产品)保修单",
            "英语": "quarter"
        },
        {
            "序号": 11,
            "汉语": "vt.保证 n.令状,凭单,正当理由",
            "英语": "warrant"
        },
        {
            "序号": 50,
            "汉语": "n.面纱,遮蔽物 vt.掩饰;[文]遮掩",
            "英语": "veil"
        }
    ]
    return json.dumps(demo_data, ensure_ascii=False, indent=2)

def create_gradio_interface():
    """
    创建Gradio界面
    """
    # 自定义CSS样式
    custom_css = """
    .main-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
    }
    
    .input-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .output-container {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .demo-button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .demo-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    .process-button {
        background: linear-gradient(45deg, #f093fb, #f5576c);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 30px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .process-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(245, 87, 108, 0.4);
    }
    
    .scrollable-textbox textarea {
        max-height: 400px !important;
        overflow-y: auto !important;
        resize: vertical !important;
    }
    """
    
    with gr.Blocks(css=custom_css, title="单词比对系统") as demo:
        gr.HTML("""
        <div style="text-align: center; padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin-bottom: 30px; color: white;">
            <h1 style="margin: 0; font-size: 2.5em; font-weight: 700;">🔤 单词比对系统</h1>
            <p style="margin: 10px 0 0 0; font-size: 1.2em; opacity: 0.9;">基于AI的智能单词比对与分析工具</p>
        </div>
        """)
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.HTML('<div class="input-container">')
                gr.Markdown("### 📝 输入数据")
                
                input_textbox = gr.Textbox(
                    label="JSON格式的单词数据",
                    placeholder="请输入JSON格式的单词数据...",
                    lines=15,
                    elem_classes=["scrollable-textbox"]
                )
                
                with gr.Row():
                    demo_btn = gr.Button(
                        "📋 加载示例数据",
                        elem_classes=["demo-button"]
                    )
                    process_btn = gr.Button(
                        "🚀 开始比对",
                        elem_classes=["process-button"],
                        variant="primary"
                    )
                
                gr.HTML('</div>')
                
            with gr.Column(scale=1):
                gr.HTML('<div class="output-container">')
                gr.Markdown("### 📊 比对结果")
                
                output_textbox = gr.Textbox(
                    label="AI分析结果",
                    lines=15,
                    elem_classes=["scrollable-textbox"],
                    interactive=False
                )
                
                gr.HTML('</div>')
        
        # 使用说明
        gr.HTML("""
        <div style="background: #f8f9fa; border-radius: 12px; padding: 20px; margin-top: 30px; border-left: 4px solid #667eea;">
            <h3 style="color: #667eea; margin-top: 0;">📖 使用说明</h3>
            <div style="line-height: 1.6;">
                <p><strong>1. 数据格式：</strong>请输入包含单词信息的JSON数组</p>
                <p><strong>2. 字段说明：</strong></p>
                <ul>
                    <li><code>序号</code>: 单词序号</li>
                    <li><code>汉语</code>: 中文释义</li>
                    <li><code>英语</code>: 英文单词</li>
                </ul>
                <p><strong>3. 操作步骤：</strong></p>
                <ol>
                    <li>点击"加载示例数据"查看数据格式</li>
                    <li>输入或修改您的单词数据</li>
                    <li>点击"开始比对"进行AI分析</li>
                </ol>
            </div>
        </div>
        """)
        
        # 事件绑定
        demo_btn.click(
            fn=create_demo_data,
            outputs=input_textbox
        )
        
        process_btn.click(
            fn=process_word_comparison,
            inputs=input_textbox,
            outputs=output_textbox
        )
    
    return demo

if __name__ == "__main__":
    # 创建并启动Gradio应用
    demo = create_gradio_interface()
    
    # 启动应用
    demo.launch(
        server_name="0.0.0.0",
        server_port=16006,
        share=False,
        debug=True,
        show_error=True
    )
    
    print("\n🎉 单词比对系统已启动!")
    print("📱 访问地址: http://localhost:16006")
    print("🔧 调试模式: 已开启")