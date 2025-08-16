import os
import subprocess
import sys
import time
import gradio as gr
from pathlib import Path
import logging

# 将项目根目录添加到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

try:
    from geekaiapp.g_utils import ip_md, ip_html, upload_cos, \
        tencent_region, tencent_secret_id, tencent_secret_key, tencent_bucket, current_directory
except ImportError:
    # 如果无法导入，使用默认配置
    print("Warning: Could not import g_utils, using default configuration")
    ip_md = "static/markdown"
    ip_html = "static/html"
    current_directory = Path.cwd()
    
    # 默认腾讯云配置（可选）
    tencent_region = os.getenv('TENCENT_REGION', 'ap-nanjing')
    tencent_secret_id = os.getenv('TENCENT_SECRET_ID', '')
    tencent_secret_key = os.getenv('TENCENT_SECRET_KEY', '')
    tencent_bucket = os.getenv('TENCENT_BUCKET', '')
    
    def upload_cos(*args, **kwargs):
        """Mock upload function when COS is not available"""
        return None

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 确保目录存在
os.makedirs(ip_md, exist_ok=True)
os.makedirs(ip_html, exist_ok=True)

def markdown_to_mindmap(markdown_content):
    """
    将Markdown内容转换为思维导图HTML文件
    
    Args:
        markdown_content (str): Markdown文本内容
        
    Returns:
        tuple: (状态信息, HTML文件路径, 预览URL)
    """
    if not markdown_content.strip():
        return "请输入Markdown内容", None, None
    
    try:
        # 生成时间戳作为文件名
        time_name = str(int(time.time()))
        md_file_name = time_name + ".md"
        html_file_name = time_name + ".html"
        
        # 构建完整路径
        md_file_path = os.path.join(ip_md, md_file_name)
        html_file_path = os.path.join(ip_html, html_file_name)
        
        # 将Markdown内容写入文件
        with open(md_file_path, "w", encoding='utf-8') as f:
            f.write(markdown_content)
        
        logger.info(f"Markdown file created: {md_file_path}")
        
        # 使用subprocess调用markmap-cli将Markdown转换为HTML
        result = subprocess.run(
            ['npx', 'markmap-cli', md_file_path, '--no-open'],
            capture_output=True,
            shell=True,
            text=True
        )
        
        if result.returncode != 0:
            error_msg = f"转换失败: {result.stderr}"
            logger.error(error_msg)
            return error_msg, None, None
        
        # 检查生成的HTML文件是否存在于markdown目录
        temp_html_path = md_file_path.replace('.md', '.html')
        if os.path.exists(temp_html_path):
            # 移动HTML文件到html目录
            os.replace(temp_html_path, html_file_path)
            logger.info(f"HTML file moved to: {html_file_path}")
        else:
            return "HTML文件生成失败", None, None
        
        # 生成预览URL
        preview_url = f"http://localhost:16008/{ip_html}/{html_file_name}"
        
        # 尝试上传到腾讯云COS
        try:
            etag = upload_cos(
                'text1', 
                tencent_region, 
                tencent_secret_id, 
                tencent_secret_key, 
                tencent_bucket,
                html_file_name,
                current_directory / ip_html
            )
            
            if etag:
                cos_url = f"https://{tencent_bucket}.cos.{tencent_region}.myqcloud.com/{html_file_name}"
                success_msg = f"✅ 转换成功！\n📁 本地文件: {html_file_name}\n🌐 云端链接: {cos_url}\n👀 本地预览: {preview_url}"
                return success_msg, html_file_path, cos_url
            else:
                success_msg = f"✅ 转换成功！\n📁 本地文件: {html_file_name}\n👀 本地预览: {preview_url}\n⚠️ 云端上传失败"
                return success_msg, html_file_path, preview_url
                
        except Exception as upload_error:
            logger.warning(f"上传到COS失败: {upload_error}")
            success_msg = f"✅ 转换成功！\n📁 本地文件: {html_file_name}\n👀 本地预览: {preview_url}\n⚠️ 云端上传失败: {upload_error}"
            return success_msg, html_file_path, preview_url
            
    except subprocess.CalledProcessError as e:
        error_msg = f"转换过程出错: {e.output}\n{e.stderr}"
        logger.error(error_msg)
        return error_msg, None, None
    except Exception as e:
        error_msg = f"发生未知错误: {str(e)}"
        logger.error(error_msg)
        return error_msg, None, None

