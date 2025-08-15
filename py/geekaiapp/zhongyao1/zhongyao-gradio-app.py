import json
import os
import re
import gradio as gr
from openai import OpenAI
from volcenginesdkarkruntime import Ark

# 初始化OpenAI客户端
client = OpenAI(api_key="sk-c4c99fecf0bb4a09bd5b74d21a728ef5",
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

# 初始化Ark客户端（建议将API Key存储在环境变量 ARK_API_KEY 中）
clientArk = Ark(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=os.getenv("ARK_API_KEY", "d160b0a1-ca46-43d0-8b0d-4b143ed65ae8")  # 建议安全存储
)


def get_yaocai_info(yaocai: str):
    """
    输入指定药材的名称，返回当前药材信息
    :param yaocai: 药材名称
    :return: 格式化的药材信息文本
    """
    try:
        # 构建提示词
        prompt = f"""请以JSON格式返回关于"{yaocai}"的中药材信息，包含以下字段：
        1. name: 药材名称
        2. property: 药性（寒、热、温、凉）
        3. taste: 药味（酸、苦、甘、辛、咸）
        4. meridian: 归经
        5. function: 功效主治
        6. usage: 用法用量
        请确保返回的是合法的JSON格式。
        """

        # 调用DeepSeek API
        response = client.chat.completions.create(
            model="qwen-plus-1220",
            messages=[
                {"role": "system", "content": "你是一个专业的中医药专家，请提供准确的中药材信息。"},
                {"role": "user", "content": prompt}
            ],
            stream=False
        )

        # 获取回复并确保是JSON格式
        result = response.choices[0].message.content

        # 尝试从回复中提取JSON部分
        def extract_json(text):
            # 尝试直接解析
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                pass

            # 尝试使用正则表达式提取JSON部分
            json_pattern = r'\{[\s\S]*\}'
            match = re.search(json_pattern, text)
            if match:
                try:
                    return json.loads(match.group(0))
                except json.JSONDecodeError:
                    pass

            # 尝试清理常见问题并解析
            # 1. 移除可能的Markdown代码块标记
            cleaned_text = re.sub(r'```json|```', '', text).strip()
            # 2. 处理转义字符
            cleaned_text = cleaned_text.replace('\\"', '\"').replace('\\n', '\n')
            try:
                return json.loads(cleaned_text)
            except json.JSONDecodeError:
                pass

            # 如果所有尝试都失败，返回None
            return None

        # 尝试解析JSON
        info = extract_json(result)
        if info:
            # 格式化输出为易读的文本
            formatted_info = f"## {info.get('name', yaocai)}\n\n"
            formatted_info += f"**药性：** {info.get('property', '未知')}\n\n"
            formatted_info += f"**药味：** {info.get('taste', '未知')}\n\n"
            formatted_info += f"**归经：** {info.get('meridian', '未知')}\n\n"
            formatted_info += f"**功效主治：** {info.get('function', '未知')}\n\n"
            formatted_info += f"**用法用量：** {info.get('usage', '未知')}"
            return formatted_info
        else:
            # 如果无法解析JSON，创建一个基本的信息结构
            formatted_info = f"## {yaocai}\n\n"
            formatted_info += f"**原始回复：**\n{result}\n\n"
            formatted_info += "*注：系统无法解析为标准格式，显示原始回复*"
            return formatted_info

    except Exception as e:
        return f"获取药材信息出错：{str(e)}"


def get_yaocai_image(yaocai: str):
    """
    输入指定药材的名称，返回当前药材的图片
    :param yaocai: 药材名称
    :return: 药材的图片URL或None
    """
    max_retries = 2  # 最大重试次数
    retry_count = 0

    while retry_count <= max_retries:
        try:
            # 构建提示词
            prompt = f"高清晰度的{yaocai}中药材实物图片，清晰展示其外观特征，包括颜色、形状和质地，白色背景，专业医药参考图"

            # 调用火山方舟 Doubao Seedream 图像生成API
            imagesResponse = clientArk.images.generate(
                model="doubao-seedream-3-0-t2i-250415",
                prompt=prompt
            )

            # 检查响应中是否有数据
            if hasattr(imagesResponse, 'data') and len(imagesResponse.data) > 0 and hasattr(imagesResponse.data[0],
                                                                                            'url'):
                return imagesResponse.data[0].url
            else:
                print(f"图片生成响应格式异常: {imagesResponse}")
                retry_count += 1
                continue

        except Exception as e:
            print(f"获取药材图片出错 (尝试 {retry_count + 1}/{max_retries + 1}): {str(e)}")
            retry_count += 1
            if retry_count <= max_retries:
                continue
            else:
                break

    # 所有尝试都失败，返回None
    return None


def query_yaocai(yaocai_name):
    """整合药材信息和图片查询的函数"""
    try:
        # 输入验证
        if not yaocai_name or yaocai_name.strip() == "":
            return "请输入药材名称", None

        yaocai_name = yaocai_name.strip()
        print(f"开始查询药材: {yaocai_name}")

        # 获取药材信息
        info = get_yaocai_info(yaocai_name)

        # 获取药材图片
        image_url = get_yaocai_image(yaocai_name)

        # 如果图片获取失败，提供友好提示
        if not image_url:
            info += "\n\n*注：药材图片生成失败，请稍后再试*"

        return info, image_url

    except Exception as e:
        error_message = f"## 查询出错\n\n查询 '{yaocai_name}' 时发生错误: {str(e)}\n\n请稍后重试。"
        return error_message, None


# 创建Gradio界面
with gr.Blocks(title="中药材查询系统", theme=gr.themes.Soft()) as app:
    gr.Markdown(
        """
        # 中药材查询系统
    
        输入中药材名称，获取详细信息和图片。
        """
    )

    with gr.Row():
        with gr.Column(scale=1):
            # 输入区域
            yaocai_input = gr.Textbox(label="药材名称", placeholder="请输入中药材名称，如：人参、黄芪等")
            query_btn = gr.Button("查询", variant="primary")

        with gr.Column(scale=3):
            # 输出区域
            with gr.Row():
                with gr.Column(scale=2):
                    info_output = gr.Markdown(label="药材信息")
                with gr.Column(scale=1):
                    image_output = gr.Image(label="药材图片")

    # 设置事件
    query_btn.click(fn=query_yaocai, inputs=yaocai_input, outputs=[info_output, image_output])
    yaocai_input.submit(fn=query_yaocai, inputs=yaocai_input, outputs=[info_output, image_output])

    # 示例
    gr.Examples(
        examples=["人参", "黄芪", "当归", "枸杞子", "灵芝"],
        inputs=yaocai_input,
        outputs=[info_output, image_output],
        fn=query_yaocai,
        cache_examples=True,
    )

# 启动应用
if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=15803, share=True)