# import json
# import requests
# from bs4 import BeautifulSoup
# from fastapi import FastAPI, Query
# from crawl4ai import AsyncWebCrawler
# from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
#
# app = FastAPI()
#
# # 获取新闻列表页面的所有新闻URL
# def get_news_urls():
#     url = "https://www.aibase.com/zh/news"
#     response = requests.get(url)
#     news_urls = []
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')
#         # 查找所有新闻链接
#         news_items = soup.find_all('a', href=True)
#         for item in news_items:
#             link = item['href']
#             # 过滤出符合新闻详情页的链接
#             if '/zh/news/' in link and len(link.split('/')) > 3:
#                 full_url = f"https://www.aibase.com{link}"
#                 news_urls.append(full_url)
#     else:
#         print(f"请求失败，状态码: {response.status_code}")
#     return news_urls
#
# # 提取单个新闻文章的数据
# async def extract_ai_news_article(url):
#     print(f"\n--- 提取新闻文章数据: {url} ---")
#     # 定义提取 schema
#     schema = {
#         "name": "AIbase News Article",
#         "baseSelector": "div.pb-32",  # 主容器的 CSS 选择器
#         "fields": [
#             {
#                 "name": "title",
#                 "selector": "h1",
#                 "type": "text",
#             },
#             {
#                 "name": "publication_date",
#                 "selector": "div.flex.flex-col > div.flex.flex-wrap > span:nth-child(6)",
#                 "type": "text",
#             },
#             {
#                 "name": "content",
#                 "selector": "div.post-content",
#                 "type": "text",
#             },
#         ],
#     }
#     # 创建提取策略
#     extraction_strategy = JsonCssExtractionStrategy(schema, verbose=True)
#     # 使用 AsyncWebCrawler 进行爬取
#     async with AsyncWebCrawler(verbose=True) as crawler:
#         result = await crawler.arun(
#             url=url,
#             extraction_strategy=extraction_strategy,
#             bypass_cache=True,  # 忽略缓存，确保获取最新内容
#         )
#         if not result.success:
#             print(f"页面爬取失败: {url}")
#             return None
#         # 解析提取的内容
#         extracted_data = json.loads(result.extracted_content)
#         print(f"成功提取新闻: {extracted_data[0]['title']}")
#         return extracted_data[0]
#
# # 主函数：获取所有新闻URL并逐一提取详细数据
# async def fetch_news(limit: int = 5):
#     # 获取所有新闻URL
#     news_urls = get_news_urls()
#     print(f"共找到 {len(news_urls)} 条新闻链接")
#
#     # 限制新闻数量
#     news_urls = news_urls[:limit]
#
#     news_data_list = []
#     # 循环处理每个新闻URL
#     for url in news_urls:
#         news_data = await extract_ai_news_article(url)
#         if news_data:
#             news_data_list.append(json.dumps(news_data, indent=2, ensure_ascii=False))
#
#     return news_data_list
#
# # FastAPI 接口
# @app.get("/news/")
# async def get_news(limit: int = Query(5, description="返回的新闻数量")):
#     news_data = await fetch_news(limit)
#     return {"news": news_data}
#
# # 运行 FastAPI 应用
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8086)


import json
import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI, Query
from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

app = FastAPI()

# 获取新闻列表页面的所有新闻URL
def get_news_urls():
    url = "https://www.aibase.com/zh/news"
    response = requests.get(url)
    news_urls = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # 查找所有新闻链接
        news_items = soup.find_all('a', href=True)
        for item in news_items:
            link = item['href']
            # 过滤出符合新闻详情页的链接
            if '/zh/news/' in link and len(link.split('/')) > 3:
                full_url = f"https://www.aibase.com{link}"
                news_urls.append(full_url)
    else:
        print(f"请求失败，状态码: {response.status_code}")
    return news_urls

# 提取单个新闻文章的数据
async def extract_ai_news_article(url):
    print(f"\n--- 提取新闻文章数据: {url} ---")
    # 定义提取 schema
    schema = {
        "name": "AIbase News Article",
        "baseSelector": "div.pb-32",  # 主容器的 CSS 选择器
        "fields": [
            {
                "name": "title",
                "selector": "h1",
                "type": "text",
            },
            {
                "name": "publication_date",
                "selector": "div.flex.flex-col > div.flex.flex-wrap > span:nth-child(6)",
                "type": "text",
            },
            {
                "name": "content",
                "selector": "div.post-content",
                "type": "text",
            },
        ],
    }
    # 创建提取策略
    extraction_strategy = JsonCssExtractionStrategy(schema, verbose=True)
    # 使用 AsyncWebCrawler 进行爬取
    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(
            url=url,
            extraction_strategy=extraction_strategy,
            bypass_cache=True,  # 忽略缓存，确保获取最新内容
        )
        if not result.success:
            print(f"页面爬取失败: {url}")
            return None
        # 解析提取的内容
        extracted_data = json.loads(result.extracted_content)
        print(f"成功提取新闻: {extracted_data[0]['title']}")
        return extracted_data[0]

# 主函数：获取所有新闻URL并逐一提取详细数据
async def fetch_news(limit: int = 5):
    # 获取所有新闻URL
    news_urls = get_news_urls()
    print(f"共找到 {len(news_urls)} 条新闻链接")
    # 限制新闻数量
    news_urls = news_urls[:limit]
    news_data_list = []
    newsdetail = ""
    # 循环处理每个新闻URL
    for index, url in enumerate(news_urls, start=1):
        news_data = await extract_ai_news_article(url)
        if news_data:
            # 添加到新闻数据列表
            news_data_list.append(news_data)
            # 拼接新闻详情字符串
            content = news_data.get("content", "无法提取内容")
            newsdetail += f"今天新闻第{index}条内容：{content}；\n"
    return news_data_list, newsdetail

# FastAPI 接口
@app.get("/news/")
async def get_news(limit: int = Query(5, description="返回的新闻数量")):
    news_data, newsdetail = await fetch_news(limit)
    return {"news": news_data, "newsdetail": newsdetail}

# 运行 FastAPI 应用
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8086)