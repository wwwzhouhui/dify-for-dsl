import os
import subprocess
import sys
import time

from fastapi import Request

# 将项目根目录添加到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.routing import APIRoute, Mount

from geekaiapp.g_utils import upload_cos, tencent_region, tencent_secret_id, \
    tencent_secret_key, tencent_bucket, ip_md

app = FastAPI(debug=True)

router = APIRouter()

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 获取当前程序运行目录并创建必要的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
temp_dir = os.path.join(current_dir, 'temp')
output_dir = os.path.join(current_dir, 'static')
filters_dir = os.path.join(current_dir, 'filters')
os.makedirs(temp_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)


# g把laTex转换成word
@router.post('/latextword')
async def latextword(request: Request, output_path=None):
    content = await request.body()
    latex_content = content.decode('utf-8')
    time_name = str(int(time.time()))  # 生成时间戳作为文件名
    tex_file_name = time_name + ".tex"  # Markdown文件名
    docx_file_name = time_name + ".docx"  # HTML文件名
    # 创建markdown和html文件夹，如果它们不存在的话
    os.makedirs('../static/markdown', exist_ok=True)
    os.makedirs('../static/html', exist_ok=True)
    tex_file = os.path.join(temp_dir, tex_file_name)
    with open(tex_file, 'w', encoding='utf-8') as f:
        f.write(latex_content)
    print(f"Markdown file created: {ip_md}/{tex_file_name}")
    # 确定输出文件路径
    if output_path is None:
        docx_file = os.path.join(temp_dir, docx_file_name)
    else:
        docx_file = output_path
    try:
        cmd = [
            'pandoc',
            tex_file,
            '-o', docx_file,
            '--from=latex',
            '--to=docx',
            '--mathml',
            # '--filter', filter_script,
            # '--reference-doc=custom-template.docx'
        ]

        result = subprocess.run(
            cmd,
            cwd=temp_dir,
            capture_output=True,
            shell=True,
            text=True
        )

        if result.returncode != 0:
            raise subprocess.CalledProcessError(result.returncode, result.args, output=result.stdout,
                                                stderr=result.stderr)
        # return f'点击预览: {ip}temp/{docx_file_name}'
        # Upload to COS
        etag = upload_cos('text12', tencent_region, tencent_secret_id, tencent_secret_key, tencent_bucket,
                          docx_file_name,
                          temp_dir)
        if etag:
            oss_url = f"https://{tencent_bucket}.cos.{tencent_region}.myqcloud.com/{docx_file_name}"
            return {
                "docx_file_name": docx_file_name,
                "output_path": oss_url
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to upload audio to COS")
    except subprocess.CalledProcessError as e:
        return f"Error generating file: {e.output}\n{e.stderr}"


app.include_router(router, prefix="/api")

# 打印所有路由
for route in app.routes:
    if isinstance(route, APIRoute):  # 检查是否为路由
        print(f"Path: {route.path}, Methods: {route.methods}")
    elif isinstance(route, Mount):  # 检查是否为挂载点
        print(f"Mount: {route.path} -> {route.name}")

if __name__ == '__main__':
    import uvicorn

    # 修改启动配置 # 禁用热重载以避免初始化问题
    uvicorn.run(app, host="0.0.0.0", port=16002, log_level="info", reload=False)
