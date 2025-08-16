import os
import subprocess
import sys
import time
import gradio as gr
import logging
from pathlib import Path

# 将项目根目录添加到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from geekaiapp.g_utils import upload_cos, tencent_region, tencent_secret_id, \
    tencent_secret_key, tencent_bucket

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 获取当前程序运行目录并创建必要的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
temp_dir = os.path.join(current_dir, 'temp')
output_dir = os.path.join(current_dir, 'static')
os.makedirs(temp_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

def latex_to_word(latex_content):
    """
    将LaTeX内容转换为Word文档
    
    Args:
        latex_content (str): LaTeX源代码
        
    Returns:
        tuple: (状态信息, 下载链接, 本地文件路径)
    """
    if not latex_content or not latex_content.strip():
        return "❌ 请输入LaTeX内容", None, None
    
    try:
        # 生成时间戳作为文件名
        time_name = str(int(time.time()))
        tex_file_name = f"{time_name}.tex"
        docx_file_name = f"{time_name}.docx"
        
        # 创建LaTeX文件
        tex_file = os.path.join(temp_dir, tex_file_name)
        with open(tex_file, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        
        logger.info(f"LaTeX文件已创建: {tex_file}")
        
        # 确定输出文件路径
        docx_file = os.path.join(temp_dir, docx_file_name)
        
        # 使用pandoc转换
        cmd = [
            'pandoc',
            tex_file,
            '-o', docx_file,
            '--from=latex',
            '--to=docx',
            '--mathml'
        ]
        
        result = subprocess.run(
            cmd,
            cwd=temp_dir,
            capture_output=True,
            shell=True,
            text=True
        )
        
        if result.returncode != 0:
            error_msg = f"Pandoc转换失败:\n标准输出: {result.stdout}\n错误输出: {result.stderr}"
            logger.error(error_msg)
            return f"❌ 转换失败: {result.stderr}", None, None
        
        # 检查输出文件是否存在
        if not os.path.exists(docx_file):
            return "❌ 转换失败: 输出文件未生成", None, None
        
        # 上传到腾讯云COS
        try:
            oss_url = upload_cos(
                'text12', tencent_region, tencent_secret_id, 
                tencent_secret_key, tencent_bucket, docx_file_name, temp_dir
            )
            
            if oss_url:
                success_msg = f"✅ 转换成功!\n文件名: {docx_file_name}\n已上传到云存储"
                return success_msg, oss_url, docx_file
            else:
                # 如果上传失败，仍然返回本地文件
                warning_msg = f"⚠️ 转换成功，但上传到云存储失败\n文件名: {docx_file_name}\n可下载本地文件"
                return warning_msg, None, docx_file
                
        except Exception as upload_error:
            logger.error(f"上传到COS失败: {str(upload_error)}")
            warning_msg = f"⚠️ 转换成功，但上传失败: {str(upload_error)}\n文件名: {docx_file_name}"
            return warning_msg, None, docx_file
            
    except subprocess.CalledProcessError as e:
        error_msg = f"❌ 转换过程出错:\n{e.output}\n{e.stderr}"
        logger.error(error_msg)
        return error_msg, None, None
    except Exception as e:
        error_msg = f"❌ 发生未知错误: {str(e)}"
        logger.error(error_msg)
        return error_msg, None, None

def create_sample_latex():
    """
    创建示例LaTeX内容
    """
    sample = r"""\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage{amsmath}
\usepackage{amsfonts}
\usepackage{amssymb}

\title{LaTeX转Word示例文档}
\author{Gradio演示}
\date{\today}

\begin{document}

\maketitle

\section{介绍}
这是一个LaTeX转Word的示例文档。本工具可以将LaTeX源代码转换为Microsoft Word格式。

\section{数学公式}
这里是一些数学公式的例子：

\subsection{行内公式}
爱因斯坦的质能方程：$E = mc^2$

\subsection{行间公式}
二次方程的解：
\begin{equation}
x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
\end{equation}

\subsection{矩阵}
一个简单的矩阵：
\begin{equation}
A = \begin{pmatrix}
a & b \\
c & d
\end{pmatrix}
\end{equation}

\section{列表}
\begin{itemize}
\item 第一项
\item 第二项
\item 第三项
\end{itemize}

\begin{enumerate}
\item 编号项目1
\item 编号项目2
\item 编号项目3
\end{enumerate}

\section{结论}
这个工具可以帮助您快速将LaTeX文档转换为Word格式，方便与他人协作和分享。

\end{document}"""
    return sample

def clear_inputs():
    """
    清空输入
    """
    return "", "请输入LaTeX内容...", None

# 创建Gradio界面
def create_interface():
    with gr.Blocks(
        title="LaTeX转Word工具",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 1200px !important;
        }
        .main-header {
            text-align: center;
            margin-bottom: 30px;
        }
        .feature-box {
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
            background-color: #f9f9f9;
        }
        """
    ) as demo:
        
        gr.HTML("""
        <div class="main-header">
            <h1>🔄 LaTeX转Word工具</h1>
            <p>将LaTeX源代码快速转换为Microsoft Word文档</p>
        </div>
        """)
        
        with gr.Row():
            with gr.Column(scale=2):
                gr.HTML('<div class="feature-box"><h3>📝 输入LaTeX内容</h3></div>')
                
                latex_input = gr.Textbox(
                    label="LaTeX源代码",
                    placeholder="请在此输入您的LaTeX代码...",
                    lines=15,
                    max_lines=25,
                    value=""
                )
                
                with gr.Row():
                    convert_btn = gr.Button("🔄 转换为Word", variant="primary", size="lg")
                    sample_btn = gr.Button("📄 加载示例", variant="secondary")
                    clear_btn = gr.Button("🗑️ 清空", variant="secondary")
            
            with gr.Column(scale=1):
                gr.HTML('<div class="feature-box"><h3>📊 转换结果</h3></div>')
                
                status_output = gr.Textbox(
                    label="状态信息",
                    value="请输入LaTeX内容...",
                    lines=5,
                    interactive=False
                )
                
                download_file = gr.File(
                    label="下载Word文档",
                    visible=True
                )
                
                cloud_link = gr.Textbox(
                    label="云存储链接",
                    placeholder="转换成功后将显示下载链接",
                    interactive=False
                )
        
        # 功能说明
        gr.HTML("""
        <div class="feature-box">
            <h3>🔧 功能特点</h3>
            <ul>
                <li>✅ 支持完整的LaTeX语法</li>
                <li>✅ 自动处理数学公式（使用MathML）</li>
                <li>✅ 保持文档结构和格式</li>
                <li>✅ 支持表格、列表、图片等元素</li>
                <li>✅ 自动上传到云存储</li>
                <li>✅ 提供本地下载选项</li>
            </ul>
        </div>
        """)
        
        gr.HTML("""
        <div class="feature-box">
            <h3>📋 使用说明</h3>
            <ol>
                <li>在左侧文本框中输入您的LaTeX代码</li>
                <li>点击"转换为Word"按钮开始转换</li>
                <li>转换完成后可以下载Word文档</li>
                <li>如果上传成功，还会提供云存储链接</li>
            </ol>
            <p><strong>注意：</strong>请确保您的LaTeX代码语法正确，工具使用Pandoc进行转换。</p>
        </div>
        """)
        
        # 事件绑定
        def handle_conversion(latex_content):
            status, cloud_url, local_file = latex_to_word(latex_content)
            
            # 返回状态、云链接、本地文件
            cloud_display = cloud_url if cloud_url else ""
            file_display = local_file if local_file and os.path.exists(local_file) else None
            
            return status, cloud_display, file_display
        
        convert_btn.click(
            fn=handle_conversion,
            inputs=[latex_input],
            outputs=[status_output, cloud_link, download_file]
        )
        
        sample_btn.click(
            fn=create_sample_latex,
            outputs=[latex_input]
        )
        
        clear_btn.click(
            fn=clear_inputs,
            outputs=[latex_input, status_output, download_file]
        )
    
    return demo

if __name__ == '__main__':
    # 检查pandoc是否安装
    try:
        result = subprocess.run(['pandoc', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            logger.info("Pandoc已安装，版本信息:")
            logger.info(result.stdout.split('\n')[0])
        else:
            logger.warning("Pandoc未正确安装")
    except FileNotFoundError:
        logger.error("未找到Pandoc，请先安装Pandoc: https://pandoc.org/installing.html")
    
    # 创建并启动界面
    demo = create_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=16002,
        share=False,
        show_error=True,
        inbrowser=True
    )