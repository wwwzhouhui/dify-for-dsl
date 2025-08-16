# BeArt AI 换脸系统 - Gradio 界面

这是一个基于Gradio的BeArt AI换脸系统界面，允许用户通过Web界面上传源图片和目标图片进行换脸操作。

## 功能特点

- 简洁的Web界面，易于使用
- 支持多种图片格式（jpg/png/gif/webp/bmp）
- 集成腾讯云COS存储
- 安全的API认证机制

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行应用

```bash
python bf_gradio.py
```

应用将在 http://localhost:16001 启动。

## 使用方法

1. 打开浏览器访问 http://localhost:16001
2. 上传源图片（包含要提取的人脸）
3. 上传目标图片（需要被替换人脸的图片）
4. 输入认证令牌（默认可用令牌："sk-geekaiapp"或"geekaiapp"）
5. 点击"开始换脸"按钮
6. 等待处理完成，查看结果

## 注意事项

- 图片质量和人脸清晰度会影响换脸效果
- 处理大图片可能需要较长时间
- 确保网络连接正常，以便与BeArt AI服务器通信