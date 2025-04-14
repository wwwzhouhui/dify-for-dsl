from enum import Enum

class StoryType(str, Enum):
    """故事类型"""
    custom = "custom"  # 自定义故事
    bedtime = "bedtime"  # 睡前故事
    fairy_tale = "fairy_tale"  # 童话故事
    adventure = "adventure"  # 冒险故事
    science = "science"  # 科普故事
    moral = "moral"  # 寓言故事

class ImageStyle(str, Enum):
    """图片风格"""
    realistic = "realistic"  # 写实风格
    cartoon = "cartoon"  # 卡通风格
    watercolor = "watercolor"  # 水彩风格
    oil_painting = "oil_painting"  # 油画风格

class Language(str, Enum):
    """支持的语言"""
    CHINESE_CN = "zh-CN"      # 中文（简体）
    CHINESE_TW = "zh-TW"      # 中文（繁体）
    ENGLISH_US = "en-US"      # 英语（美国）
    JAPANESE = "ja-JP"        # 日语
    KOREAN = "ko-KR"          # 韩语

# 语言名称映射
LANGUAGE_NAMES = {
    Language.CHINESE_CN: "中文（简体）",
    Language.CHINESE_TW: "中文（繁体）",
    Language.ENGLISH_US: "English",
    Language.JAPANESE: "日本語",
    Language.KOREAN: "한국어"
}

PUNCTUATIONS = [
    "?",
    ",",
    ".",
    "、",
    ";",
    ":",
    "!",
    "…",
    "？",
    "，",
    "。",
    "、",
    "；",
    "：",
    "！",
    "...",
]

TASK_STATE_FAILED = -1
TASK_STATE_COMPLETE = 1
TASK_STATE_PROCESSING = 4

FILE_TYPE_VIDEOS = ["mp4", "mov", "mkv", "webm"]
FILE_TYPE_IMAGES = ["jpg", "jpeg", "png", "bmp"]
