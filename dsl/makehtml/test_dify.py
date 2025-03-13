import json
import re
import time
import requests

def main(json_html: str, apikey: str,apiurl: str,strtype: str) -> dict:
    try:
        # 去除输入字符串中的 ```html 和 ``` 标记
        html_content = re.sub(r'^```html\s*|\s*```$', '', json_html, flags=re.DOTALL).strip()
        
        # 生成时间戳，确保文件名唯一
        timestamp = int(time.time())
        filename = f"{strtype}_{timestamp}.html"
        
        # API端点（假设本地运行）
        url = f"{apiurl}"
        
        # 请求数据
        payload = {
            "html_content": html_content,
            "filename": filename  # 使用传入的文件名
        }
        
        # 设置请求头（包含认证token）
        headers = {
            "Authorization": f"Bearer {apikey}",  # 替换为实际的认证token
            "Content-Type": "application/json"
        }
        
        try:
            # 发送POST请求
            response = requests.post(url, json=payload, headers=headers)
            
            # 检查响应状态
            if response.status_code == 200:
                result = response.json()
                html_url = result.get("html_url", "")
                generated_filename = result.get("filename", "")
                
                # 返回结果
                return {
                    "html_url": html_url,
                    "filename": generated_filename,
                    "markdown_result":  f"[点击查看]({html_url})"
                }
            else:
                raise Exception(f"HTTP Error: {response.status_code}, Message: {response.text}")
        
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")
    
    except Exception as e:
        return {
            "error": f"Error: {str(e)}"
        }

# 示例调用
if __name__ == "__main__":
    # 示例输入HTML内容
    input_html = """```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>统计数据</title>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
    </style>
</head>
<body>
    <h1>统计数据</h1>
    <table>
        <thead>
            <tr>
                <th>年份</th>
                <th>AA地区使用率</th>
                <th>BB地区使用率</th>
                <th>CC地区使用率</th>
                <th>DD地区使用率</th>
                <th>其他使用率</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>2025</td>
                <td>59.69</td>
                <td>41.28</td>
                <td>9.78</td>
                <td>2.17</td>
                <td>6.48</td>
            </tr>
            <tr>
                <td>2026</td>
                <td>56.07</td>
                <td>38.78</td>
                <td>9.18</td>
                <td>2.04</td>
                <td>6.10</td>
            </tr>
            <tr>
                <td>2027</td>
                <td>52.46</td>
                <td>36.28</td>
                <td>8.59</td>
                <td>1.91</td>
                <td>5.71</td>
            </tr>
            <tr>
                <td>2028</td>
                <td>48.84</td>
                <td>33.78</td>
                <td>8.00</td>
                <td>1.78</td>
                <td>5.32</td>
            </tr>
            <tr>
                <td>2029</td>
                <td>45.22</td>
                <td>31.27</td>
                <td>7.41</td>
                <td>1.65</td>
                <td>4.93</td>
            </tr>
            <tr>
                <td>2030</td>
                <td>41.60</td>
                <td>28.76</td>
                <td>6.81</td>
                <td>1.51</td>
                <td>4.53</td>
            </tr>
        </tbody>
    </table>
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <div style="width:100%;margin-top:20px;">
        <canvas id="myChart"></canvas>
    </div>
    <script>
        const ctx = document.getElementById('myChart').getContext('2d');
        const chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['2025', '2026', '2027', '2028', '2029', '2030'],
                datasets: [{
                    label: 'AA地区使用率',
                    data: [59.69, 56.07, 52.46, 48.84, 45.22, 41.6],
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }, {
                    label: 'BB地区使用率',
                    data: [41.28, 38.78, 36.28, 33.78, 31.27, 28.76],
                    backgroundColor: 'rgba(153, 102, 255, 0.2)',
                    borderColor: 'rgba(153, 102, 255, 1)',
                    borderWidth: 1
                }, {
                    label: 'CC地区使用率',
                    data: [9.78, 9.18, 8.59, 8.00, 7.41, 6.81],
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                }, {
                    label: 'DD地区使用率',
                    data: [2.17, 2.04, 1.91, 1.78, 1.65, 1.51],
                    backgroundColor: 'rgba(255, 159, 64, 0.2)',
                    borderColor: 'rgba(255, 159, 64, 1)',
                    borderWidth: 1
                }, {
                    label: '其他使用率',
                    data: [6.48, 6.1, 5.71, 5.32, 4.93, 4.53],
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    </script>
</body>
</html>
```"""
    
    # 调用主函数并打印结果
    api_key = "sk-zhouhui111111"  # 替换为实际的API Key
    api_url = "http://192.168.1.2:8080/generate-html/"
    strtype="柱状图"
    result = main(input_html, api_key,api_url,strtype)
    print(json.dumps(result, ensure_ascii=False, indent=2))