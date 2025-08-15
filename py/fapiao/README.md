# 🧾 智能发票申请单处理系统

基于LangGPT提示词工程技术的智能发票申请单处理系统，支持从Excel文件中提取发票数据，生成专业的发票预览，并提供数据导出功能。

## ✨ 核心特性

- **🎯 智能提取**: 基于LangGPT提示词专家技术，自动识别Excel中的发票申请单结构
- **📄 多发票支持**: 一次处理多张申请单，支持发票间快速切换预览
- **🎨 专业预览**: 仿真发票样式的可视化界面，支持打印功能
- **💾 数据导出**: 支持JSON格式的结构化数据导出
- **📱 响应式设计**: 适配各种屏幕尺寸的现代化界面

## 📋 系统要求

- Python 3.11+
- 现代浏览器 (Chrome, Firefox, Safari, Edge)
- 支持Excel格式文件 (.xlsx, .xls)

## 🚀 快速部署

### 使用 Docker 部署（推荐）

#### 1. 构建 Docker 镜像

```bash
# 构建镜像
docker build -t fapiaosqd:latest .
```

#### 2. 使用 Docker Compose 部署

```bash
# 启动服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f fapiaosqd

# 停止服务
docker-compose down
```

#### 3. 直接使用 Docker 运行

```bash
# 创建必要的目录
mkdir -p uploads exports

# 运行容器
docker run -d \
  --name fapiaosqd-web \
  -p 15601:15601 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/exports:/app/exports \
  --restart unless-stopped \
  wwwzhouhui569/fapiaosqd:latest
```

#### 4. 访问应用

部署完成后，在浏览器中访问：
- **Web界面**: http://localhost:15601

### 本地开发部署

```bash
# 安装依赖
pip install -r requirements.txt

# 运行应用
python fapiaosqd.py
```

## 📁 项目结构

```
.
├── fapiaosqd.py          # 主应用程序
├── fapiaosqd.css         # 样式文件
├── requirements.txt      # Python依赖
├── Dockerfile           # Docker镜像构建文件
├── docker-compose.yml   # Docker Compose配置
├── README.md           # 项目说明文档
└── 测试数据/
    └── 测试数据.xlsx    # 测试用Excel文件
```

## 📖 使用指南

### 📤 文件上传
1. 点击"上传发票申请单"区域
2. 选择Excel格式的发票申请单文件
3. 系统将自动开始处理

### 🔍 数据预览
- **发票切换**: 如果文件包含多张发票，可通过顶部标签页切换
- **详细信息**: 查看购买方、销售方信息和商品明细
- **金额核对**: 检查不含税金额、税额和价税合计

### 💾 数据导出
1. 点击"导出数据"按钮
2. 系统生成包含所有发票信息的JSON文件
3. 文件包含处理统计和详细的发票数据

### 🖨️ 打印功能
1. 点击"打印预览"按钮
2. 使用浏览器的打印功能 (Ctrl+P)
3. 系统已优化打印样式

## 🔧 配置说明

### Docker 配置

- **端口映射**: 15601 (Gradio Web界面)
- **数据卷**:
  - `./uploads:/app/uploads` - 上传文件存储
  - `./exports:/app/exports` - 导出文件存储

### 环境要求

- Python 3.11+
- Gradio 4.0.0+
- openpyxl 3.1.0+
- Docker (可选，用于容器化部署)

## 🛠️ 维护命令

```bash
# 查看容器状态
docker ps

# 进入容器
docker exec -it fapiaosqd-web bash

# 查看容器日志
docker logs fapiaosqd-web

# 重启服务
docker-compose restart

# 更新镜像
docker-compose pull
docker-compose up -d

# 清理未使用的镜像
docker image prune -f
```

## 🚨 故障排除

### 常见问题

#### 文件上传失败
- **检查文件格式**: 确保是Excel格式 (.xlsx, .xls)
- **检查文件大小**: 避免过大的文件
- **检查文件权限**: 确保文件可读

#### 数据提取错误
- **检查Excel结构**: 确保包含"发票申请单"标识
- **检查数据完整性**: 确保必要字段不为空
- **检查编码格式**: 确保中文字符正确显示

#### 界面显示问题
- **清除浏览器缓存**: 刷新页面
- **检查浏览器兼容性**: 使用现代浏览器
- **检查网络连接**: 确保本地服务正常

---

*基于LangGPT提示词工程技术，为财务数字化转型提供专业解决方案*