# Markdown转思维导图 - Gradio版本

这是一个基于Gradio的可视化工具，可以将Markdown文档转换为交互式思维导图。

## 🚀 功能特点

- 📝 支持标准Markdown语法
- 🧠 自动生成交互式思维导图
- 🌐 支持云端存储和分享
- 📱 响应式Web界面
- ⚡ 快速转换处理
- 🎯 支持本地预览和下载

## 📋 系统要求

### 必需软件
- Python 3.8+
- Node.js 14+
- npm

### Python依赖
```bash
pip install -r requirements.txt
```

### Node.js依赖
```bash
npm install -g markmap-cli
```

## 🛠️ 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd geekaiapp/markdown2map
```

2. **安装Python依赖**
```bash
pip install -r requirements.txt
```

3. **安装markmap-cli**
```bash
npm install -g markmap-cli
```

4. **配置环境变量**
确保以下环境变量已设置（可选，用于云存储）：
```bash
TENCENT_REGION=ap-nanjing
TENCENT_SECRET_ID=your_secret_id
TENCENT_SECRET_KEY=your_secret_key
TENCENT_BUCKET=your_bucket_name
```

## 🎯 使用方法

### 启动应用
```bash
python marp1_gradio.py
```

### 访问界面
打开浏览器访问：http://localhost:16008

### 操作步骤
1. 在文本框中输入或粘贴Markdown内容
2. 点击"🚀 转换为思维导图"按钮
3. 等待转换完成
4. 通过预览链接查看思维导图
5. 可下载生成的HTML文件

## 📝 Markdown语法支持

支持标准Markdown语法，包括：
- 标题（# ## ### 等）
- 列表（- * + 1. 等）
- 链接和图片
- 代码块
- 表格
- 引用

### 示例Markdown
```markdown
# 主题
## 子主题1
### 详细内容1
- 要点1
- 要点2
## 子主题2
### 详细内容2
- 要点3
- 要点4
```

## 🔧 技术架构

- **前端界面**: Gradio
- **转换引擎**: markmap-cli
- **云存储**: 腾讯云COS
- **后端处理**: Python
- **文件管理**: 本地文件系统

## 📁 项目结构

```
markdown2map/
├── marp1_gradio.py      # Gradio主应用
├── marp1_jiekou.py      # 原FastAPI接口
├── requirements.txt     # Python依赖
├── README.md           # 说明文档
├── static/             # 静态文件目录
│   ├── markdown/       # Markdown文件存储
│   └── html/          # HTML文件存储
└── temp/              # 临时文件目录
```

## 🌐 API接口

如果需要API接口，可以使用原有的FastAPI版本：
```bash
python marp1_jiekou.py
```

API端点：`POST /api/markdown2map/upload`

## 🐛 故障排除

### 常见问题

1. **markmap-cli未找到**
   ```bash
   npm install -g markmap-cli
   ```

2. **端口被占用**
   - 修改代码中的端口号（默认16008）
   - 或关闭占用端口的程序

3. **权限错误**
   - 确保对static目录有写权限
   - Windows用户可能需要以管理员身份运行

4. **云存储上传失败**
   - 检查腾讯云配置
   - 确保网络连接正常
   - 本地功能不受影响

### 日志查看
应用会输出详细的日志信息，包括：
- 文件创建状态
- 转换过程信息
- 错误详情

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 📄 许可证

本项目采用MIT许可证。

## 🔗 相关链接

- [Gradio官方文档](https://gradio.app/)
- [markmap项目](https://markmap.js.org/)
- [Markdown语法指南](https://www.markdownguide.org/)