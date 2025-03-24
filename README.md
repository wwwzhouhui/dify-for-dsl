## dify-for-dsl

本项目是基于dify开源项目实现的dsl工作流脚本合集。

分享一些好用的 Dify 工作流程，自用、学习两相宜，请使用 Dify 0.8.0 及以上版本导入使用。

## 使用说明

###   1 打开dify 

​     ![image-20241115095253729](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20241115095253729.png)

###   2  导入DSL

​      在创建应用-导入dsl

​     	![image-20241115095400354](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20241115095400354.png)

   ![image-20241115100248631](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20241115100248631.png)

### 3 创建

![image-20241115100334137](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20241115100334137.png)

## 4 完成

![image-20241115100449276](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20241115100449276.png)

### DSL列表清单

| DSL清单名称                              | 工作流显示                         | 用到技术                                                     | 更新时间                                                 | 作者                                       | 适用dify版本                               |
| ---------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ---------------------------------------- |
| FLUX绘画机器人.yml                       | ![image-20250323090547121](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323090547121.png) | 调用FLUX绘画模型、文本模型、http接口请求                     | 2024年11月16日          | wwwzhouhui           | 0.15.3               |
| 增值税发票提取小工具chatflow.yml         | ![image-20250323090514862](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323090514862.png) | 调用多模态模型、文本模型、文件提取器                         | 2024年11月16日              | wwwzhouhui               | 0.15.3                   |
| 发票提取小工具整合版-变量聚合器.yml      | ![image-20250323090446623](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323090446623.png) | 调用多模态模型、文本模型、文件提取器、IF流程判断             | 2024年11月16日  | wwwzhouhui   | 0.15.3       |
| 发票比对专家-新版客运火车票2.yml         | ![image-20250323090415346](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323090415346.png) | 调用多模态模型、文本模型                                     | 2024年11月16日                          | wwwzhouhui                           | 0.15.3                               |
| 抓取获取36氪热榜文章内容 .yml            | ![image-20250323090341369](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323090341369.png) | 调用文本模型、http接口请求、jina-ai爬取网页信息、迭代        | 2024年11月16日 | wwwzhouhui | 0.15.3  |
| 中国历史专家播客.yml                     | ![image-20250323090253917](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323090253917.png) | 调用文本模型、TEXT TO SPEECH工具组件使用                     | 2024年11月26日          | wwwzhouhui           | 0.15.3               |
| giteeKolors工作流.yaml                   | ![image-20250323090209808](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323090209808.png) | 自定义第三方接口服务封装文生图、使用gitee Serverless API 接口+腾讯云OSS存储 | 2024年12月18日 | wwwzhouhui | 0.15.3 |
| Fine-tune 语料构造器.yml                 | ![image-20250323085757187](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323085757187.png) | 调用文本模型                                                 | 2025年1月7日                                        | wwwzhouhui                                       | 0.15.3                                           |
| FLUX绘画机器人+多模态识别+语音播放.yml   | ![image-20250323085720140](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323085720140.png) | 文本生成模型、多模态模型、文生图模型、文生语音模型           | 2025年1月12日 | wwwzhouhui | 0.15.3     |
| 诗句封面+语音播报.yml                    | ![image-20250323085615684](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323085615684.png) | 文本生成模型、多模态模型、文生语音模型、http接口请求         | 2025年1月18日 | wwwzhouhui | 0.15.3   |
| ai绘画整合comfyui_bizair.yml             |              | http接口请求、comfui_bizair                                  | 2025年1月22日                        | wwwzhouhui                        | 0.15.3                            |
| YouTube博主和自媒体运营专家工作流.yml    | ![image-20250323085542505](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323085542505.png) | 文本生成模型                                                 | 2025年1月25日                                       | wwwzhouhui                                       | 0.15.3                                           |
| AI资讯每日新闻+语音播报工作流.yml        | ![image-20250323085517148](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323085517148.png) | 文本生成模型、crawl4ai                                       | 2025年2月3日                              | wwwzhouhui                             | 0.15.3                                 |
| 即梦AI绘画.yml                           | ![image-20250323085448044](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323085448044.png) | http接口请求、jimeng-free-api                                | 2025年2月4日                       | wwwzhouhui                      | 0.15.3                          |
| 自定义edgetts工作流.yml | ![image-20250323085251381](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323085251381.png) | http接口请求、edgetts                                        | 2025年2月10日                              | wwwzhouhui                              | 0.15.3                                  |
| 自带edgetts.yml | ![image-20250323085421648](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323085421648.png) | http接口请求、edgetts | 2025年2月10日 | wwwzhouhui | 0.15.3 |
| 飞书表格.yml                             | ![image-20250323085225985](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323085225985.png) | 文本生成模型、dify内置工具、飞书表格                         | 2025年2月12日               | wwwzhouhui               | 0.15.3                   |
| 儿童故事绘本.yml                         | ![image-20250323085154185](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323085154185.png) | 文本生成模型、http接口请求、jimeng-free-api、edgetts         | 2025年2月15日 | wwwzhouhui | 0.15.3   |
| 文生视频+tts语音播报.yml                 | ![image-20250323085121044](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323085121044.png) | 文本生成模型、http接口请求、edgetts、文本生成视频模型（接口调用） | 2025年2月20 日 | wwwzhouhui | 0.15.3 |
| ai agent智能体.yml                       | ![image-20250323085050777](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323085050777.png) | 文本生成模型、联网搜索、获取当前系统时间、AI绘画、语音播报等智能体功能组合。 | 2025年2月22 日 | wwwzhouhui | 0.15.3 |
| excel表格提取+echarts展示.yml            | ![image-20250323085005332](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323085005332.png) | 文本生成模型、文档提取功能、echarts                          | 2025年2月25 日               | wwwzhouhui                | 0.15.3                    |
| 学生成绩查询工作流（带数据库查询）.yml   | ![image-20250323084936593](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323084936593.png) | 文本生成模型、柱状图、数据库查询、http接口请求、table markdown | 2025年2月27 日 | wwwzhouhui | 0.15.3 |
| 知识库检索工作流.yml                     | ![image-20250323084900900](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323084900900.png) | 文本生成模型、知识库RAG、知识检索                            | 2025年3月3 日                  | wwwzhouhui                  | 0.15.3                      |
| AI绘画+飞书+企业微信整合.yml             | ![image-20250323084834734](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323084834734.png) | http接口请求、jimeng-free-api、飞书表格、企业微信            | 2025年3月7 日  | wwwzhouhui  | 0.15.3      |
| API文档生成代码.yml                      | ![image-20250323084807347](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323084807347.png) | jina-ai、文档提取功能、文本生成模型                          | 2025年3月9 日                | wwwzhouhui                | 0.15.3                  |
| 股票分析系统.yml                         | ![image-20250323084739019](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323084739019.png) | http接口请求、文本生成模型、Akshare股票数据接口、条件分支、变量聚合器 | 2025年3月11 日 | wwwzhouhui | 0.15.3 |
| 股票分析系统-Gordon修改版.yml             | ![image-20250323084643251](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323084643251.png) | 增加用户输入文本参数提取 http接口请求、文本生成模型、Akshare股票数据接口、条件分支、变量聚合器 | 2025年3月18 | Gordon | 0.15.3 |
| 大模型表格解析自动生成代码生成统计图.yml | ![image-20250323084556331](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323084556331.png) | http接口请求、文档提取功能、文本生成模型                     | 2025年3月13            | wwwzhouhui  | 0.15.3               |
| 儿童故事绘本文生视频语音合成版 .yml      | ![image-20250323084414060](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323084414060.png) | http接口请求、文本生成模型、文生图模型、edgetts、ffmpeg      | 2025年3月18 | wwwzhouhui | 0.15.3 |
| gemini-2.0-flash-exp-image-generation-文生图智能体.yml | ![image-20250323084256259](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323084256259.png) | 问题分类器、条件分支、自定义工具、变量赋值 | 2025年3月20日 | wwwzhouhui | 0.15.3 |
| 中英文翻译工作流-AI辅助生成.yml | ![image-20250323180346219](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323180346219.png) | llm大语言模型 | 2025年3月23日 | wwwzhouhui+trae | 0.15.3 |

