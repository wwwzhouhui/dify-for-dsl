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

| DSL清单名称                         | 用到技术                                               |
| ----------------------------------- |----------------------------------------------------|
| FLUX绘画机器人.yml                  | 调用FLUX绘画模型、文本模型、http接口请求                           |
| 增值税发票提取小工具chatflow.yml    | 调用多模态模型、文本模型、文件提取器                                 |
| 发票提取小工具整合版-变量聚合器.yml | 调用多模态模型、文本模型、文件提取器、IF流程判断                          |
| 发票比对专家-新版客运火车票2.yml    | 调用多模态模型、文本模型                                       |
| 抓取获取36氪热榜文章内容 .yml       | 调用文本模型、http接口请求、jina-ai爬取网页信息、迭代                   |
| 中国历史专家播客.yml       | 调用文本模型、TEXT TO SPEECH工具组件使用                        |
| giteeKolors工作流.yaml       | 自定义第三方接口服务封装文生图、使用gitee Serverless API 接口+腾讯云OSS存储 |
| Fine-tune 语料构造器.yml      | 调用文本模型                                             |
| FLUX绘画机器人+多模态识别+语音播放.yml | 文本生成模型、多模态模型、文生图模型、文生语音模型                          |
| 诗句封面+语音播报.yml | 文本生成模型、多模态模型、文生语音模型、http接口请求                       |
| ai绘画整合comfyui_bizair.yml | http接口请求、comfui_bizair                             |
| YouTube博主和自媒体运营专家工作流.yml | 文本生成模型                                             |
| AI资讯每日新闻+语音播报工作流.yml | 文本生成模型、crawl4ai                                            |

### 部分视频链接地址

| 视频名称                                                 | 链接地址                                                     | 视频源              |
| -------------------------------------------------------- | ------------------------------------------------------------ | ------------------- |
| dify案例分享-基于多模态模型的发票识别                    | https://www.bilibili.com/video/BV1H51xYbENj 、https://www.youtube.com/watch?v=rjMBui5IsOw、https://www.toutiao.com/video/7435521963365237287/ | B站、油管、今日头条 |
| dify案例分享-基于多模态模型的发票识别2                   | https://www.bilibili.com/video/BV1YgmzYxEhh、https://www.youtube.com/watch?v=ghehTQhdnss、https://www.toutiao.com/video/7433468877918437940/ | B站、油管、今日头条 |
| dify案例分享-基于多模态模型的发票比对                    | https://www.bilibili.com/video/BV1YgmzYxEhh、https://www.youtube.com/watch?v=Id41hLyxwlE、https://www.toutiao.com/video/7435521963365237287/ | B站、油管、今日头条 |
| dify案例分享-基于jina和http实现36氪新闻热榜文章          | https://www.bilibili.com/video/BV1YgmzYxEhh、https://www.youtube.com/watch?v=hrS-FTLtsGI | B站、油管           |
| dify案例分享-文生图片OCR识别加语音播报，AI工作流一键搞定 | https://www.bilibili.com/video/BV13GcgezEVT、https://www.youtube.com/watch?v=Nq_5kDW0jO0&t=16s、https://www.toutiao.com/video/7458884426408182282/ | B站、油管、今日头条 |
| dify案例分享-古诗词海报生成加语音播报                    | https://www.bilibili.com/video/BV1fVwPeqEz9、https://www.youtube.com/watch?v=M6aVZX51cO0、https://www.toutiao.com/video/7461152220034171429/ | B站、油管、今日头条 |

## 更新说明

2024年11月16日- version 0.0.1: 新创建dsl文件（包含发票提取小工具整合版、抓取获取36氪热榜文章内容、发票提取小工具整合版-循环迭代等工作流)

2024年11月26日- version 0.0.2: 新增加中国历史专家播客 DSL文件

2024年12月18日- version 0.0.2.1: 新增加giteeKolors工作流.yaml 提供第三方接口api源码，详细文档和代码看https://github.com/wwwzhouhui/dify-for-dsl/tree/main/dsl/difyforgitee

2025年1月7日- version 0.0.2.2:新增加Fine-tune 语料构造器.yml

2025年1月12日-version 0.0.2.3:新增加FLUX绘画机器人+多模态识别+语音播放.yml 提供第三方接口api源码，详细文档和代码看https://github.com/wwwzhouhui/dify-for-dsl/tree/main/dsl/difyforsiliconflow/
2025年1月18日-version 0.0.2.4:新增加诗句封面+语音播报.yml

2025年1月22日-version 0.0.2.5:新增加ai绘画整合comfyui_bizair.yml 提供第三方接口api源码，详细文档和代码看 https://github.com/wwwzhouhui/dify-for-dsl/tree/main/dsl/difyforsiliconflow/bizyair

2025年1月25日-version 0.0.2.6:新增加YouTube博主和自媒体运营专家工作流.yml

2025年2月3日-version 0.0.2.7:新增加AI资讯每日新闻+语音播报工作流.yml 提供第三方接口api源码，详细文档和代码看 https://github.com/wwwzhouhui/dify-for-dsl/tree/main/dsl/crawl4ai

## 技术文档地址（飞书）:

https://aqma351r01f.feishu.cn/wiki/HF5FwMDQkiHoCokvbQAcZLu3nAg?table=tbleOWb4WgXcxiHK&view=vewGwwbpzl

![image-20241115093319205](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20241115093319205.png)

## 🎉 致谢

感谢以下项目对本项目提供的有力支持：

1.[dify](https://github.com/langgenius/dify)

   Dify 是一个开源 LLM 应用程序开发平台。 Dify 的直观界面结合了 AI 工作流程、RAG 管道、代理功能、模型管理、可观察性功能等，让您快速从原型转向生产。

## 问题反馈

如有问题，请在GitHub Issue中提交，在提交问题之前，请先查阅以往的issue是否能解决你的问题

## 常见问题汇总



## 技术交流群

![img](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/%E5%BE%AE%E4%BF%A1%E5%9B%BE%E7%89%87_20250203152237.jpg)

## Star History

![dify-for-dsl](https://api.star-history.com/svg?repos=wwwzhouhui/dify-for-dsl&type=Date)