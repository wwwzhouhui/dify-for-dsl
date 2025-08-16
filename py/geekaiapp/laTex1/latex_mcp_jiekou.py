import os
import subprocess
import sys
import time
from fastapi import FastAPI, HTTPException, APIRouter, Request, BackgroundTasks
from fastapi.responses import StreamingResponse
import asyncio
import logging
from typing import AsyncGenerator

# 将项目根目录添加到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from geekaiapp.g_utils import upload_cos, tencent_region, tencent_secret_id, tencent_secret_key, tencent_bucket, ip_md

# MCP配置 - 遵循MCP架构规范
class MCPConfig:
    SERVICE_NAME = "latex_converter"
    VERSION = "1.0"
    SSE_EVENT_TYPE = "latex_conversion_status"
    MAX_RETRY_COUNT = 3

# 配置日志 - MCP标准日志格式
logging.basicConfig(
    level=logging.INFO,
    format=f"%(asctime)s [%(levelname)s] [{MCPConfig.SERVICE_NAME}] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# 创建FastAPI应用 - MCP服务入口
app = FastAPI(
    title=f"{MCPConfig.SERVICE_NAME} Service",
    version=MCPConfig.VERSION,
    description="MCP风格的LaTeX转换服务，支持SSE实时通知"
)
router = APIRouter(prefix="/api/mcp")

# 服务层 - MCP业务逻辑分离
class LaTeXConversionService:
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.temp_dir = os.path.join(self.current_dir, 'temp')
        self.output_dir = os.path.join(self.current_dir, 'static')
        os.makedirs(self.temp_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        self.status_updates = {}  # 存储转换任务状态，用于SSE

    async def generate_tex_file(self, latex_content: str) -> tuple[str, str]:
        """生成LaTeX临时文件"""
        time_name = str(int(time.time()))
        tex_file_name = f"{time_name}.tex"
        docx_file_name = f"{time_name}.docx"
        tex_file = os.path.join(self.temp_dir, tex_file_name)

        with open(tex_file, 'w', encoding='utf-8') as f:
            f.write(latex_content)

        logger.info(f"LaTeX file created: {ip_md}/{tex_file_name}")
        return tex_file_name, docx_file_name

    def convert_to_docx(self, tex_file_name: str, docx_file_name: str) -> str:
        """执行LaTeX到DOCX的转换"""
        tex_file = os.path.join(self.temp_dir, tex_file_name)
        docx_file = os.path.join(self.temp_dir, docx_file_name)

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
            cwd=self.temp_dir,
            capture_output=True,
            shell=True,
            text=True
        )

        if result.returncode != 0:
            logger.error(f"Conversion failed: {result.stderr}")
            raise subprocess.CalledProcessError(
                result.returncode, result.args, output=result.stdout, stderr=result.stderr
            )

        return docx_file

    def upload_to_cos(self, docx_file_name: str) -> str:
        """上传DOCX文件到COS"""
        etag = upload_cos(
            'text12', tencent_region, tencent_secret_id, 
            tencent_secret_key, tencent_bucket, docx_file_name, self.temp_dir
        )

        if etag:
            return f"https://{tencent_bucket}.cos.{tencent_region}.myqcloud.com/{docx_file_name}"
        raise HTTPException(status_code=500, detail="Failed to upload to COS")

# 初始化服务实例 - MCP单例模式
conversion_service = LaTeXConversionService()

# 后台任务 - MCP异步处理
async def process_conversion_task(task_id: str, latex_content: str, status_queue: asyncio.Queue):
    try:
        await status_queue.put("Generating LaTeX file...")
        tex_file_name, docx_file_name = await conversion_service.generate_tex_file(latex_content)

        await status_queue.put("Converting to DOCX...")
        loop = asyncio.get_event_loop()
        docx_file = await loop.run_in_executor(
            None, conversion_service.convert_to_docx, tex_file_name, docx_file_name
        )

        await status_queue.put("Uploading to COS...")
        oss_url = await loop.run_in_executor(
            None, conversion_service.upload_to_cos, docx_file_name
        )

        await status_queue.put(f"Completed|{oss_url}|{docx_file_name}")
    except Exception as e:
        await status_queue.put(f"Error|{str(e)}")
    finally:
        status_queue.task_done()

# SSE端点 - MCP实时通知接口
@router.post("/latextword/sse", response_class=StreamingResponse)
async def latextword_sse(request: Request):
    """MCP风格的SSE接口，用于LaTeX到DOCX的转换"""
    content = await request.body()
    latex_content = content.decode('utf-8')
    task_id = f"task_{int(time.time())}"
    status_queue = asyncio.Queue()

    # 启动后台转换任务
    background_tasks = BackgroundTasks()
    background_tasks.add_task(process_conversion_task, task_id, latex_content, status_queue)

    # SSE事件生成器
    async def event_generator():
        while True:
            if await request.is_disconnected():
                logger.warning(f"Client disconnected, task {task_id} cancelled")
                break

            try:
                status = await asyncio.wait_for(status_queue.get(), timeout=1.0)
                if status.startswith("Completed|"):
                    _, oss_url, docx_file_name = status.split("|")
                    yield f"event: completed\ndata: {{\"docx_file_name\": \"{docx_file_name}\", \"output_path\": \"{oss_url}\"}}\n\n"
                    break
                elif status.startswith("Error|"):
                    _, error_msg = status.split("|")
                    yield f"event: error\ndata: {{\"error\": \"{error_msg}\"}}\n\n"
                    break
                else:
                    yield f"event: status\ndata: {{\"message\": \"{status}\"}}\n\n"
            except asyncio.TimeoutError:
                continue

    # MCP标准响应头
    headers = {
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'text/event-stream'
    }

    return StreamingResponse(
        event_generator(),
        headers=headers,
        background=background_tasks
    )

# 标准HTTP端点 - 保持向后兼容
@router.post("/latextword")
async def latextword(request: Request):
    """标准HTTP接口，用于LaTeX到DOCX的转换"""
    content = await request.body()
    latex_content = content.decode('utf-8')

    try:
        tex_file_name, docx_file_name = await conversion_service.generate_tex_file(latex_content)
        loop = asyncio.get_event_loop()
        docx_file = await loop.run_in_executor(
            None, conversion_service.convert_to_docx, tex_file_name, docx_file_name
        )
        oss_url = await loop.run_in_executor(
            None, conversion_service.upload_to_cos, docx_file_name
        )

        return {
            "docx_file_name": docx_file_name,
            "output_path": oss_url
        }
    except Exception as e:
        return f"Error generating file: {str(e)}"

# 注册路由 - MCP路由管理
app.include_router(router)

# MCP服务元数据接口
@router.get("/metadata")
async def get_metadata():
    """获取MCP服务元数据"""
    return {
        "service_name": MCPConfig.SERVICE_NAME,
        "version": MCPConfig.VERSION,
        "endpoints": [
            {"path": "/api/mcp/latextword", "method": "POST", "description": "Standard LaTeX to DOCX conversion"},
            {"path": "/api/mcp/latextword/sse", "method": "POST", "description": "SSE-enabled LaTeX to DOCX conversion"},
            {"path": "/api/mcp/metadata", "method": "GET", "description": "Service metadata"}
        ]
    }

# 启动服务 - MCP入口点
if __name__ == '__main__':
    import uvicorn
    logger.info(f"Starting {MCPConfig.SERVICE_NAME} service v{MCPConfig.VERSION} on port 16002")
    uvicorn.run(app, host="0.0.0.0", port=16002, log_level="info", reload=False)