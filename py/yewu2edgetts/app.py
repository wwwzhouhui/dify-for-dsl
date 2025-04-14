from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import edge_tts
import asyncio
import uuid
import os
from typing import Optional
from mutagen.mp3 import MP3
import time
from datetime import datetime
import logging
from functools import lru_cache
import shutil

from geekaiapp.g_utils import baseurl, ip_tts

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('tts.log', encoding='utf-8')
    ]
)

app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# 配置静态文件服务
os.makedirs("static/audio", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# 获取当前文件的绝对路径
# current_dir = os.path.dirname(os.path.abspath(__file__))
# static_dir = os.path.join(current_dir, "..", "static")
# app.mount("/static", StaticFiles(directory=static_dir), name="static")

ooutput1 = baseurl / ip_tts
print("完整路径-g_jiekou1", ooutput1)

# 添加根路径处理
@app.get("/")
async def read_root():
    return FileResponse('index.html')

# 修改 favicon 处理部分
@app.get('/favicon.ico')
async def favicon():
    try:
        # 直接用网站根目录的 favicon.ico
        favicon_path = '/www/wwwroot/favicon.ico'
        if os.path.exists(favicon_path):
            return FileResponse(
                favicon_path,
                media_type="image/x-icon"
            )
        else:
            print(f"Favicon not found at: {favicon_path}")
            raise HTTPException(status_code=404, detail="Favicon not found")
    except Exception as e:
        print(f"Error serving favicon: {str(e)}")
        raise HTTPException(status_code=404, detail="Favicon not found")

# 在 app.mount 之前添加静态文件路由
@app.get("/static/{file_path:path}")
async def static_files(file_path: str):
    return FileResponse(f"static/{file_path}")

class TTSRequest(BaseModel):
    text: str
    voice_id: str
    speed: float = 1.0
    autoplay: bool = True
    user_id: str

class Voice(BaseModel):
    id: str
    name: str
    gender: str
    language: str

# 缓存可用的声音列
VOICE_CACHE = {}

# 缓存声音列表，每小时更新一次
@lru_cache(maxsize=1)
def get_cache_key():
    """生成基于小时的缓存键"""
    now = datetime.now()
    return now.strftime("%Y%m%d%H")

async def get_voices():
    try:
        cache_key = get_cache_key()
        if cache_key in VOICE_CACHE:
            return VOICE_CACHE[cache_key]
        
        print("Fetching voices from edge-tts...")
        voices = await edge_tts.list_voices()
        print(f"Got {len(voices)} voices from edge-tts")
        
        # 初始化语言分类字典
        voice_dict = {}
        
        for voice in voices:
            # 将所有中文声音统一到 zh-CN
            lang = "zh-CN" if voice["Locale"].startswith("zh") else voice["Locale"]
            
            if lang not in voice_dict:
                voice_dict[lang] = []
            
            # 添加更友好的声音名称
            friendly_name = {
                # 中文普通话 - 男声
                "zh-CN-YunjianNeural": "云健 (标准男声)",
                "zh-CN-YunxiNeural": "云希 (阳光男声)",
                "zh-CN-YunxiaNeural": "云夏 (男童声)",
                "zh-CN-YunyangNeural": "云扬 (新闻男声)",
                "zh-CN-YunfengNeural": "云峰 (成熟男声)",
                "zh-CN-YunzeNeural": "云泽 (温柔男声)",
                "zh-CN-YunhaoNeural": "云浩 (商务男声)",
                "zh-CN-YunleNeural": "云乐 (活力男声)",
                "zh-CN-YunxuanNeural": "云轩 (青年男声)",
                "zh-CN-YunqiangNeural": "云强 (浑厚男声)",
                "zh-CN-YunpengNeural": "云鹏 (书生男声)",
                "zh-CN-YunwenNeural": "云文 (儒雅男声)",
                "zh-CN-YunchengNeural": "云程 (知性男声)",
                "zh-CN-YunhuiNeural": "云辉 (磁性男声)",
                "zh-CN-YunminNeural": "云敏 (清新男声)",
                
                # 中文普通话 - 女声
                "zh-CN-XiaoxiaoNeural": "晓晓 (标准女声)",
                "zh-CN-XiaoyiNeural": "晓伊 (温柔女声)",
                "zh-CN-XiaohanNeural": "晓涵 (活力女声)",
                "zh-CN-XiaomengNeural": "晓梦 (甜美女声)",
                "zh-CN-XiaomoNeural": "晓墨 (文艺女声)",
                "zh-CN-XiaoxuanNeural": "晓萱 (知性女声)",
                "zh-CN-XiaoruiNeural": "晓睿 (儿童女声)",
                "zh-CN-XiaoshuangNeural": "晓双 (青年女声)",
                "zh-CN-XiaoyanNeural": "晓妍 (邻家女声)",
                "zh-CN-XiaochenNeural": "晓辰 (自然女声)",
                "zh-CN-XiaoqiuNeural": "晓秋 (温暖女声)",
                "zh-CN-XiaozhenNeural": "晓珍 (优雅女声)",
                "zh-CN-XiaohuiNeural": "晓慧 (干练女声)",
                "zh-CN-XiaolingNeural": "晓玲 (甜美女声)",
                "zh-CN-XiaoxuanNeural": "晓轩 (标准女声)",
                "zh-CN-XiaoyouNeural": "晓悠 (柔美女声)",
                "zh-CN-XiaoqingNeural": "晓青 (清新女声)",
                "zh-CN-XiaorongNeural": "晓蓉 (标准女声)",
                "zh-CN-XiaoyanNeural": "晓妍 (时尚女声)",
                "zh-CN-XiaojingNeural": "晓静 (标准女声)",
                "zh-CN-XiaohuanNeural": "晓欢 (活泼女声)",
                "zh-CN-XiaoyunNeural": "晓云 (标准女声)",
                "zh-CN-XiaolingNeural": "晓玲 (标准女声)",
                "zh-CN-XiaoxianNeural": "晓仙 (空灵女声)",
                "zh-CN-XiaoxueNeural": "晓雪 (清纯女声)",
                
                # 中文方言 - 男声
                "zh-CN-shandong-YunxiangNeural": "云翔 (山东话)",
                "zh-CN-sichuan-YunxiNeural": "云希 (四川话)",
                "zh-CN-henan-YundengNeural": "云登 (河南话)",
                "zh-CN-hubei-YunrongNeural": "云荣 (湖北话)",
                "zh-CN-shanxi-YunjiangNeural": "云江 (山西话)",
                "zh-CN-guangdong-YunrongNeural": "云荣 (粤语男声)",
                "zh-CN-hebei-YunboNeural": "云博 (河北话)",
                "zh-CN-hunan-YunwenNeural": "云文 (湖南话)",
                "zh-CN-jiangxi-YunfengNeural": "云峰 (江西话)",
                "zh-CN-guizhou-YunhaoNeural": "云浩 (贵州话)",
                
                # 中文方言 - 女声
                "zh-CN-liaoning-XiaobeiNeural": "晓北 (东北话)",
                "zh-CN-shaanxi-XiaoniNeural": "晓妮 (陕西话)",
                "zh-CN-zhijiang-XiaotongNeural": "晓彤 (长江话)",
                "zh-CN-jiangsu-XiaoleiNeural": "晓蕾 (江苏话)",
                "zh-CN-zhejiang-XiaonianNeural": "晓年 (浙江话)",
                "zh-CN-guangxi-XiaominNeural": "晓敏 (桂林话)",
                "zh-CN-fujian-XiaomeiNeural": "晓梅 (闽南话)",
                "zh-CN-anhui-XiaoruiNeural": "晓睿 (安徽话)",
                "zh-CN-yunnan-XiaojingNeural": "晓静 (云南话)",
                "zh-CN-gansu-XiaoqingNeural": "晓青 (甘肃话)",
                
                # 港台声音
                "zh-HK-HiuGaaiNeural": "晓佳 (粤语女声)",
                "zh-HK-HiuMaanNeural": "晓曼 (粤语女声)",
                "zh-HK-WanLungNeural": "云龙 (粤男声)",
                "zh-TW-HsiaoChenNeural": "晓辰 (台湾女声)",
                "zh-TW-YunJheNeural": "云哲 (台湾男声)",
                "zh-TW-HsiaoYuNeural": "晓雨 (台湾女声)",
                "zh-TW-HsiaoTungNeural": "晓彤 (台湾女声)",
                "zh-TW-YunFuNeural": "云甫 (台湾男声)",
                
                # 英文声音
                "en-US-GuyNeural": "Guy (美式男声)",
                "en-US-DavisNeural": "Davis (美式男声)",
                "en-US-TonyNeural": "Tony (美式男声)",
                "en-US-JennyNeural": "Jenny (美式女声)",
                "en-US-AriaNeural": "Aria (美式女声)",
                "en-GB-RyanNeural": "Ryan (英式男声)",
                "en-GB-SoniaNeural": "Sonia (英式女声)",
                
                # 日文声音
                "ja-JP-KeitaNeural": "圭太 (日本男声)",
                "ja-JP-DaichiNeural": "大智 (日本男声)",
                "ja-JP-NanamiNeural": "七海 (日本女声)",
                "ja-JP-AoiNeural": "葵 (日本女声)",
            }.get(voice["ShortName"], voice["ShortName"])
            
            print(f"Adding voice: {friendly_name} ({voice['ShortName']})")
            
            voice_dict[lang].append({
                "id": voice["ShortName"],
                "name": friendly_name,
                "gender": voice["Gender"].lower(),
                "language": lang
            })
        
        # 更新缓存
        VOICE_CACHE[cache_key] = voice_dict
        return voice_dict
    except Exception as e:
        print(f"Error in get_voices: {str(e)}")
        raise

@app.get("/api/voices")
async def list_voices(language: str = "zh-CN", gender: Optional[str] = None):
    try:
        print(f"Fetching voices for language: {language}, gender: {gender}")
        voices = await get_voices()
        print(f"Available languages: {list(voices.keys())}")
        
        # 获取所有匹配语言前缀的声音
        filtered_voices = []
        
        # 处理中文声音（包括普通话、方言、港台）
        if language == "zh-CN":
            # 收集所有中文相关声音
            for lang, voice_list in voices.items():
                if lang.startswith("zh-"):  # 匹配所有中文声音（包括 zh-CN, zh-HK, zh-TW）
                    filtered_voices.extend(voice_list)
                elif lang == "zh":  # 防止可能的其他中文变体
                    filtered_voices.extend(voice_list)
        else:
            # 其他语言的常规匹配
            for lang, voice_list in voices.items():
                if lang.startswith(language):
                    filtered_voices.extend(voice_list)
        
        print(f"Found {len(filtered_voices)} voices before gender filter")
        
        # 应用性别过滤
        if gender:
            def is_matching_voice(voice):
                voice_id = voice["id"].lower()
                name = voice["name"].lower()
                
                # 通用匹配规则
                if gender.lower() == "male":
                    if (
                        voice["gender"].lower() == "male" or
                        "男" in name or
                        ("云" in name and "晓" not in name) or  # 确保是云字辈且不包含晓字
                        (any(x in voice_id.lower() for x in [
                            "yun", "wan", "-yun"
                        ]) and not any(x in voice_id.lower() for x in [
                            "xiao", "hiu", "hsiao"  # 排除包含女声标识的ID
                        ]))
                    ):
                        return True
                else:  # female
                    if (
                        voice["gender"].lower() == "female" or
                        "女" in name or
                        ("晓" in name and "云" not in name) or  # 确保是晓字辈且不包含云字
                        (any(x in voice_id.lower() for x in [
                            "xiao", "hiu", "hsiao", "-xiao"
                        ]) and not any(x in voice_id.lower() for x in [
                            "yun", "wan"  # 排除包含男声标识的ID
                        ]))
                    ):
                        return True
                return False
            
            filtered_voices = [v for v in filtered_voices if is_matching_voice(v)]
            print(f"Found {len(filtered_voices)} voices after gender filter")
            
            # 打印过滤后的声音详情
            for voice in filtered_voices:
                print(f"Filtered voice: {voice['name']} ({voice['id']}, {voice['gender']})")
        
        # 按特定顺序排序
        def sort_key(voice):
            # 定义声音类型的排序优先级
            voice_type_order = {
                "标准": 1,
                "新闻": 2,
                "成熟": 3,
                "阳光": 4,
                "温柔": 5,
                "商务": 6,
                "活力": 7,
                "磁性": 8,
                "浑厚": 9,
                "书生": 10,
                "儒雅": 11,
                "男童": 12,
                "东北": 13,
                "山东": 14,
                "四川": 15,
                "河南": 16,
                "湖北": 17,
                "山西": 18,
                "河北": 19,
                "湖南": 20,
                "江西": 21,
                "贵州": 22,
                "江苏": 23,
                "浙江": 24,
                "广西": 25,
                "福建": 26,
                "安徽": 27,
                "云南": 28,
                "甘肃": 29,
                "粤语": 30,
                "闽南": 31,
                "台湾": 32,
            }
            
            # 获取声音类型的排序值
            name = voice["name"]
            for key, value in voice_type_order.items():
                if key in name:
                    return value
            return 100  # 其他类型放到最后
            
        # 先按类型排序，然后按名称排序
        filtered_voices.sort(key=lambda x: (sort_key(x), x["name"]))
        
        return filtered_voices
    except Exception as e:
        print(f"Error in list_voices: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# 添加时长格式化函数
def format_duration(seconds):
    """将秒数转换为 MM:SS 格式"""
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

@app.post("/api/generate")
async def generate_audio(request: TTSRequest):
    try:
        # 验证请求参数
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="文本内容不能为空")
        if not request.voice_id:
            raise HTTPException(status_code=400, detail="未选择声音")
        if not 0.25 <= request.speed <= 4:
            raise HTTPException(status_code=400, detail="语速设置无效")
            
        # 生成文件名时包含用户ID
        filename = f"{request.user_id}_{str(uuid.uuid4())}"
        audio_path = f"static/audio/{filename}.mp3"
        subtitle_path = f"static/audio/{filename}.srt"
        
        # 确保目录存在
        os.makedirs("static/audio", exist_ok=True)
        
        try:
            logging.info(f"Starting audio generation for user {request.user_id}")
            print(f"Starting audio generation...")
            print(f"Text: {request.text[:100]}...")
            print(f"Voice ID: {request.voice_id}")
            print(f"Speed: {request.speed}")
            
            # 修改语速格式
            speed_percentage = int((request.speed - 1) * 100)
            rate = f"{speed_percentage:+d}%"
            print(f"Calculated rate: {rate}")
            
            try:
                # 验证文本长度
                if len(request.text) > 10000:  # 设置合理的文本长度限制
                    raise HTTPException(status_code=400, detail="文本内容过长")
                
                # 验证语速范围
                if not 0.25 <= request.speed <= 4:
                    raise HTTPException(status_code=400, detail="语速必须在 0.25 到 4 之间")
                
                # 验证声音ID是否存在
                voices = await get_voices()
                available_voices = []
                for voice_list in voices.values():
                    available_voices.extend([v["id"] for v in voice_list])
                if request.voice_id not in available_voices:
                    raise HTTPException(status_code=400, detail="选择的声不可用")
                
                # 设置语音参数并生成
                communicate = edge_tts.Communicate(
                    text=request.text,
                    voice=request.voice_id,
                    rate=rate
                )
                print("Created communicate object")

                # 生成音频和字幕
                print(f"Saving audio to: {audio_path}")
                audio_data = []
                subtitle_data = []
                subtitle_index = 1
                
                # 用于合并幕的临时存储
                temp_text = []
                temp_start = None
                temp_end = None
                
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        audio_data.append(chunk["data"])
                    elif chunk["type"] == "WordBoundary":
                        # 转换时间戳
                        start_ms = int(chunk['offset'] / 10000)
                        duration_ms = int(chunk['duration'] / 10000)
                        end_ms = start_ms + duration_ms
                        
                        # 如果是新的字幕组或时间间隔太大，就保存当前组
                        if temp_start is None:
                            temp_start = start_ms
                            temp_end = end_ms
                            temp_text.append(chunk["text"])
                        elif end_ms - temp_end > 500:  # 如果间隔超过500毫秒，就作为新的字幕
                            # 保存当前字幕组
                            start_time = format_time(temp_start)
                            end_time = format_time(temp_end)
                            
                            subtitle_entry = [
                                f"{subtitle_index}",
                                f"{start_time} --> {end_time}",
                                "".join(temp_text),
                                ""
                            ]
                            print(f"Adding subtitle entry:\n" + "\n".join(subtitle_entry))
                            subtitle_data.extend(subtitle_entry)
                            subtitle_index += 1
                            
                            # 开始新的字幕组
                            temp_text = [chunk["text"]]
                            temp_start = start_ms
                            temp_end = end_ms
                        else:
                            # 继续当前字幕组
                            temp_text.append(chunk["text"])
                            temp_end = end_ms
                
                # 保存最后一组字幕
                if temp_text:
                    start_time = format_time(temp_start)
                    end_time = format_time(temp_end)
                    subtitle_entry = [
                        f"{subtitle_index}",
                        f"{start_time} --> {end_time}",
                        "".join(temp_text),
                        ""
                    ]
                    print(f"Adding subtitle entry:\n" + "\n".join(subtitle_entry))
                    subtitle_data.extend(subtitle_entry)
                
                # 写入音频文件
                with open(audio_path, "wb") as audio_file:
                    for data in audio_data:
                        audio_file.write(data)

                # 写入 SRT 格式字幕文件
                try:
                    subtitle_content = "\n".join(subtitle_data)
                    print(f"Writing subtitle content:\n{subtitle_content}")
                    
                    with open(subtitle_path, "w", encoding="utf-8", newline='\n') as subtitle_file:
                        subtitle_file.write(subtitle_content)
                        subtitle_file.flush()  # 确保数据写入磁盘
                        os.fsync(subtitle_file.fileno())  # 强制同步到磁盘
                    
                    # 添加短暂延迟确保文件完全写入
                    await asyncio.sleep(0.1)
                    
                    # 验证文件是否正确写入
                    if os.path.exists(subtitle_path):
                        with open(subtitle_path, "r", encoding="utf-8") as check_file:
                            saved_content = check_file.read()
                            print(f"Verified subtitle content:\n{saved_content}")
                            if saved_content != subtitle_content:
                                raise ValueError("Subtitle file content verification failed")
                    else:
                        raise ValueError("Subtitle file was not created")
                    
                    print(f"Subtitle file successfully written to {subtitle_path}")
                    
                except Exception as e:
                    print(f"Error writing subtitle file: {str(e)}")
                    raise

                print("Audio and subtitles saved successfully")
                
                # 再次验证文件是否可访问
                if not (os.path.exists(audio_path) and os.path.exists(subtitle_path)):
                    raise ValueError("Generated files are not accessible")
                
                # 获取文件大小和时长
                file_size = os.path.getsize(audio_path)
                try:
                    # 使用 mutagen 获取音频时长
                    audio = MP3(audio_path)
                    duration = format_duration(audio.info.length)
                    print(f"Audio duration: {duration}")
                except Exception as e:
                    print(f"Error getting audio duration: {str(e)}")
                    duration = "00:00"
                
                return JSONResponse({
                    "success": True,
                    "audio": {
                        "url": f"/static/audio/{filename}.mp3",
                        "name": f"{filename}.mp3",
                        "size": f"{file_size / 1024:.1f}KB",
                        "duration": duration,  # 使实际计算的时长
                        "id": filename
                    }
                })
                
            except Exception as e:
                print(f"Error during TTS generation: {str(e)}")
                print(f"Error type: {type(e)}")
                import traceback
                print(f"Traceback: {traceback.format_exc()}")
                raise ValueError(f"TTS生成失败: {str(e)}")
            
        except Exception as e:
            logging.error(f"Error in generation process: {str(e)}")
            # 清理可能部分生成的文件
            for path in [audio_path, subtitle_path]:
                if os.path.exists(path):
                    try:
                        os.remove(path)
                    except Exception as cleanup_error:
                        logging.error(f"Error cleaning up file {path}: {str(cleanup_error)}")
            raise
            
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        error_message = str(e)
        
        # 处理常见错误
        error_mapping = {
            "Connection refused": "无法连接到语音服务，请稍后重试",
            "Invalid rate": "语速设置无效，请使用正确的语速值",
            "Invalid voice": "选择的声音无效，请重新选择",
            "TTS generation failed": "语音生成失败，请重试",
            "No such file": "文件生成失败，请重试"
        }
        
        for key, value in error_mapping.items():
            if key in error_message:
                error_message = value
                break
        
        raise HTTPException(
            status_code=500,
            detail={
                "message": "生成音频失败",
                "error": error_message
            }
        )

@app.delete("/api/audio/{audio_id}")
async def delete_audio(audio_id: str):
    try:
        file_path = f"static/audio/{audio_id}"
        if os.path.exists(file_path):
            os.remove(file_path)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 添加获取音频列表的接口
@app.get("/api/audio/{user_id}")
async def list_audio(user_id: str):
    try:
        audio_files = []
        audio_dir = "static/audio"
        for filename in os.listdir(audio_dir):
            if filename.endswith(".mp3") and filename.startswith(f"{user_id}_"):
                file_path = os.path.join(audio_dir, filename)
                file_size = os.path.getsize(file_path)
                try:
                    audio = MP3(file_path)
                    duration = format_duration(audio.info.length)
                except Exception as e:
                    print(f"Error getting duration for {filename}: {str(e)}")
                    duration = "00:00"
                
                audio_files.append({
                    "url": f"/static/audio/{filename}",
                    "name": filename,
                    "size": f"{file_size / 1024:.1f}KB",
                    "duration": duration,
                    "id": filename
                })
        return audio_files
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/subtitle/{audio_id}")
async def get_subtitle(audio_id: str):
    try:
        print(f"Requesting subtitle for audio: {audio_id}")
        
        # 确保文件名格式正确
        base_name = audio_id.replace('.mp3', '')
        subtitle_path = f"static/audio/{base_name}.srt"
        
        print(f"Looking for subtitle file: {subtitle_path}")
        
        # 如果字幕文件不存在，返回404
        if not os.path.exists(subtitle_path):
            print(f"Subtitle file not found: {subtitle_path}")
            raise HTTPException(status_code=404, detail="字幕文件不存在")
        
        # 直接使用 FileResponse，但设置正确的 headers
        return FileResponse(
            path=subtitle_path,
            filename=f"{base_name}.srt",
            headers={
                "Content-Disposition": f'attachment; filename="{base_name}.srt"',
                "Content-Type": "text/srt"
            }
        )
    except Exception as e:
        print(f"Error serving subtitle: {str(e)}")
        if isinstance(e, HTTPException):
            raise
        raise HTTPException(status_code=500, detail=str(e))

# 添加时间格式辅助函数
def format_time(ms):
    """将毫秒转换为 SRT 时间格式 (HH:MM:SS,mmm)"""
    hours = ms // 3600000
    minutes = (ms % 3600000) // 60000
    seconds = (ms % 60000) // 1000
    milliseconds = ms % 1000
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

# 优化文件清理函数
async def cleanup_old_files():
    """清理超过30分钟的音频和字幕文件"""
    while True:
        try:
            logging.info("Starting cleanup check...")
            current_time = time.time()
            audio_dir = "static/audio"
            files_cleaned = 0
            total_size_cleaned = 0
            
            # 获取所有文件及其信息
            files = []
            for filename in os.listdir(audio_dir):
                try:
                    file_path = os.path.join(audio_dir, filename)
                    stat = os.stat(file_path)
                    files.append({
                        'path': file_path,
                        'name': filename,
                        'mtime': stat.st_mtime,
                        'size': stat.st_size
                    })
                except Exception as e:
                    logging.error(f"Error getting file info for {filename}: {str(e)}")
            
            # 按修改时间排序，先删除最旧的文件
            files.sort(key=lambda x: x['mtime'])
            
            for file_info in files:
                try:
                    if current_time - file_info['mtime'] > 30 * 60:  # 30分钟
                        os.remove(file_info['path'])
                        files_cleaned += 1
                        total_size_cleaned += file_info['size']
                        logging.info(f"Cleaned up: {file_info['name']} ({file_info['size'] / 1024:.1f}KB)")
                except Exception as e:
                    logging.error(f"Error deleting file {file_info['name']}: {str(e)}")
            
            if files_cleaned > 0:
                logging.info(f"Cleanup completed: removed {files_cleaned} files, freed {total_size_cleaned / 1024 / 1024:.1f}MB")
            
        except Exception as e:
            logging.error(f"Error during cleanup: {str(e)}", exc_info=True)
        
        await asyncio.sleep(5 * 60)  # 5分钟检查一次

# 修改日志中间件的实现
@app.middleware("http")
async def log_requests(request: Request, call_next):
    try:
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        logging.info(
            f"{request.client.host}:{request.client.port} - "
            f"\"{request.method} {request.url.path} HTTP/{request.scope.get('http_version', '1.1')}\" "
            f"{response.status_code} - {process_time:.2f}s"
        )
        return response
    except Exception as e:
        logging.error(f"Error in request logging: {str(e)}", exc_info=True)
        return await call_next(request)

# 修改错误处理器
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logging.error(
        f"HTTP error: {exc.status_code} - {exc.detail} - "
        f"Path: {request.url.path} - "
        f"Client: {request.client.host}"
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": str(exc.detail)}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logging.error(
        f"Unexpected error: {str(exc)} - "
        f"Path: {request.url.path} - "
        f"Client: {request.client.host}",
        exc_info=True
    )
    return JSONResponse(
        status_code=500,
        content={"message": "服务器内部错误，请稍后重试"}
    )

@app.get("/health")
async def health_check():
    """健康检查接口"""
    try:
        # 检查存储目录
        if not os.path.exists("static/audio"):
            raise Exception("Audio directory not found")
        
        # 检查存储空间
        total, used, free = shutil.disk_usage("/")
        if free < 1024 * 1024 * 100:  # 小于100MB空间时报警
            raise Exception("Low disk space")
        
        # 检查 Edge TTS 服务
        voices = await edge_tts.list_voices()
        if not voices:
            raise Exception("No voices available")
        
        return {
            "status": "healthy",
            "disk_space": {
                "total": f"{total / 1024 / 1024 / 1024:.1f}GB",
                "used": f"{used / 1024 / 1024 / 1024:.1f}GB",
                "free": f"{free / 1024 / 1024 / 1024:.1f}GB"
            },
            "voices_count": len(voices)
        }
    except Exception as e:
        logging.error(f"Health check failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=503, detail=str(e))

# 修改主函数，启动清理任务
if __name__ == "__main__":
    import uvicorn
    
    # 创建清理任务
    @app.on_event("startup")
    async def startup_event():
        asyncio.create_task(cleanup_old_files())
    
    uvicorn.run(app, host="0.0.0.0", port=15009)
