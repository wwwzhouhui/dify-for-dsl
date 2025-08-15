import os
import subprocess
import sys
import time

# 将项目根目录添加到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openai import OpenAI
from geekaiapp.g_utils import ai_api_key, ai_base_url, ip_md, ip_html, upload_cos, \
    tencent_region, tencent_secret_id, tencent_secret_key, tencent_bucket, current_directory

import logging
from fastapi import FastAPI, APIRouter, Request, HTTPException
from fastapi.routing import APIRoute, Mount

app = FastAPI(debug=True)

router = APIRouter()

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 硅基流动大模型服务
client2 = OpenAI(
    api_key=ai_api_key,
    base_url=ai_base_url
)


# g把markdown2思维导图
@router.post('/markdown2map/upload')
async def upload_markdown2map(request: Request):
    content = await request.body()
    content = content.decode('utf-8')
    time_name = str(int(time.time()))  # 生成时间戳作为文件名
    md_file_name = time_name + ".md"  # Markdown文件名
    html_file_name = time_name + ".html"  # HTML文件名

    # 创建markdown和html文件夹，如果它们不存在的话
    os.makedirs('../static/markdown', exist_ok=True)
    os.makedirs('../static/html', exist_ok=True)

    # 将Markdown内容写入文件
    with open(f'{ip_md}/{md_file_name}', "w", encoding='utf-8') as f:
        f.write(content)

    print(f"Markdown file created: {ip_md}/{md_file_name}")

    # 使用subprocess调用markmap-cli将Markdown转换为HTML，并移动到static/html目录
    try:
        result = subprocess.run(['npx', 'markmap-cli', f'{ip_md}/{md_file_name}', '--no-open'], capture_output=True,
                                shell=True,
                                text=True)

        if result.returncode != 0:
            raise subprocess.CalledProcessError(result.returncode, result.args, output=result.stdout,
                                                stderr=result.stderr)

        # 尝试将生成的HTML文件移动到static/html文件夹
        os.replace(f'{ip_md}/{html_file_name}', f'{ip_html}/{html_file_name}')
        print(f"HTML file moved to: {ip_html}/{html_file_name}")

        # 返回转换后的HTML文件链接
        # return f'Markdown文件已保存. 点击预览: {request.url_for("get_html", filename=html_file_name)}'
        bd_url = f"http://localhost:16007/{ip_html}/{html_file_name}"
        # return f'Markdown文件已保存. 点击预览: {bd_url}'
        # Upload to COS
        etag = upload_cos('text1', tencent_region, tencent_secret_id, tencent_secret_key, tencent_bucket,
                          html_file_name,
                          current_directory / ip_html)
        if etag:
            audio_url2 = f"https://{tencent_bucket}.cos.{tencent_region}.myqcloud.com/{html_file_name}"
            return {
                "audio_url": audio_url2,
                "filename": html_file_name,
                "output_path": bd_url
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to upload audio to COS")
    except subprocess.CalledProcessError as e:
        # 如果转换过程中出现错误，返回错误信息
        return f"Error generating HTML file: {e.output}\n{e.stderr}"


app.include_router(router, prefix="/api")

# 打印所有路由
for route in app.routes:
    if isinstance(route, APIRoute):  # 检查是否为路由
        print(f"Path: {route.path}, Methods: {route.methods}")
    elif isinstance(route, Mount):  # 检查是否为挂载点
        print(f"Mount: {route.path} -> {route.name}")

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=16007)

# 测试
# curl --location 'http://10.20.0.65:15101/api/markdown2map/upload/' \
# --header 'Content-Type: text/plain' \
# --data-raw '{
#     "mindmap_generator": {
#         "content": "# Java学习
# ## 基础语法
# ### 数据类型
# - 基本数据类型
#  - byte
#  - short
#  - int
#  - long
#  - float
#  - double
#  - char
#  - boolean
# - 引用数据类型
#  - 类
#  - 接口
#  - 数组
# ### 运算符
# - 算术运算符
# - 关系运算符
# - 逻辑运算符
# - 位运算符
# - 赋值运算符
# - 其他运算符
# ### 控制语句
# - 条件语句
#  - if
#  - if-else
#  - switch
# - 循环语句
#  - for
#  - while
#  - do-while
# - 跳转语句
#  - break
#  - continue
#  - return
# ## 面向对象
# ### 类与对象
# - 类的定义
# - 对象的创建
# - 构造方法
# - 方法重载
# - this关键字
# ### 继承
# - 继承的概念
# - 方法重写
# - super关键字
# - final关键字
# ### 多态
# - 多态的概念
# - 向上转型
# - 向下转型
# ### 抽象类与接口
# - 抽象类
# - 接口
# - 接口与抽象类的区别
# ## 异常处理
# ### 异常分类
# - 检查型异常
# - 非检查型异常
# ### 异常处理机制
# - try-catch-finally
# - throw
# - throws
# ## 集合框架
# ### 集合接口
# - Collection
# - List
# - Set
# - Map
# ### 集合实现类
# - ArrayList
# - LinkedList
# - HashSet
# - TreeSet
# - HashMap
# - TreeMap
# ## 多线程
# ### 线程的创建
# - 继承Thread类
# - 实现Runnable接口
# ### 线程的生命周期
# - 新建
# - 就绪
# - 运行
# - 阻塞
# - 死亡
# ### 线程同步
# - synchronized关键字
# - 锁机制
# - 线程通信
# ## IO流
# ### 字节流
# - InputStream
# - OutputStream
# ### 字符流
# - Reader
# - Writer
# ### 文件操作
# - File类
# - 文件读写
# ## 网络编程
# ### Socket编程
# - TCP协议
# - UDP协议
# ### URL编程
# - URL类
# - URLConnection类
# ## 反射机制
# ### 反射的概念
# - Class类
# - 获取类的信息
# - 动态创建对象
# - 动态调用方法
# ## 泛型
# ### 泛型的概念
# - 泛型类
# - 泛型方法
# - 泛型接口
# ### 通配符
# - 上限通配符
# - 下限通配符
# ## 注解
# ### 内置注解
# - @Override
# - @Deprecated
# - @SuppressWarnings
# ### 自定义注解
# - 定义注解
# - 使用注解
# - 解析注解
# ## JDBC
# ### JDBC基础
# - JDBC API
# - 连接数据库
# - 执行SQL语句
# - 处理结果集
# ### 数据库连接池
# - DBCP
# - C3P0
# - Druid"
#     }
# }'
