# 工作流说明

工作流文件FLUX绘画机器人+多模态识别+语音播放.yml

工作流截图

![image-20250112170354957](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250112170354957.png)

 工作流运行效果

![image-20250112170519812](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20250112170519812.png)

 系统体验地址（临时不保证永久使用）

 http://101.126.84.227:88/chat/X3rxcjUYx0tQCutv

# 用的模型

 文本生成模型internlm/internlm2_5-7b-chat   flux提示词转换生成以及文本翻译使用

多模态模型Pro/OpenGVLab/InternVL2-8B    生成的图片实现OCR 图片生成内容

文生图模型 black-forest-labs/FLUX.1-schnell  使用该模型实现文本生成图片

文生语音模型 FunAudioLLM/CosyVoice2-0.5B  使用该模型实现文本生成语言生成TTS播报功能

# 关键技术点

1. flux提示词

2. 硅基流动多模态接口、文生图片接口

3. 自定义工具调用文本生成语言生成TTS播报功能，并整合腾讯云OSS存储实现语音生成URL存储

   关于自定义工具如何制作部署发布 可以参考https://github.com/wwwzhouhui/dify-for-dsl/blob/main/dsl/difyforgitee/dify%E4%B8%AD%E5%88%9B%E5%BB%BA%E5%B9%B6%E4%BD%BF%E7%94%A8%E8%87%AA%E5%AE%9A%E4%B9%89%E5%B7%A5%E5%85%B7-gitee%E7%BB%98%E7%94%BB.md