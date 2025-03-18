# 1.依赖包安装

 首先需要在本地电脑上安装好python 运行环境，建议python3.10+

 安装如下依赖包

```
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

![image-20250318104545091](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250318104545091.png)

# 2.配置文件说明

config.ini

```ini
[common]
region = xxxx
secret_id = xxxx
secret_key = xxx
bucket = xxx

[llm]
text_llm_provider = intern
text_llm_model = internlm3-latest
image_llm_provider = siliconflow
image_llm_model = black-forest-labs/FLUX.1-schnell
openai_base_url = https://api.openai.com/v1
aliyun_base_url = https://dashscope.aliyuncs.com/compatible-mode/v1
deepseek_base_url = https://api.deepseek.com/v1
ollama_base_url = http://localhost:11434/v1
siliconflow_base_url = https://api.siliconflow.cn/v1
intern_base_url = https://chat.intern-ai.org.cn/api/v1
openai_api_key = ""
aliyun_api_key = ""
deepseek_api_key = ""
ollama_api_key = ""
siliconflow_api_key = sk-xxxxx
intern_api_key = 

[voice]
voice_name = zh-CN-XiaoxiaoNeural
voice_rate = 1.0

[server]
host = 127.0.0.1
port = 8000

[auth]
valid_tokens = ["zhouhui-1258720xxxx"]
```

 说明 common 配置下面4个值是腾讯COS 相关配置，主要目的生成的视频上传腾讯COS 上方便后面浏览和显示视频。

  llm  配置中text_llm_provider 文本类模型提供商，目前提供 上海人工智能实验室书生（intern）、openai、aliyun、deepseek、ollama、硅基流动（siliconflow）；text_llm_model 对应使用各个厂商提供的模型名称; image_llm_provider 和 image_llm_model 顾名思义就是硅基提供的文生图的模型；api key 就是配置各个厂商提供api key 就可以了。

auth 是客户端和服务端通过http请求的鉴权账号。可以自定义，服务端配置后，客户端调用的地方需要和这个账号保持一致，否自会报401的错误。

![image-20250318115922798](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250318115922798.png)

上面客户端API 可以key 需要和服务端 保持一致。

![image-20250318115959122](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250318115959122.png)

如果是用dify 可以在调用http 请求API key 设置

![image-20250318120104390](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250318120104390.png)

# 3.启动服务

```
 python main.py
```

  完成启动服务

![image-20250318105520756](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250318105520756.png)

# 4.客户端测试代码验证

 服务端启动后我们使用teststoryvideo.py 可以对服务端请求发起测试 生成短视频

```
python teststoryvideo.py 
```

 客户端代码如果想运行需要修改一些调用的地方

 api_token

text_llm_provider

image_llm_provider

text_llm_model

image_llm_model

![image-20250318120319303](C:/Users/wwwzh/AppData/Roaming/Typora/typora-user-images/image-20250318120319303.png)

![image-20250318120354879](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250318120354879.png)

下面看一下运行效果服务端会返回 分镜提示词

![image-20250318105921590](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250318105921590.png)

 调用API 生成绘画，接下来会生成语音

![image-20250318105958847](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250318105958847.png)

最后生成视频并上传腾讯COS 提供 视频链接地址

![image-20250318110042223](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250318110042223.png)

 客户端返回视频生成 URL

![image-20250318110113576](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250318110113576.png)

 视频同时在项目tasks 目录下生成最新的视频文件。

 ![image-20250318110232095](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250318110232095.png)

​      演示效果

<video controls>   <source src='https://dify-1258720957.cos.ap-nanjing.myqcloud.com/videos/video20250318105914.mp4' type='video/mp4'>{filename}</video>



# 5.给dify调用

后面我们就可以在dify上配置http请求调用该生成视频的http客户端请求调用了。

![image-20250318111802065](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250318111802065.png)

http请求这块 目前是写死 方便调试 ，大家也可以使用Chrome插件 调试整理json格式

chrome-extension://pkgccpejnmalmdinmhkkfafefagiiiad/json-format/index.html

![image-20250318111904213](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250318111904213.png)

  通过该工具方便编写JSON，以及对JSON格式语法检查。

  关于dify 使用关系我微信公众号文章wwzhouhui

  

  ![image-20250318115103435](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/image-20250318115103435.png)