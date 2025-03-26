from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from spire.doc import Document, FileFormat
import os
import time
import logging
from pydantic import BaseModel

app = FastAPI(title="Markdown to Word Converter")

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
class MarkdownContent(BaseModel):
    content: str

# 获取当前程序运行目录并创建必要的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
temp_dir = os.path.join(current_dir, 'temp')
output_dir = os.path.join(current_dir, 'output')
os.makedirs(temp_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

@app.post("/office/word/convert")
async def convert_md_to_docx(request: Request):
    logger.info('Received request for /convert')
    content = await request.body()
    if not content:
        logger.error('No content part in the request')
        return JSONResponse(content={"error": "No content part"}, status_code=400)

    content = content.decode('utf-8')
    if content == '':
        logger.error('No content provided')
        return JSONResponse(content={"error": "No content provided"}, status_code=400)
    
    # 从请求的内容中读取
    mdfile_name = str(int(time.time())) + ".md"
    md_file_path = os.path.join(temp_dir, mdfile_name)
    with open(md_file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    # 创建文档实例
    doc = Document()

    # 从上传的文件加载Markdown内容
    doc.LoadFromFile(md_file_path, FileFormat.Markdown)
    
    # 将Markdown文件转换为Word文档并保存
    file_name = str(int(time.time())) + ".docx"
    output_path = os.path.join(output_dir, file_name)
    doc.SaveToFile(output_path, FileFormat.Docx)

    # 释放资源
    doc.Dispose()
    
    # 清理临时文件
    if os.path.exists(md_file_path):
        os.remove(md_file_path)

    # 返回文件的下载链接
    base_url = str(request.base_url)
    download_url = base_url + 'office/word/download/' + os.path.basename(output_path)
    print(download_url)
    return {"download_url": download_url}

@app.get("/office/word/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(output_dir, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, filename=filename)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8089)