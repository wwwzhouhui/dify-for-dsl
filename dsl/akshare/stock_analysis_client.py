import requests
import json
import pandas as pd
from datetime import datetime
from prettytable import PrettyTable

def call_stock_analysis_api(stock_code, market_type='A', start_date=None, end_date=None, api_url="http://localhost:8085", auth_token=None):
    """
    调用股票分析API接口
    
    参数:
        stock_code (str): 股票代码
        market_type (str): 市场类型，默认为'A'
        start_date (str): 开始日期，格式为'YYYYMMDD'，默认为None
        end_date (str): 结束日期，格式为'YYYYMMDD'，默认为None
        api_url (str): API服务器地址，默认为"http://localhost:8085"
        auth_token (str): 鉴权Token，默认为None
        
    返回:
        dict: API返回的结果
    """
    # 构建请求URL
    url = f"{api_url}/analyze-stock/"
    
    # 构建请求数据
    data = {
        "stock_code": stock_code,
        "market_type": market_type
    }
    
    if start_date:
        data["start_date"] = start_date
    if end_date:
        data["end_date"] = end_date
    
    # 构建请求头
    headers = {
        "Content-Type": "application/json"
    }
    
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"
    else:
        print("警告: 未提供鉴权Token，可能会导致请求失败")
    
    try:
        # 发送POST请求
        response = requests.post(url, json=data, headers=headers)
        
        # 检查响应状态
        if response.status_code == 200:
            return response.json()
        else:
            print(f"请求失败，状态码: {response.status_code}")
            print(f"错误信息: {response.text}")
            return None
    except Exception as e:
        print(f"请求异常: {str(e)}")
        return None

def display_technical_summary(technical_summary):
    """显示技术指标概要"""
    print("\n=== 技术指标概要 ===")
    print(f"趋势: {'上升' if technical_summary['trend'] == 'upward' else '下降'}")
    print(f"波动率: {technical_summary['volatility']}")
    print(f"成交量趋势: {'增加' if technical_summary['volume_trend'] == 'increasing' else '减少'}")
    print(f"RSI指标: {technical_summary['rsi_level']:.2f}")

def display_recent_data(recent_data):
    """显示近期交易数据"""
    print("\n=== 近14日交易数据 ===")
    
    # 创建表格
    table = PrettyTable()
    
    # 设置表头
    table.field_names = ["日期", "开盘", "最高", "最低", "收盘", "成交量", "RSI", "MACD"]
    
    # 添加数据行
    for day in recent_data:
        date_str = day['date'].split('T')[0] if 'T' in day['date'] else day['date']
        table.add_row([
            date_str,
            f"{day['open']:.2f}",
            f"{day['high']:.2f}",
            f"{day['low']:.2f}",
            f"{day['close']:.2f}",
            f"{day['volume']}",
            f"{day['RSI']:.2f}" if 'RSI' in day and day['RSI'] is not None else "N/A",
            f"{day['MACD']:.4f}" if 'MACD' in day and day['MACD'] is not None else "N/A"
        ])
    
    # 打印表格
    print(table)

def display_report(report):
    """显示分析报告"""
    print("\n=== 股票分析报告 ===")
    print(f"股票代码: {report['stock_code']} (市场: {report['market_type']})")
    print(f"分析日期: {report['analysis_date']}")
    print(f"当前价格: {report['price']:.2f}")
    print(f"价格变动: {report['price_change']:.2f}%")
    print(f"MA趋势: {report['ma_trend']}")
    print(f"RSI指标: {report['rsi']:.2f}" if report['rsi'] is not None else "RSI指标: N/A")
    print(f"MACD信号: {report['macd_signal']}")
    print(f"成交量状态: {report['volume_status']}")
    print(f"评分: {report['score']}")
    print(f"建议: {report['recommendation']}")

def save_to_file(result, stock_code):
    """保存结果到文件"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"f:\\work\\code\\2024pythontest\\akshare\\analysis_{stock_code}_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    
    print(f"\n分析结果已保存到: {filename}")

def main():
    """主函数"""
    print("=== 股票分析客户端 ===")
    
    # 获取用户输入
    # stock_code = input("请输入股票代码: ")
    # market_type = input("请输入市场类型 [A/HK/US/ETF/LOF] (默认A): ") or 'A'
    # start_date = input("请输入开始日期 (YYYYMMDD) (可选): ")
    # end_date = input("请输入结束日期 (YYYYMMDD) (可选): ")
    # auth_token = input("请输入鉴权Token: ")
    stock_code = "512670"
    market_type = "ETF"
    start_date = ""
    end_date = ""
    auth_token = "sk-zhouhui1122444"  # 替换为实际的Token
    
    # 调用API
    print(f"\n正在分析股票 {stock_code}...")
    result = call_stock_analysis_api(stock_code, market_type, start_date, end_date, auth_token=auth_token)
    
    if result:
        # 显示技术指标概要
        display_technical_summary(result["technical_summary"])
        
        # 显示近期交易数据
        display_recent_data(result["recent_data"])
        
        # 显示分析报告
        display_report(result["report"])
        
        # 保存结果到文件
        save_to_file(result, stock_code)
    else:
        print("获取股票分析数据失败")

if __name__ == "__main__":
    main()