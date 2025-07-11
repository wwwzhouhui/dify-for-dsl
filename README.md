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

| 用 Dify 一键搭建数学公式识别工作流，支持laTex | ![img](https://dify-1305874767.cos.ap-nanjing.myqcloud.com/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20250711082331.png) | 开始、Agent、LLM大语言模型、代码执行、直接回复 | 2025年7月11日 | wwwzhouhui | 1.4.3 |
| 用 Dify 一键搭建中药科普工作流，文字 + 图片 + 视频全搞定 | ![img](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/QQ_1751471812082.png) | 开始节点、AGENT、直接回复、自定义MCP-Server | 2025年7月3日 | wwwzhouhui | 1.4.3 |
| 用 Dify 一键生成 长安的荔枝金句 HTML 页面，三步搞定！.yml | ![image-20250626211532393](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250626211532393.png) | 开始、Agent、LLM大语言模型、代码执行、直接回复 | 2025年6月27日 | wwwzhouhui | 1.4.3 |
| Dify 轻松实现 PPT 到 SVG 海报的华丽变身_合合版.yml | ![image-20250622174547135](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250622174547135.png) | 开始、合合通用文档解析、LLM大语言模型、直接回复 | 2025年6月22日 | wwwzhouhui | 1.4.3 |
| Dify 轻松实现 PPT 到 SVG 海报的华丽变身-MinerU版.yml | ![image-20250622174454713](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250622174454713.png) | 开始、MinerU、LLM大语言模型、直接回复 | 2025年6月22日 | wwwzhouhui | 1.4.3 |
| 中药科普知识工作流.yml | ![image-20250617225402249](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250617225402249.png.png) | 开始节点、AGENT、直接回复、自定义MCP-Server | 2025年6月18日 | 醒醒、wwwzhouhui | 1.4.0 |
| 豆包文本生成图、文生视频+小支付功能 | ![image-20250614151812492](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250614151812492.png.png) | 开始节点、条件分支、AGENT、小支付、直接回复 | 2025年6月14日 | wwwzhouhui | 1.4.0 |
| N8N+Dify 打造新闻定时推送流.yml | ![image-20250610152751289](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250610152751289.png) | 条件分支、rookie_rss(第三方工具)、变量聚合器、代码执行、llm文本模型、获取时间（第三方工具）、163SMTP邮件发送 | 2025年6月10日 | wwwzhouhui | 1.4.0 |
| Dify+RSS 聚合 8 大平台实时热点，新闻获取效率飙升 300%.yml | ![image-20250609171838135](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250609171838135.png.png) | 条件分支、rookie_rss(第三方工具)、变量聚合器、代码执行、llm文本模型、获取时间（第三方工具） | 2025年6月9日 | wwwzhouhui | 1.4.0 |
| 批量识别PDF电子发票信息生成excle表格.yml | ![image-20250605222058323](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250605222058323.png.png) | 迭代、pdf转png转换器（第三方工具）、多模态大语言模型、代码执行、飞书表格 | 2025年6月6日 | wwwzhouhui | 1.4.0 |
| 豆包文本生成图像、文本生成视频以及图像转视频.yml | ![image-20250603140834839](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250603140834839.png.png) | 条件分支、llm大语言模型、Doubao Image and Video Generator 的插件 | 2025年6月3日 | wwwzhouhui | 1.4.0 |
| 衡水体英语作文评分工作流.yml | ![image-20250601154019415](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250601154019415.png.png) | 模板转换、条件分支、pdf转png转换器（第三方工具）、基于多模态llm大语言模型、变量聚合器、基于文本大语言模型 | 2025年6月2日 | wwwzhouhui | 1.4.0 |
| 中小学数学错题本-生成同类型题.yml | ![image-20250529235930374](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250529235930374.png) | 问题分类器、模板转换、条件分支、代码处理、SQL Execute、变量赋值、迭代、获取当前时间、Markdown转PDF文件、LLM大语言模型等 | 2025年5月30日 | wwwzhouhui | 1.4.0 |
| 中小学数学错题本-错题收集篇.yml | ![image-20250528153730875](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250528153730875.png) | 开始节点、模板转换、条件分支、pdf转png转换器（第三方工具）、基于多模态llm大语言模型、变量聚合器、代码执行、迭代、SQL Execute（第三方工具） | 2025年5月28日 | wwwzhouhui | 1.4.0 |
| 0 代码实现企业画像！16 种图表，解锁数据查询新姿势.yml | ![image-20250526175553744](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250526175553744.png.png) | 问题分类器、mcp-sse、mcp-server-chart、MCP Agent 策略工具、企业信息查询的MCP-Server | 2025年5月27日 | wwwzhouhui | 1.4.0 |
| 英语单词口语练习.yml | ![image-20250524093955804](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250524093955804.png.png) | llm大语言模型、参数提取器、Markdown转HTML文件 | 2025年5月24日 | wwwzhouhui | 1.4.0 |
| 海报封面生成工作流-Wanx 文生图.yml | ![image-20250522225213393](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250522225213393.png) | 阿里云百炼MCP Agent（Wanx 文生图）、条件分支、变量聚合器、模版转换、代码执行 | 2025年5月23日 | wwwzhouhui | 1.4.0 |
| 12306mcp火车票信息查询-chatflow.yml | ![image-20250520164540255](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250520164540255.png) | AGNET策略工具、12306MCP、mcphub | 2025年5月21日 | wwwzhouhui | 1.4.0 |
| 3步实现音视频转文字会议纪要从此无忧.yml | ![image-20250520103737363](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250520103737363.png) | ffmpeg、Speech To Text、ASR模型、LLM大语言模型 | 2025年5月20日 | wwwzhouhui | 1.4.0 |
| 基于上市公司财报分析结果html分析报告（整合MinerU+edgeone-pages-mcp）.yml | ![image-20250513221853568](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250513221853568.png) | mineru插件、LLM大语言模型、参数提取器、代码处理生成 | 2025年5月13日 | wwwzhouhui | 1.13 |
| 多模态图像编辑(HiDream-E1-Full)chatflow.yml | ![image-20250510164614722](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250510164614722.png.png) | 图片转base64、条件分支、代码转换、变量赋值、2个自定义工具 | 2025年5月10日 | wwwzhouhui | 1.13 |
| 图片生成html,网页小游戏（1panel mcpsse）.yml | ![image-20250503124212089](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250503124212089.png.png) | 1panelmcp、问题分类器、AGNET策略工具、edgeone-pages-mcp-server | 2025年5月3日 | wwwzhouhui | 1.13 |
| 通用合同审查助手.yml | ![image-20250429145121654](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250429145121654.png) | qwen3最新模型、文档提取器、markdown转换器 | 2025年4月29日 | 堕落奶酪、wwwzhouhui | 1.3.1 |
| 魔搭社区MCP-Server.yml | ![image-20250426162356017](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250426162356017.png) | 问题分类器、AGNET策略工具、魔搭社区MCP-server(高德MCP 、好吃的、Tavily、LeetCode(力扣)) | 2025年4月26日 | wwwzhouhui | 1.1.3 |
| 基于表结构的agent text2sql.yml | ![image-20250424115715194](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250424115715194.png) | AGNET | 2025年4月24日 | wwwzhouhui | 1.1.3 |
| 基于知识库+agent实现text2sqlchatflow工作流.yml | ![image-20250424115545595](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250424115545595.png) | 知识检索、AGNET策略工具、database插件 | 2025年4月24日 | wwwzhouhui | 1.1.3 |
| 软件开发类合同审查chatflow.yml | ![image-20250423120822891](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250423120822891.png) | llm、文档提取器、markdown转换器、企业微信 | 2025年4月23日 | wwwzhouhui | 1.1.3 |
| 提示词生成器chatflow.yml | ![image-20250419131519060](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250419131519060.png) | llm、条件判断器 | 2025年4月19日 | wwwzhouhui | 1.1.3 |
| 儿童故事绘本-PPT chatflow.yml | ![image-20250414220809839](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250414220809839.png) | agent、markdown转换器 | 2025年4月14日 | wwwzhouhui | 1.1.3 |
| 儿童故事绘本-PPT Agent.yml | ![image-20250414220712520](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250414220712520.png) | llm、markdown转PPTX 转换器 | 2025年4月14日 | wwwzhouhui | 1.1.3 |
| 学生成绩查询Chatflow支持text2sql.yml | ![image-20250409155549478](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250409155549478.png) | 时间工具、ECharts图表生成、database、llm | 2025年4月9日 | wwwzhouhui | 1.1.3 |
| dify-mcp-sse+Zapier MCP新闻检索邮件发送.yml | ![image-20250407220011943](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250407220011943.png) | mcp-sse、Zapier MCP | 2025年4月7日 | wwwzhouhui | 1.1.3 |
| 物头像风格迁移工作流.yml | ![image-20250404205912304](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250404205912304.png) | http接口请求、逆向人物头像风格迁移fastapi接口实现 | 2025年4月4日 | wwwzhouhui | 1.1.3 |
| 免费即梦文生视频.yml | ![image-20250401145310390](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250401145310390.png) | 文本模型、http接口请求、 逆向即梦文生视频fastapi接口实现 | 2025年4月1日 | wwwzhouhui | 0.15.3 |
| 周易大师.yml | ![image-20250326223949931](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/%E5%91%A8%E6%98%93%E5%A4%A7%E5%B8%88..jpg) | 周易大师 | 2025年3月26日 | gordon | 0.0.1 |
| 大学生计算机专业简历美化工作流.yml | ![image-20250326223949931](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250326223949931.png) | 模版转换、文本模型、多模态模型、文档提取器 | 2025年3月26日 | wwwzhouhui | 0.15.3 |
| 文生Word_Http_Post.yml 、文生Word_Agent.yml | ![image-20250326223908260](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250326223908260.png) | ai agent、自定义workflow、http请求 | 2025年3月25日 | wwwzhouhui+jenal | 0.15.3 or 1.1.2 |
| 中英文翻译工作流-AI辅助生成.yml | ![image-20250323180346219](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323180346219.png) | llm大语言模型 | 2025年3月23日 | wwwzhouhui+trae | 0.15.3 |
| gemini-2.0-flash-exp-image-generation-文生图智能体.yml | ![image-20250323084256259](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323084256259.png) | 问题分类器、条件分支、自定义工具、变量赋值 | 2025年3月20日 | wwwzhouhui | 0.15.3 |
| 儿童故事绘本文生视频语音合成版 .yml | ![image-20250323084414060](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323084414060.png) | http接口请求、文本生成模型、文生图模型、edgetts、ffmpeg | 2025年3月18 | wwwzhouhui | 0.15.3 |
| 大模型表格解析自动生成代码生成统计图.yml | ![image-20250323084556331](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323084556331.png) | http接口请求、文档提取功能、文本生成模型 | 2025年3月13 | wwwzhouhui | 0.15.3 |
| 股票分析系统-Gordon修改版.yml | ![image-20250323084643251](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323084643251.png) | 增加用户输入文本参数提取 http接口请求、文本生成模型、Akshare股票数据接口、条件分支、变量聚合器 | 2025年3月18 | Gordon | 0.15.3 |
| 股票分析系统.yml | ![image-20250323084739019](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323084739019.png) | http接口请求、文本生成模型、Akshare股票数据接口、条件分支、变量聚合器 | 2025年3月11 日 | wwwzhouhui | 0.15.3 |
| API文档生成代码.yml | ![image-20250323084807347](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323084807347.png) | jina-ai、文档提取功能、文本生成模型 | 2025年3月9 日 | wwwzhouhui | 0.15.3 |
| AI绘画+飞书+企业微信整合.yml | ![image-20250323084834734](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323084834734.png) | http接口请求、jimeng-free-api、飞书表格、企业微信 | 2025年3月7 日 | wwwzhouhui | 0.15.3 |
| 知识库检索工作流.yml | ![image-20250323084900900](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323084900900.png) | 文本生成模型、知识库RAG、知识检索 | 2025年3月3 日 | wwwzhouhui | 0.15.3 |
| 生成绩查询工作流（带数据库查询）.yml | ![image-20250323084936593](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323084936593.png) | 文本生成模型、柱状图、数据库查询、http接口请求、table markdown | 2025年2月27 日 | wwwzhouhui | 0.15.3 |
| excel表格提取+echarts展示.yml | ![image-20250323085005332](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323085005332.png) | 文本生成模型、文档提取功能、echarts | 2025年2月25 日 | wwwzhouhui | 0.15.3 |
| ai agent智能体.yml | ![image-20250323085050777](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323085050777.png) | 文本生成模型、联网搜索、获取当前系统时间、AI绘画、语音播报等智能体功能组合。 | 2025年2月22 日 | wwwzhouhui | 0.15.3 |
| 文生视频+tts语音播报.yml | ![image-20250323085121044](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323085121044.png) | 文本生成模型、http接口请求、edgetts、文本生成视频模型（接口调用） | 2025年2月20 日 | wwwzhouhui | 0.15.3 |
| 儿童故事绘本.yml | ![image-20250323085154185](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323085154185.png) | 文本生成模型、http接口请求、jimeng-free-api、edgetts | 2025年2月15日 | wwwzhouhui | 0.15.3 |
| 飞书表格.yml | ![image-20250323085225985](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323085225985.png) | 文本生成模型、dify内置工具、飞书表格 | 2025年2月12日 | wwwzhouhui | 0.15.3 |
| 自带edgetts.yml | ![image-20250323085421648](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323085421648.png) | http接口请求、edgetts | 2025年2月10日 | wwwzhouhui | 0.15.3 |
| 自定义edgetts工作流.yml | ![image-20250323085251381](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323085251381.png) | http接口请求、edgetts | 2025年2月10日 | wwwzhouhui | 0.15.3 |
| 即梦AI绘画.yml | ![image-20250323085448044](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323085448044.png) | http接口请求、jimeng-free-api | 2025年2月4日 | wwwzhouhui | 0.15.3 |
| AI资讯每日新闻+语音播报工作流.yml | ![image-20250323085517148](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323085517148.png) | 文本生成模型、crawl4ai | 2025年2月3日 | wwwzhouhui | 0.15.3 |
| YouTube博主和自媒体运营专家工作流.yml | ![image-20250323085542505](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323085542505.png) | 文本生成模型 | 2025年1月25日 | wwwzhouhui | 0.15.3 |
| ai绘画整合comfyui_bizair.yml |  | http接口请求、comfui_bizair | 2025年1月22日 | wwwzhouhui | 0.15.3 |
| 诗句封面+语音播报.yml | ![image-20250323085615684](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323085615684.png) | 文本生成模型、多模态模型、文生语音模型、http接口请求 | 2025年1月18日 | wwwzhouhui | 0.15.3 |
| FLUX绘画机器人+多模态识别+语音播放.yml | ![image-20250323085720140](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323085720140.png) | 文本生成模型、多模态模型、文生图模型、文生语音模型 | 2025年1月12日 | wwwzhouhui | 0.15.3 |
| Fine-tune 语料构造器.yml | ![image-20250323085757187](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323085757187.png) | 调用文本模型 | 2025年1月7日 | wwwzhouhui | 0.15.3 |
| giteeKolors工作流.yaml | ![image-20250323090209808](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323090209808.png) | 自定义第三方接口服务封装文生图、使用gitee Serverless API 接口+腾讯云OSS存储 | 2024年12月18日 | wwwzhouhui | 0.15.3 |
| 中国历史专家播客.yml | ![image-20250323090253917](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323090253917.png) | 调用文本模型、TEXT TO SPEECH工具组件使用 | 2024年11月26日 | wwwzhouhui | 0.15.3 |
| 抓取获取36氪热榜文章内容 .yml | ![image-20250323090341369](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323090341369.png) | 调用文本模型、http接口请求、jina-ai爬取网页信息、迭代 | 2024年11月16日 | wwwzhouhui | 0.15.3 |
| 发票比对专家-新版客运火车票2.yml | ![image-20250323090415346](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323090415346.png) | 调用多模态模型、文本模型 | 2024年11月16日 | wwwzhouhui | 0.15.3 |
| 发票提取小工具整合版-变量聚合器.yml | ![image-20250323090446623](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323090446623.png) | 调用多模态模型、文本模型、文件提取器、IF流程判断 | 2024年11月16日 | wwwzhouhui | 0.15.3 |
| 增值税发票提取小工具chatflow.yml | ![image-20250323090514862](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323090514862.png) | 调用多模态模型、文本模型、文件提取器 | 2024年11月16日 | wwwzhouhui | 0.15.3 |
| FLUX绘画机器人.yml                       | ![image-20250323090547121](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250323090547121.png) | 调用FLUX绘画模型、文本模型、http接口请求                     | 2024年11月16日          | wwwzhouhui           | 0.15.3               |

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

###  mcp-server

| mcp-server名称  | 界面显示                                                     | 用到技术    | 更新时间     | 作者       | mcp client    |
| --------------- | ------------------------------------------------------------ | ----------- | ------------ | ---------- | ------------- |
| 即梦ai 文生视频 | ![image-20250402133331455](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250402133331455.png) | fastapi-mcp | 2025年4月2日 | wwwzhouhui | Cherry Studio |
|                 |                                                              |             |              |            |               |
|                 |                                                              |             |              |            |               |



## 更新说明
2025年7月11日-version 0.0.3.32：增加数学公式识别工作流，输入pdf或图片，识别出里面的数学公式，并且输出支持latex格式的可编辑word，需要安装pandoc（ https://github.com/jgm/pandoc/releases/tag/3.7.0.2 ）和laTex（ https://miktex.org/download ） 环境。

https://github.com/wwwzhouhui/dify-for-dsl/tree/main/dsl/69-数学公式识别工作流.yml
2025年7月3日-version 0.0.3.31：增加用 Dify 一键搭建中药科普工作流，文字 + 图片 + 视频全搞定.使用到第三方MCP_Server代码地址

https://github.com/zhouqyu666/zhongyao-mcp-server

2025年6月27日-version 0.0.3.30：增加用 Dify 一键生成 长安的荔枝金句 HTML 页面，三步搞定！.yml后端代码复用之前的代码 https://github.com/wwwzhouhui/dify-for-dsl/tree/main/dsl/makehtml/makehtmlapi.py

2025年6月22日-version 0.0.3.29：增加Dify 轻松实现 PPT 到 SVG 海报的华丽变身_合合版.yml,Dify 轻松实现 PPT 到 SVG 海报的华丽变身-MinerU版.yml

2025年6月18日-version 0.0.3.28：增加中药科普知识工作流.yml 后端代码https://github.com/wwwzhouhui/dify-for-dsl/tree/main/mcp/FastMCP/zhongyao-mcp-server.py

2025年6月14日-version 0.0.3.27：增加豆包文本生成图、文生视频+小支付功能.yml 后端代码https://github.com/wwwzhouhui/dify-for-dsl/tree/main/mcp/FastMCP/doubao_mcp_ai_server2.py

2025年6月10日-version 0.0.3.26：增加N8N+Dify 打造新闻定时推送流.yml

2025年6月9日-version 0.0.3.25：增加Dify+RSS 聚合 8 大平台实时热点，新闻获取效率飙升 300%.yml

2025年6月6日-version 0.0.3.24：增加批量识别PDF电子发票信息生成excle表格.yml

2025年6月3日-version 0.0.3.23：增加豆包文本生成图像、文本生成视频以及图像转视频.yml

2025年6月2日-version 0.0.3.22：增加衡水体英语作文评分工作流.yml

2025年5月30日-version 0.0.3.21：增加中小学数学错题本-生成同类型题.yml

2025年5月29日-version 0.0.3.20：增加中小学数学错题本-错题收集篇.yml

2025年5月28日-version 0.0.3.19：增加0 代码实现企业画像！16 种图表，解锁数据查询新姿势.yml

2025年5月24 日-version 0.0.3.18：增加英语单词口语练习.yml

2025年5月23 日-version 0.0.3.17：增加海报封面生成工作流-Wanx 文生图.yml

2025年5月21 日-version 0.0.3.16：增加12306mcp火车票信息查询-chatflow.yml、12306mcp火车票信息查询-AIAgent.yml

2025年5月20 日-version 0.0.3.15：增加音视频转文字会议纪要.yml

2025年5月13 日-version 0.0.3.14：增加基于上市公司财报分析结果html分析报告（整合MinerU+edgeone-pages-mcp）.yml后端代码复用之前的代码 https://github.com/wwwzhouhui/dify-for-dsl/tree/main/dsl/makehtml/makehtmlapi.py

2025年5月10 日-version 0.0.3.13：增加多模态图像编辑(HiDream-E1-Full)chatflow.yml以及代码等资料详见https://github.com/wwwzhouhui/dify-for-dsl/tree/main/dsl/difyforgitee

2025年5月3 日-version 0.0.3.12：增加图片生成html,网页小游戏（1panel mcpsse）.yml 

2025年4月29 日-version 0.0.3.11：增加通用合同审查助手.yml

2025年4月26 日-version 0.0.3.10：增加基于魔搭社区MCP-Server.yml（包含魔搭社区MCP-server(高德MCP 、好吃的、Tavily、LeetCode(力扣) 4个MCP-Server）

2025年4月24 日-version 0.0.3.09：增加基于知识库+agent实现text2sqlchatflow工作流.yml、基于表结构的agent text2sql.yml

2025年4月23 日-version 0.0.3.08：增加软件开发类合同审查chatflow.yml

2025年4月19 日-version 0.0.3.07：增加提示词生成器chatflow.yml

2025年4月14 日-version 0.0.3.06：增加儿童故事绘本-PPT Agent.yml、儿童故事绘本-PPT chatflow.yml

2025年4月11 日-version 0.0.3.05：
新增docker部署：docker-compose up --build，

汇总功能性接口[g_jiekou.py](geekaiapp/g_jiekou.py)，

拆分部分业务独立运行：

1.[yewu2edgetts](yewu2edgetts)文字转语音


2.[yewu2excelhtml](yewu2excelhtml)数据可视化md转文档

3.[yewu2googleimgtxt](yewu2googleimgtxt)Gemini文生图，图+文生图，连载

4.[yewu2jmvideo](yewu2jmvideo)即梦AI文生视频

5.[yewu2story](yewu2story)文生音频+图片=动漫人物连载

6.[yewu2videoaddsrt](yewu2videoaddsrt)视频加字幕+音频可编辑（支持软硬字幕）

apikey值配置参考以往文章即可。

2025年4月9 日-version 0.0.3.04：增加学生成绩查询Chatflow支持text2sql.yml，student_scores.sql 建表语句详见

 https://github.com/wwwzhouhui/dify-for-dsl/tree/main/dsl/db/test2sql/student_scores.sql

2025年4月7 日-version 0.0.3.03：增加dify-mcp-sse+Zapier MCP新闻检索邮件发送.yml

2025年4月3 日-version 0.0.3.02：增加人物头像风格迁移工作流.yml以及代码详见https://github.com/wwwzhouhui/dify-for-dsl/tree/main/dsl/beartAI/beartAI_face_swap.py

2025年4月2 日-version 0.0.3.01：增加免费即梦文生视频mcp-server,代码详见 https://github.com/wwwzhouhui/dify-for-dsl/tree/main/mcp/fastapi-mcp-server/jimeng/jimeng_video_service.py

2025年4月1 日-version 0.0.2.28 :免费即梦文生视频.yml 提供第三方接口api源码 代码看  https://github.com/wwwzhouhui/dify-for-dsl/tree/main/dsl/jimeng/jimeng_video_service.py  详细操作可以看文档说明即梦文生视频逆向接口部署使用.md

2025年3月27 日-version 0.0.2.27 :对抗测试方案.md  周易大师.yml

2025年3月26 日-version 0.0.2.26 :大学生计算机专业简历美化工作流.yml

2025年3月25 日-version 0.0.2.25 :文生Word_Http_Post.yml、文生Word_Agent.yml 提供第三方接口api源码 代码看 https://github.com/wwwzhouhui/dify-for-dsl/tree/main/dsl/office/word/md_to_docx_server.py

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

6.[prompt-optimizer](https://github.com/linshenkx/prompt-optimizer)

  一款提示词优化器，助力于编写高质量的提示词

## 问题反馈

如有问题，请在GitHub Issue中提交，在提交问题之前，请先查阅以往的issue是否能解决你的问题

## 常见问题汇总

<details>
<summary>http请求节点超时时间及请求体大小限制的配置调整</summary>
     修改docker-compose.yaml<br>
<img src="https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250409115803027.png" alt="示例图片" width="400"><br>
    对应的源码
    <img src="https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/cfbdbf9f-5271-4593-af35-1dd0c14d8b12.png" alt="示例图片" width="400">
</details>
<details>
<summary>80端口被占用修改其他端口</summary>
     问题默认dify使用的是80端口。但是有的小伙伴服务器80端口被占用了，只能通过修改端口问题实现访问dify的访问。<br>
    我们修改.env配置<br>
    源配置信息<br>
    EXPOSE_NGINX_PORT=80<br>
    EXPOSE_NGINX_SSL_PORT=443<br>
    修改后<br>
    EXPOSE_NGINX_PORT=88<br>
    EXPOSE_NGINX_SSL_PORT=8443<br>
    这里我们需要把80（http）和443（https）修改服务器未被使用端口，我这里修改成88 和4443端口<br>
<img src="https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250419164431488.png" ><br>
    修改后的效果 dify访问地址变成http://101.126.84.227:88/<br>
    <img src="https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250419163321317.png" >
</details>

<details>
<summary>应用端口不是80分享修改端口配置</summary>
     对外访问的API接口地址是http://101.126.84.227/v1，分享后访问失败<br>
<img src="https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250419164757901.png" ><br>
    解决我们修改.env配置<br>
    源配置信息默认是空的<br>
    # Service API Url,<br>
	# used to display Service API Base Url to the front-end.<br>
	# If empty, it is the same domain.<br>
	# Example: https://api.dify.ai<br>
	SERVICE_API_URL=<br>
     修改后<br>
    # Service API Url,<br>
	# used to display Service API Base Url to the front-end.<br>
	# If empty, it is the same domain.<br>
	# Example: https://api.dify.ai<br>
	SERVICE_API_URL=http://101.126.84.227:88<br>
    这里我们需要填写服务器对外访问地址+端口号http://101.126.84.227:88<br>
    <img src="https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250419170233151.png" >
    修改后重启，重启后我们访问web应用<br>
    <img src="https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250419170415108.png" >
</details>
<details>
<summary>文档提取器不支持 doc文件上传</summary>
     文档提取器不支持doc文件<br>
<img src="https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250423110402835.png" ><br>
    如果用户输入doc 文件上传会报错<br>
    <img src="https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250423110443749.png" >
    建议用wps或者office 转一下变成docx文件<br>
</details>
<details>
<summary>插件和模型下载慢</summary>
     默认dify 配置什么都不该的情况下 安装模型非常慢（国内网络环境）<br>
<img src="https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250429133213256.png" ><br>
    点击安装模型或则工具后半天没反应。 这里主要的原因的目前模型插件和工具下载后都需要在容器内部实现python依赖包的安装，而python依赖包安装需要网络环境，所以下载非常慢。可以修改.env 文件中的配置（大概1041行）<br>
    # PIP_MIRROR_URL=https://pypi.tuna.tsinghua.edu.cn/simple<br>
PIP_MIRROR_URL=<br>
    我们需要把上https://pypi.tuna.tsinghua.edu.cn/simple 配置填写，修改后的地址如下<br>
    # PIP_MIRROR_URL=https://pypi.tuna.tsinghua.edu.cn/simple <br>
PIP_MIRROR_URL=https://pypi.tuna.tsinghua.edu.cn/simple <br>
    修改后重启dify  后面安装就非常快了。<br>
</details>
<details>
<summary>带文件的插件出现Request URL is missing an 'http://' or 'https://' protocol</summary>
     我们配置第三方插件比如MinerU 、Base64 编解码器等支持文件的插件下载完成后使用报错<br>
<img src="https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250510003529262.png" ><br>
    出现上述错误如何解决？<br>
    需要修改2个地方。<br>
     1.env 文件中查找FILES_URL<br>
    默认的FILES_URL是空的，我们需要修改使用 http://<your-ip>:5001 或 http://api:5001，在此情况下，确保外部可以访问端口 5001<br>
    <img src="https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250510003900660.png" ><br>
    2.docker-compose.yaml 对应的FILES_URL修改<br>
     <img src="https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250510004029749.png" ><br>
    此外dify-api容器镜像端口开放出来（默认情况是不开放的），增加如下代码<br>
     ports: <br>
   - '5001:5001' <br>
    <img src="https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250510004232125.png" ><br>
    我们也可以从docker容器看到端口开放情况（默认是不开启的） <br>
 <img src="https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250510004416081.png" ><br>
</details>
<details>
<summary>自定义工具超时时间和超时重试次数设置</summary>
     我们在.env文件找到<br>
    API_TOOL_DEFAULT_CONNECT_TIMEOUT=10<br>
    API_TOOL_DEFAULT_READ_TIMEOUT=60<br>
</details>

<details>
<summary>dify-sandbox-py 项目如何自定义编译打包</summary>
     1下载 https://github.com/svcvit/dify-sandbox-py项目<br>
    git clone https://github.com/svcvit/dify-sandbox-py<br>
    <img src="https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/QQ20250512-212041.png" ><br>
    接下来我们输入如下命令实现自定义打包<br>
    cd F:\temp\dify-sandbox-py<br>
    docker build -t dify-sandbox-py:local .<br>
</details>

<details>
<summary>sandbox 如何安装pandas这些第三方库？</summary>
      打开dify  docker 文件夹里面docker-compose.yaml文件<br>
    <img src="https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250512221641604.png" ><br>
    打开docker-compose.yaml 搜索langgenius/dify-sandbox 添加python-requirements.txt 依赖包<br>
    volumes:<br>
        - ./volumes/sandbox/dependencies/python-requ<br>irements.txt:/dependencies<br>
        - ./volumes/sandbox/conf:/conf<br>
    我们添加pandas依赖包<br>
     <img src="https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250512222233209.png" ><br>
    以上添加完成后，重启dify<br>
    docker compose up -d <br>
</details>

<details>
<summary>如何把pg数据对外开启访问</summary>
     由于安全性考虑dify使用docker 容器化部署的时候默认是不对外开启数据库访问的，如果你需要二次开发通过数据库连接整合对接这个时候是需要访问容器数据库，这个时候就需要把数据库开启对外访问。<br>
    修改docker-compose.yaml 文件 image: postgres:15-alpine 将数据库端口开放出来<br>
      原配置文件<br>
    <img src="https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250530134120141.png" ><br>
    修改后<br>
    <img src="https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250530134203328.png" ><br>
</details>    

<details>
<summary>容器内访问不了外部怎么办？</summary>
     <img src="https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250525105728679.png" ><br>
    遇到上面的问题主要是容器内部没办法通过127.0.0.1 访问局域网地址<br>
    方法1 把模型请求地址换成局域网地址<br>
    <img src="https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250525110133945.png" ><br>
     方法2：改成http://host.docker.internal:11434<br>
    `host.docker.internal` 是 Docker 提供的一个特殊域名，用于在 **容器内部访问宿主机（运行 Docker 的主机）的网络服务**。它的作用    是简化容器与宿主机之间的网络通信，尤其在开发场景中非常实用<br>
    **适用场景**：当容器需要访问宿主机上运行的服务（如数据库、API 接口等）时，可直接使用 `host.docker.internal` 作为宿主机的地址，避免手动查找宿主机的 IP 地址（如 `192.168.x.x` 或 `localhost`）<br>
    **本质**：Docker 会将该域名自动解析为宿主机的 IP 地址，实现容器与宿主机的网络互通。<br>
</details>
<details>
<summary>字符串内容超过80000限制</summary>
      Run failed: The length of output variable result must be less than 80000 characters<br>
    修改.env 配置文件<br>
    CODE MAX STRING LENGTH=800000<br>
    TEMPLATE TRANSFORM MX LENGTH-800000<br>
      可以参考下面图<br>
    <img src="https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250531113229275.png" ><br>
</details>    

<details>
<summary>文件上传超过15MB的限制</summary>
<img src="https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250620143908372.png" ><br>
我们需要修改.env 文件里面<br>
UPLOAD_FILE_SIZE_LIMIT=15<br>
把它修改成 100 <br>
UPLOAD_FILE_SIZE_LIMIT=100<br>
另外 Nginx 反向代理配置部分修改<br>
NGINX_CLIENT_MAX_BODY_SIZE=15M<br>
修改 <br>
NGINX_CLIENT_MAX_BODY_SIZE=100M<br>
修改后记得重启。<br>
</details>



## 技术交流群

![Screenshot_20250708_164428_com.tencent.mm](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Screenshot_20250708_164428_com.tencent.mm.jpg)

## Star History

![dify-for-dsl](https://api.star-history.com/svg?repos=wwwzhouhui/dify-for-dsl&type=Date)