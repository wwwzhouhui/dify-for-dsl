import requests
import json
import time
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("VideoGenerationTest")

def test_generate_video():
    """测试即梦视频生成API客户端"""
    
    # 服务器地址
    server_url = "http://localhost:8088/jimeng/generate_video/"
    
    # 添加认证头
    headers = {
        "Authorization": "Bearer sk-zhouhui111111",  # 替换为实际的认证token
        "Content-Type": "application/json"
    }
    
    # 请求参数
    payload = {
        "prompt": "小刺猬在吃西瓜",  # 视频描述提示词
        "aspect_ratio": "16:9",                # 视频宽高比，可选 "16:9", "9:16", "1:1" 等
        "duration_ms": 5000,                   # 视频时长(毫秒)
        "fps": 24                              # 帧率
    }
    
    logger.info(f"开始测试视频生成，提示词: {payload['prompt']}")
    logger.info(f"参数: 宽高比={payload['aspect_ratio']}, 时长={payload['duration_ms']}ms, 帧率={payload['fps']}fps")
    
    try:
        # 发送POST请求时添加headers
        start_time = time.time()
        logger.info("发送请求到视频生成API...")
        
        response = requests.post(server_url, json=payload, headers=headers)
        
        # 检查响应状态
        if response.status_code != 200:
            logger.error(f"请求失败，状态码: {response.status_code}")
            # 修改这里，使用 repr() 来安全地输出错误信息，避免格式化问题
            logger.error(f"错误信息: {repr(response.text)}")
            return
        
        # 解析响应
        result = response.json()
        elapsed_time = time.time() - start_time
        
        logger.info(f"视频生成成功! 总耗时: {elapsed_time:.2f}秒")
        logger.info(f"任务ID: {result.get('task_id')}")
        logger.info(f"视频URL: {result.get('video_url')}")
        
        # 保存结果到文件
        with open("video_generation_result.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        logger.info("结果已保存到 video_generation_result.json")
        
        return result
        
    except Exception as e:
        logger.error(f"测试过程中发生错误: {str(e)}")
        return None

def test_multiple_videos():
    """测试生成多个不同参数的视频"""
    
    test_cases = [
        {
            "prompt": "卡通风格的小猫在草地上奔跑",
            "aspect_ratio": "16:9",
            "duration_ms": 5000,
            "fps": 24
        },
        {
            "prompt": "宇航员在太空中漂浮",
            "aspect_ratio": "1:1",
            "duration_ms": 8000,
            "fps": 30
        },
        {
            "prompt": "海浪拍打沙滩，夕阳西下",
            "aspect_ratio": "9:16",
            "duration_ms": 6000,
            "fps": 24
        }
    ]
    
    results = []
    for i, test_case in enumerate(test_cases):
        logger.info(f"\n===== 测试用例 {i+1}/{len(test_cases)} =====")
        result = test_single_video(test_case)
        if result:
            results.append(result)
        # 等待一段时间再发送下一个请求，避免服务器压力过大
        if i < len(test_cases) - 1:
            time.sleep(5)
    
    return results

def test_single_video(params):
    """测试单个视频生成"""
    server_url = "http://localhost:8088/jimeng/generate_video/"
     # 设置请求头（包含认证token）
    headers = {
        "Authorization": "Bearer sk-zhouhui1122444",  # 替换为实际的认证token
        "Content-Type": "application/json"
    }
    try:
        logger.info(f"生成视频: {params['prompt']}")
        response = requests.post(server_url, json=params, headers=headers)
        
        if response.status_code != 200:
            logger.error(f"请求失败: {response.status_code} - {response.text}")
            return None
            
        result = response.json()
        logger.info(f"视频URL: {result.get('video_url')}")
        return result
        
    except Exception as e:
        logger.error(f"请求出错: {str(e)}")
        return None

if __name__ == "__main__":
    logger.info("===== 开始测试即梦视频生成API =====")
    
    # 测试单个视频生成
    result = test_generate_video()
    
    # 如果需要测试多个视频，可以取消下面的注释
    # results = test_multiple_videos()
    
    logger.info("===== 测试完成 =====")