### 部分视频链接地址

| 视频名称                                                 | 链接地址                                                     | 视频源                          |
| -------------------------------------------------------- | ------------------------------------------------------------ | ------------------------------- |
| dify案例分享-基于多模态模型的发票识别                    | https://www.bilibili.com/video/BV1H51xYbENj 、https://www.youtube.com/watch?v=rjMBui5IsOw、https://www.toutiao.com/video/7435521963365237287/ | B站、油管、今日头条             |
| dify案例分享-基于多模态模型的发票识别2                   | https://www.bilibili.com/video/BV1YgmzYxEhh、https://www.youtube.com/watch?v=ghehTQhdnss、https://www.toutiao.com/video/7433468877918437940/ | B站、油管、今日头条             |
| dify案例分享-基于多模态模型的发票比对                    | https://www.bilibili.com/video/BV1YgmzYxEhh、https://www.youtube.com/watch?v=Id41hLyxwlE、https://www.toutiao.com/video/7435521963365237287/ | B站、油管、今日头条             |
| dify案例分享-基于jina和http实现36氪新闻热榜文章          | https://www.bilibili.com/video/BV1YgmzYxEhh、https://www.youtube.com/watch?v=hrS-FTLtsGI | B站、油管                       |
| dify案例分享-文生图片OCR识别加语音播报，AI工作流一键搞定 | https://www.bilibili.com/video/BV13GcgezEVT、https://www.youtube.com/watch?v=Nq_5kDW0jO0&t=16s、https://www.toutiao.com/video/7458884426408182282/ | B站、油管、今日头条             |
| dify案例分享-古诗词海报生成加语音播报                    | https://www.bilibili.com/video/BV1fVwPeqEz9、https://www.youtube.com/watch?v=M6aVZX51cO0、https://www.toutiao.com/video/7461152220034171429/ | B站、油管、今日头条             |
| dify案例分享- 儿童故事绘本                               | https://www.bilibili.com/video/BV1WCAgeNEsw、https://www.youtube.com/watch?v=QV2MjL6fMi4、https://www.toutiao.com/video/7471874756129505792/ | B站、油管、今日头条、微信视频号 |