def create_demo_content():
    """
    创建示例Markdown内容
    """
    return """# Java学习路线图

## 基础语法
### 数据类型
- 基本数据类型
  - byte
  - short
  - int
  - long
  - float
  - double
  - char
  - boolean
- 引用数据类型
  - 类
  - 接口
  - 数组

### 运算符
- 算术运算符
- 关系运算符
- 逻辑运算符
- 位运算符
- 赋值运算符
- 其他运算符

### 控制语句
- 条件语句
  - if
  - if-else
  - switch
- 循环语句
  - for
  - while
  - do-while
- 跳转语句
  - break
  - continue
  - return

## 面向对象
### 类与对象
- 类的定义
- 对象的创建
- 构造方法
- 方法重载
- this关键字

### 继承
- 继承的概念
- 方法重写
- super关键字
- final关键字

### 多态
- 多态的概念
- 向上转型
- 向下转型

### 抽象类与接口
- 抽象类
- 接口
- 接口与抽象类的区别

## 异常处理
### 异常分类
- 检查型异常
- 非检查型异常

### 异常处理机制
- try-catch-finally
- throw
- throws

## 集合框架
### 集合接口
- Collection
- List
- Set
- Map

### 集合实现类
- ArrayList
- LinkedList
- HashSet
- TreeSet
- HashMap
- TreeMap

## 多线程
### 线程的创建
- 继承Thread类
- 实现Runnable接口

### 线程的生命周期
- 新建
- 就绪
- 运行
- 阻塞
- 死亡

### 线程同步
- synchronized关键字
- 锁机制
- 线程通信

## IO流
### 字节流
- InputStream
- OutputStream

### 字符流
- Reader
- Writer

### 文件操作
- File类
- 文件读写

## 网络编程
### Socket编程
- TCP协议
- UDP协议

### URL编程
- URL类
- URLConnection类

## 反射机制
### 反射的概念
- Class类
- 获取类的信息
- 动态创建对象
- 动态调用方法

## 泛型
### 泛型的概念
- 泛型类
- 泛型方法
- 泛型接口

### 通配符
- 上限通配符
- 下限通配符

## 注解
### 内置注解
- @Override
- @Deprecated
- @SuppressWarnings

### 自定义注解
- 定义注解
- 使用注解
- 解析注解

## JDBC
### JDBC基础
- JDBC API
- 连接数据库
- 执行SQL语句
- 处理结果集

### 数据库连接池
- DBCP
- C3P0
- Druid"""

def clear_content():
    """
    清空输入内容
    """
    return ""

# 创建Gradio界面
def create_interface():
    with gr.Blocks(
        title="Markdown转思维导图",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 1200px !important;
        }
        .markdown-input {
            font-family: 'Consolas', 'Monaco', monospace;
        }
        """
    ) as demo:
        
        gr.Markdown(
            """
            # 🧠 Markdown转思维导图工具
            
            将您的Markdown文档转换为交互式思维导图，支持本地预览和云端分享。
            
            ## 📝 使用说明
            1. 在下方文本框中输入或粘贴您的Markdown内容
            2. 点击"转换为思维导图"按钮
            3. 等待转换完成，获取预览链接
            
            ## ✨ 功能特点
            - 🎯 支持标准Markdown语法
            - 🌐 自动上传到云端存储
            - 📱 响应式交互界面
            - ⚡ 快速转换处理
            """
        )
        
        with gr.Row():
            with gr.Column(scale=2):
                markdown_input = gr.Textbox(
                    label="📝 Markdown内容",
                    placeholder="请在此输入您的Markdown内容...",
                    lines=20,
                    max_lines=30,
                    elem_classes=["markdown-input"]
                )
                
                with gr.Row():
                    convert_btn = gr.Button(
                        "🚀 转换为思维导图", 
                        variant="primary",
                        size="lg"
                    )
                    demo_btn = gr.Button(
                        "📋 加载示例", 
                        variant="secondary"
                    )
                    clear_btn = gr.Button(
                        "🗑️ 清空内容", 
                        variant="secondary"
                    )
            
            with gr.Column(scale=1):
                status_output = gr.Textbox(
                    label="📊 转换状态",
                    lines=8,
                    interactive=False
                )
                
                file_output = gr.File(
                    label="📁 下载HTML文件",
                    visible=True
                )
                
                preview_link = gr.Textbox(
                    label="🔗 预览链接",
                    placeholder="转换完成后将显示预览链接",
                    interactive=False
                )
        
        # 绑定事件
        convert_btn.click(
            fn=markdown_to_mindmap,
            inputs=[markdown_input],
            outputs=[status_output, file_output, preview_link]
        )
        
        demo_btn.click(
            fn=create_demo_content,
            outputs=[markdown_input]
        )
        
        clear_btn.click(
            fn=clear_content,
            outputs=[markdown_input]
        )
        
        # 添加使用提示
        gr.Markdown(
            """
            ## 💡 提示
            - 确保您的系统已安装 Node.js 和 markmap-cli
            - 安装命令: `npm install -g markmap-cli`
            - 支持的Markdown语法包括标题、列表、链接等
            - 生成的思维导图支持缩放、拖拽等交互操作
            
            ## 🔧 技术栈
            - **前端**: Gradio
            - **转换工具**: markmap-cli
            - **云存储**: 腾讯云COS
            - **后端**: Python + FastAPI
            """
        )
    
    return demo

if __name__ == "__main__":
    # 创建并启动Gradio应用
    demo = create_interface()
    
    # 启动服务
    demo.launch(
        server_name="0.0.0.0",
        server_port=16008,
        share=False,
        show_error=True,
        quiet=False
    )