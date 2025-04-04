import json

def main(json_str: str) -> str:
    """
    解析换脸 API 返回的 JSON 结果并生成 Markdown 格式图片链接
    :param json_str: JSON 字符串
    :return: 包含处理结果的字典
    """
    try:
        # 解析 JSON 数据
        data = json.loads(json_str)
        
        # 从 image_url 中提取文件名
        filename = data['image_url'].split('/')[-1]
        
        # 生成 Markdown 格式的图片链接
        markdown_result = f"![{filename}]({data['image_url']})"
        
        return {"result": markdown_result}
    except json.JSONDecodeError:
        return {"error": "JSON 解析错误"}
    except KeyError:
        return {"error": "JSON 格式不正确"}

if __name__ == "__main__":
    # 测试用例
    test_json = '''{
        "success": true,
        "image_url": "https://dify-1258720957.cos.ap-nanjing.myqcloud.com/faceswap_20250402130140_7242.jpg",
        "original_url": "https://cdn.beart.ai/datarm/faceswap/2025-03-19/output/za785w20p9rgc0cnykgbqqst8w_result_.png"
    }'''
    
    result = main(test_json)
    print(result)