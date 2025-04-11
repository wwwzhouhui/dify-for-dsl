以下是为您整理的完整API接口文档，包含所有可用端点的Postman调用示例（Markdown格式）：

```markdown
# 完整API接口文档

## 1. 语音合成接口

### 1.1 微软TTS基础版
```bash
curl --location 'http://your-api-domain/api/edge/tts1' \
--header 'Content-Type: application/json' \
--data '{
    "model": "tts-1",
    "input": "需要转换为语音的文本内容",
    "voice": "alloy|echo|fable|onyx|nova|shimmer",  # 六种可选音色
    "response_format": "mp3",  # 输出格式
    "speed": 1.0  # 语速(0.5-2.0)
}'
```

### 1.2 微软TTS+腾讯云存储
```bash
curl --location 'http://your-api-domain/api/edge/tts12' \
--header 'Content-Type: application/json' \
--data '{
    "model": "tts-1",
    "input": "需要合成的长文本",
    "voice": "alloy",
    "response_format": "mp3",
    "speed": 1.0
}'
# 返回结果包含腾讯云COS存储地址
```

## 2. 视频生成接口

### 2.1 硅基流动文生视频
```bash
curl --location 'http://your-api-domain/api/gjld/video' \
--header 'Content-Type: application/json' \
--data '{
    "model": "siliconflow-videomodel",  # 可省略使用默认
    "prompt": "高清4K，一只会编程的熊猫坐在电脑前"
}'
```

### 2.2 智谱AI视频生成
```bash
curl --location 'http://your-api-domain/api/zhipuai/video' \
--header 'Content-Type: application/json' \
--data '{
    "prompt": "未来城市夜景，赛博朋克风格",
    "with_audio": false  # 是否带背景音乐
}'
```

### 2.3 即梦AI视频生成（需认证）
```bash
curl --location 'http://your-api-domain/api/jimeng/generate_video' \
--header 'Authorization: Bearer your-access-token' \
--header 'Content-Type: application/json' \
--data '{
    "prompt": "夏日海滩日落场景",
    "aspect_ratio": "16:9",  # 支持9:16/1:1
    "fps": 24,  # 帧率
    "duration_ms": 8000  # 视频时长(毫秒)
}'
```

## 3. AI绘画接口

### 3.1 即梦文生图
```bash
curl --location 'http://your-api-domain/api/jimeng/img' \
--header 'Content-Type: application/json' \
--data '{
    "image_api_key": "your-api-key",
    "model": "stable-diffusion-xl",
    "prompt": "中国山水画风格的老虎",
    "negativePrompt": "模糊，低质量",
    "width": 1024,
    "height": 1024,
    "sample_strength": 0.7  # 强度(0-1)
}'
```

### 3.2 ComfyUI专业绘画
```bash
curl --location 'http://your-api-domain/api/comfyui_bizyairapi' \
--form 'prompt="masterpiece, best quality, a beautiful girl"' \
--form 'seed="123456"' \
--form 'idx="0"' \
--form 'workflowfile=@"/path/to/workflow.json"'
# 需要上传工作流配置文件
```

## 4. 文档处理接口

### 4.1 Markdown转PPT
```bash
curl --location 'http://your-api-domain/api/pptupload' \
--header 'Content-Type: text/markdown' \
--data '# 标题

- 要点1
- 要点2

![图片](image.png)'
```

### 4.2 网页内容转Word
```bash
curl --location 'http://your-api-domain/api/generate_doc' \
--header 'Content-Type: application/json' \
--data '{
    "title": "项目报告",
    "content": "<h1>项目概述</h1><p>详细内容...</p>"
}'
```

### 4.3 Markdown转思维导图
```bash
curl --location 'http://your-api-domain/api/markdown2map/upload' \
--header 'Content-Type: text/markdown' \
--data '# 中心主题
## 分支1
### 子节点
## 分支2'
```

### 4.4 Markdown转Word文档
```bash
curl --location 'http://your-api-domain/api/office/word1' \
--header 'Content-Type: text/markdown' \
--data '## 文档标题

正文内容...'
```

## 5. 特色功能接口

### 5.1 儿童绘本生成
```bash
curl --location 'http://your-api-domain/api/make_ai_txt_picture_audio' \
--header 'Content-Type: application/json' \
--data '[
    {
        "text_snippet": "从前有座山",
        "prompt": "卡通风格的山"
    },
    {
        "text_snippet": "山里有座庙",
        "prompt": "古老的寺庙"
    }
]'
# 返回每页的图片URL和语音URL
```

### 5.2 智能JSON格式化
```bash
curl --location 'http://your-api-domain/api/json1' \
--header 'Content-Type: application/json' \
--data '{
    "messy_data": "需要整理的数据",
    "options": {"format": "standard"}
}'
```

## 调用说明

1. **基础路径**：所有接口前缀为 `/api`
2. **认证方式**：
   - 部分接口需要 `Authorization: Bearer token` 请求头
3. **文件上传**：
   - 使用 `multipart/form-data` 格式
   - 示例：
     ```bash
     curl -F "file=@test.jpg" http://your-api-domain/api/upload
     ```
4. **错误代码**：
   - 200 成功
   - 400 参数错误
   - 401 未授权
   - 500 服务器错误

> 提示：实际调用时请将 `your-api-domain` 替换为您的真实域名，参数值根据业务需求调整
```

这份文档完整包含了：
1. 所有接口的详细调用方式
2. 每个接口的必要参数说明
3. 标准请求格式示例
4. 统一的调用规范说明
5. 不同内容类型的处理方式（JSON/Form-data/文本）

建议保存为`API文档.md`文件，方便团队内部使用。实际调用时请注意替换示例中的测试数据为真实业务数据。