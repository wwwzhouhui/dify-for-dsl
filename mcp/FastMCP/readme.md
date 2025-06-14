#   0.运行环境

​       先保证电脑上安装好python 运行环境，python  版本>=3.10

![image-20250614200946253](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250614200946253.png)

  以上我的运行环境是python 版本是3.12.8

# 1.依赖包安装

```
       cd  F:\work\code\2025dify-dsl\dify-for-dsl\mcp\FastMCP
       pip install -r  requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

​     安装完成依赖包

​      ![image-20250614201049497](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250614201049497.png)

# 2.修改代码增加火山引擎API key

  代码doubao_mcp_ai_server2.py  第14行

 API_KEY = "火山引擎API密钥"   换成你的api 秘钥

 ![image-20250614201359605](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250614201359605.png)

这个火山引擎的api 在哪里获取登录火上引擎 https://console.volcengine.com/ark/region:ark+cn-beijing/overview?briefPage=0&briefType=introduce&type=new

有个API 管理

![image-20250614201758573](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250614201758573.png)

关于使用火山引擎模型，需要分别授权开通，点击开通管理

![image-20250614201840722](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250614201840722.png)

关于火山引擎详细开通可以参考我之前文章公众号文章《[免费体验 DeepSeek 联网功能！火山引擎 + 第三方套壳软件，开启 AI 新体验](https://mp.weixin.qq.com/s/pyRyusxgyDLy8-3-ustpyw)》

# 3.启动doubao_mcp_ai_server2.py

```shell
python doubao_mcp_ai_server2.py
```

![image-20250614202419175](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250614202419175.png)

上面我们就完成了一个mcp_server   启动.（当然你也可以部署在服务器上）

# 4.客户端（Cherry Studio）配置

 这里我们使用Cherry Studio来做测试

![image-20250612182429083](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250612182429083.png.png)

点开这里我们添加一个服务器,我们选择sse,添加URL

![image-20250614202702442](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250614202702442.png)

 设置完成后，点击保存按钮。

  接下来我点击工具按钮查看MCP 有哪些方法



![image-20250614202741960](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250614202741960.png)

 这样我们就完成MCP-Server客户端的配置。

  我们打开控制台 也能看到服务端收到的请求信息

![image-20250614202818927](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250614202818927.png)

# 5.验证云服务SSE

 我们这里使用dify来实现SSE方式验证测试一下。

## dify

​    我们使用dify平台配置一个AI Agent，模型这里我们选择火山引擎的deepseek-v3 模型（其他模型效果不行）

![image-20250612214657065](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250612214657065.png.png)

   我们需要其他配置好mcp-see 地址

```shell
{ "doubao_mcp_ai_server": { "url": "http://127.0.0.1:8002/sse", "headers": {}, "timeout": 60, "sse_read_timeout": 300 } }
```

   把上面的sse配置填写到MCP-see配置中完成授权

![image-20250612214933729](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250612214933729.png.png)

​      回到ai Agent中设置好MCP-SSE

![image-20250612214740391](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250612214740391.png.png)

  接下来我们进入聊天对话窗口中

![image-20250612215601110](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250612215601110.png.png)

第一次对话模型调用工具发现没有授权，提示我们先填写APIkey授权。 我们填写授权后开启ai 绘画

![image-20250612220528179](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250612220528179.png.png)

![image-20250612220604695](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250612220604695.png.png)