## 更新说明

2025年3月23 日-version 0.0.2.24 :中英文翻译工作流-AI辅助生成.yml

2025年3月20 日-version 0.0.2.23 :gemini-2.0-flash-exp-image-generation-文生图智能体.yml 提供第三方接口api源码 代码看 https://github.com/wwwzhouhui/dify-for-dsl/tree/main/dsl/google/gemini2/image-generation-server.py

2025年3月19 日-version 0.0.2.22 :股票分析系统-Gordon修改版.yml 

2025年3月18 日-version 0.0.2.21 :儿童故事绘本文生视频语音合成版 .yml 提供第三方接口api源码 代码看 https://github.com/wwwzhouhui/dify-for-dsl/tree/main/dsl/story/storymain.py

2025年3月13 日-version 0.0.2.20 :大模型表格解析自动生成代码生成统计图.yml 提供第三方接口api源码 代码看 https://github.com/wwwzhouhui/dify-for-dsl/tree/main/dsl/makehtml/makehtmlapi.py

2025年3月11 日-version 0.0.2.19 :新增加股票分析系统.yml 提供第三方接口api源码 代码看 https://github.com/wwwzhouhui/dify-for-dsl/tree/main/dsl/akshare/stock_analysis_api.py

2025年3月9 日-version 0.0.2.18 :新增加API文档生成代码.yml

2025年3月7 日-version 0.0.2.17 :新增加AI绘画+飞书+企业微信整合.yml

2025年3月3 日-version 0.0.2.16 :新增加知识库检索工作流.yml

2025年2月27 日-version 0.0.2.15:新增加学生成绩查询工作流（带数据库查询）.yml 提供第三方接口api源码 代码看 https://github.com/wwwzhouhui/dify-for-dsl/tree/main/dsl/db/student

2025年2月25 日-version 0.0.2.14:新增加excel表格提取+echarts展示.yml

2025年2月22 日-version 0.0.2.13:新增加ai agent智能体.yml

