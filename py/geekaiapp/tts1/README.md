# 🎵 文本转语音 TTS 系统

基于Microsoft Edge TTS API和Gradio的高质量语音合成可视化系统。

## ✨ 功能特点

- 🌍 **多语言支持**: 支持中英文多种语音选择
- 🎛️ **参数可调**: 语速、模型、音频格式自由调节
- 🎧 **实时预览**: 生成后立即可以播放试听
- ☁️ **云存储**: 可选择上传到腾讯云COS
- 🖥️ **可视化界面**: 基于Gradio的友好用户界面
- 📱 **响应式设计**: 支持桌面和移动端访问

## 🚀 快速开始

### 1. 安装依赖

```bash
cd geekaiapp/tts1
pip install -r requirements.txt
```

### 2. 环境配置

确保以下环境变量已设置（在项目根目录的.env文件中）:

```env
# Microsoft TTS API
MICROSOFT_API_KEY=your_api_key
MICROSOFT_BASE_URL=https://g4.geekaiapp.icu/v1

# 腾讯云COS配置（可选）
TENCENT_REGION=your_region
TENCENT_SECRET_ID=your_secret_id
TENCENT_SECRET_KEY=your_secret_key
TENCENT_BUCKET=your_bucket

# 服务配置
IP=http://localhost:15001/
IP_TTS=static/tts
```

### 3. 启动服务

#### 方式一：启动Gradio可视化界面

```bash
python tts1_gradio.py
```

访问: http://localhost:16003

#### 方式二：启动FastAPI接口服务

```bash
python tts1_jiekou.py
```

访问: http://localhost:16003

## 📖 使用说明

### Gradio界面使用

1. **输入文本**: 在文本框中输入要转换的文字
2. **选择语音**: 根据需要选择中文或英文语音
3. **调整参数**: 设置语速、模型和音频格式
4. **生成语音**: 点击生成按钮开始转换
5. **播放试听**: 在音频播放器中试听生成的语音
6. **获取链接**: 复制本地或云存储链接用于其他用途

### API接口使用

```bash
curl --location 'http://localhost:16003/api/edge/tts12/' \
--header 'Authorization: Bearer geekaiapp' \
--header 'Content-Type: application/json' \
--data '{
    "input":"你好，这是一个测试文本。",
    "voice": "zh-CN-XiaoxiaoNeural",
    "model": "tts-1",
    "speed": 1.0,
    "response_format": "mp3"
}'
```

## 🎛️ 参数说明

### 语音选项

| 语音名称 | 语音代码 | 语言 | 性别 |
|---------|---------|------|------|
| 中文女声-晓晓 | zh-CN-XiaoxiaoNeural | 中文 | 女 |
| 中文男声-云扬 | zh-CN-YunyangNeural | 中文 | 男 |
| 中文女声-晓伊 | zh-CN-XiaoyiNeural | 中文 | 女 |
| 中文男声-云希 | zh-CN-YunxiNeural | 中文 | 男 |
| 英文女声-Aria | en-US-AriaNeural | 英文 | 女 |
| 英文男声-Davis | en-US-DavisNeural | 英文 | 男 |
| 英文女声-Jenny | en-US-JennyNeural | 英文 | 女 |
| 英文男声-Guy | en-US-GuyNeural | 英文 | 男 |

### 模型选项

- **tts-1**: 标准质量，生成速度快
- **tts-1-hd**: 高清质量，生成速度较慢

### 其他参数

- **语速**: 0.25x - 4.0x，1.0为正常语速
- **音频格式**: mp3、wav、flac、aac
- **COS上传**: 可选择将音频文件上传到腾讯云对象存储

## 📁 文件结构

```
tts1/
├── tts1_gradio.py      # Gradio可视化界面
├── tts1_jiekou.py      # FastAPI接口服务
├── requirements.txt    # 依赖包列表
├── README.md          # 说明文档
├── static/            # 静态文件目录
│   └── tts/          # 音频文件存储
└── temp/             # 临时文件目录
```

## 🔧 故障排除

### 常见问题

1. **模块导入错误**
   - 确保已安装所有依赖: `pip install -r requirements.txt`
   - 检查Python路径设置

2. **音频生成失败**
   - 检查Microsoft API配置
   - 确认网络连接正常
   - 验证API密钥有效性

3. **文件保存错误**
   - 确保static/tts目录存在且有写入权限
   - 检查磁盘空间是否充足

4. **COS上传失败**
   - 验证腾讯云配置信息
   - 检查存储桶权限设置

## 📝 更新日志

### v1.0.0
- ✅ 基础TTS功能实现
- ✅ Gradio可视化界面
- ✅ 多语音支持
- ✅ 腾讯云COS集成
- ✅ 参数可调节
- ✅ 实时音频预览

## 📄 许可证

本项目采用MIT许可证。

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目！