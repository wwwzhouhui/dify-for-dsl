# LaTeX转Word工具 - Gradio版本

这是一个基于Gradio的可视化LaTeX转Word工具，提供友好的Web界面来转换LaTeX文档为Microsoft Word格式。

## 功能特点

- ✅ **完整LaTeX支持**: 支持完整的LaTeX语法
- ✅ **数学公式处理**: 自动处理数学公式（使用MathML）
- ✅ **格式保持**: 保持文档结构和格式
- ✅ **多元素支持**: 支持表格、列表、图片等元素
- ✅ **云存储上传**: 自动上传到腾讯云COS
- ✅ **本地下载**: 提供本地文件下载选项
- ✅ **实时预览**: Web界面实时显示转换状态

## 安装要求

### 系统依赖
1. **Python 3.8+**
2. **Pandoc**: LaTeX转换引擎
   - Windows: 下载安装包 https://pandoc.org/installing.html
   - 或使用包管理器: `choco install pandoc`

### Python依赖
```bash
pip install -r requirements.txt
```

主要依赖包括：
- `gradio>=4.0.0` - Web界面框架
- `fastapi>=0.100.0` - API框架
- `cos-python-sdk-v5>=1.9.0` - 腾讯云存储SDK
- `requests>=2.28.0` - HTTP请求库

## 使用方法

### 1. 启动应用
```bash
cd geekaiapp/laTex1
python latex_gradio.py
```

### 2. 访问界面
应用启动后会自动打开浏览器，或手动访问：
```
http://localhost:16002
```

### 3. 转换文档
1. 在左侧文本框中输入LaTeX代码
2. 点击"🔄 转换为Word"按钮
3. 等待转换完成
4. 下载生成的Word文档

### 4. 示例功能
- 点击"📄 加载示例"可以加载预设的LaTeX示例
- 点击"🗑️ 清空"可以清空输入内容

## 界面说明

### 输入区域
- **LaTeX源代码框**: 输入您的LaTeX文档内容
- **转换按钮**: 开始转换过程
- **示例按钮**: 加载示例LaTeX代码
- **清空按钮**: 清空所有输入

### 输出区域
- **状态信息**: 显示转换进度和结果
- **下载文档**: 提供本地Word文档下载
- **云存储链接**: 显示上传到云端的文件链接

## 支持的LaTeX元素

- 文档结构（章节、段落）
- 数学公式（行内和行间）
- 列表（有序和无序）
- 表格
- 图片引用
- 交叉引用
- 文献引用
- 特殊字符和符号

## 配置说明

### 云存储配置
应用使用腾讯云COS进行文件存储，相关配置在`g_utils.py`中：
```python
tencent_region = 'ap-nanjing'
tencent_secret_id = 'your_secret_id'
tencent_secret_key = 'your_secret_key'
tencent_bucket = 'your_bucket_name'
```

### 端口配置
默认端口为16002，可在代码中修改：
```python
demo.launch(server_port=16002)
```

## 故障排除

### 常见问题

1. **Pandoc未找到**
   ```
   错误: 未找到Pandoc
   解决: 安装Pandoc并确保在PATH中
   ```

2. **模块导入错误**
   ```
   错误: ModuleNotFoundError: No module named 'geekaiapp'
   解决: 确保在正确的目录中运行，或检查Python路径
   ```

3. **转换失败**
   ```
   错误: Pandoc转换失败
   解决: 检查LaTeX语法是否正确
   ```

4. **上传失败**
   ```
   错误: 上传到COS失败
   解决: 检查网络连接和COS配置
   ```

### 调试模式
启用详细日志：
```python
logging.basicConfig(level=logging.DEBUG)
```

## 技术架构

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐
│   Gradio Web    │───▶│   Python     │───▶│     Pandoc      │
│   Interface     │    │   Backend    │    │   Converter     │
└─────────────────┘    └──────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────┐
                       │ Tencent COS  │
                       │   Storage    │
                       └──────────────┘
```

## 开发说明

### 文件结构
```
laTex1/
├── latex_gradio.py      # 主应用文件
├── latex_jiekou.py      # 原始FastAPI接口
├── latex_mcp_jiekou.py  # MCP接口版本
├── requirements.txt     # 依赖列表
├── README.md           # 说明文档
├── temp/               # 临时文件目录
└── static/             # 静态文件目录
```

### 核心函数
- `latex_to_word()`: 主转换函数
- `create_sample_latex()`: 生成示例LaTeX
- `create_interface()`: 创建Gradio界面
- `upload_cos()`: 上传到云存储

## 许可证

本项目基于原有的LaTeX转换功能开发，遵循相同的许可证条款。

## 贡献

欢迎提交Issue和Pull Request来改进这个工具！

---

**注意**: 请确保您的LaTeX代码语法正确，并且已安装所有必要的依赖。如有问题，请查看日志输出或联系开发者。