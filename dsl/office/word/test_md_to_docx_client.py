import requests
import json

def test_md_to_docx_conversion():
    # 服务器地址
    server_url = "http://localhost:8089/office/word/convert"
    
    # 测试用的 Markdown 内容
    markdown_content = """# 测试标题
## 二级标题
这是一段测试文本。

- 列表项1
- 列表项2

**粗体文本**
*斜体文本*
"""
    
    try:
        # 发送 POST 请求
        response = requests.post(
            server_url,
            data=markdown_content.encode('utf-8'),
            headers={'Content-Type': 'text/plain'}
        )
        
        # 检查响应状态
        if response.status_code == 200:
            result = response.json()
            print("转换成功！")
            print("下载链接:", result['download_url'])
        else:
            print(f"转换失败，状态码: {response.status_code}")
            print("错误信息:", response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"请求出错: {e}")

if __name__ == "__main__":
    test_md_to_docx_conversion()