2025年2月20 日-version 0.0.2.12:新增加文生视频+tts语音播报.yml 提供第三方接口api源码，详细文档和代码看 https://github.com/wwwzhouhui/dify-for-dsl/tree/main/dsl/zhipu

2025年2月15日-version 0.0.2.11:新增加儿童故事绘本.yml 提供第三方接口api源码，详细文档和代码看 https://github.com/wwwzhouhui/dify-for-dsl/tree/main/dsl/jimeng

2025年2月12日-version 0.0.2.10:新增加飞书表格.yml

2025年2月10日-version 0.0.2.9:新增加自带edgetts.yml、自定义edgetts工作流.yml，详细文档和代码看 https://github.com/wwwzhouhui/dify-for-dsl/tree/main/dsl/edgetts

2025年2月4日-version 0.0.2.8:新增加即梦AI绘画.yml

2025年2月3日-version 0.0.2.7:新增加AI资讯每日新闻+语音播报工作流.yml 提供第三方接口api源码，详细文档和代码看 https://github.com/wwwzhouhui/dify-for-dsl/tree/main/dsl/crawl4ai

2025年1月25日-version 0.0.2.6:新增加YouTube博主和自媒体运营专家工作流.yml

2025年1月22日-version 0.0.2.5:新增加ai绘画整合comfyui_bizair.yml 提供第三方接口api源码，详细文档和代码看 https://github.com/wwwzhouhui/dify-for-dsl/tree/main/dsl/difyforsiliconflow/bizyair

2025年1月18日-version 0.0.2.4:新增加诗句封面+语音播报.yml

2025年1月12日-version 0.0.2.3:新增加FLUX绘画机器人+多模态识别+语音播放.yml 提供第三方接口api源码，详细文档和代码看https://github.com/wwwzhouhui/dify-for-dsl/tree/main/dsl/difyforsiliconflow/

2025年1月7日- version 0.0.2.2:新增加Fine-tune 语料构造器.yml

2024年12月18日- version 0.0.2.1: 新增加giteeKolors工作流.yaml 提供第三方接口api源码，详细文档和代码看https://github.com/wwwzhouhui/dify-for-dsl/tree/main/dsl/difyforgitee

2024年11月26日- version 0.0.2: 新增加中国历史专家播客 DSL文件

2024年11月16日- version 0.0.1: 新创建dsl文件（包含发票提取小工具整合版、抓取获取36氪热榜文章内容、发票提取小工具整合版-循环迭代等工作流)

## 技术文档地址（飞书）:

https://aqma351r01f.feishu.cn/wiki/HF5FwMDQkiHoCokvbQAcZLu3nAg?table=tbleOWb4WgXcxiHK&view=vewGwwbpzl

![image-20241115093319205](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20241115093319205.png)

## 🎉 致谢

感谢以下项目对本项目提供的有力支持：

1.[dify](https://github.com/langgenius/dify)

   Dify 是一个开源 LLM 应用程序开发平台。 Dify 的直观界面结合了 AI 工作流程、RAG 管道、代理功能、模型管理、可观察性功能等，让您快速从原型转向生产。

2.[jimeng-free-api](https://github.com/LLM-Red-Team/jimeng-free-api)
   Jimeng AI Free 服务 支持即梦超强图像生成能力（目前官方每日赠送 66 积分，可生成 66 次），零配置部署，多路 token 支持。 与 OpenAI 接口完全兼容

3.[akshare](https://github.com/akfamily/akshare) 

  开源财经数据接口库

4.[stock-scanner](https://github.com/lanzhihong6/stock-scanner)

   股票分析系统 (Stock Analysis System)

5.[story-flicks](https://github.com/alecm20/story-flicks)

  使用AI大模型，一键生成高清故事短视频

## 问题反馈

如有问题，请在GitHub Issue中提交，在提交问题之前，请先查阅以往的issue是否能解决你的问题

## 常见问题汇总



## 技术交流群

![image-20250324202253438](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250324202253438.png)

## Star History

![dify-for-dsl](https://api.star-history.com/svg?repos=wwwzhouhui/dify-for-dsl&type=Date)