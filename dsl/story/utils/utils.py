import json
import locale
import os
import random
import re
import string
import threading
import urllib3
from typing import Any, List
from uuid import uuid4
from pathlib import Path

from loguru import logger

from models import const

urllib3.disable_warnings()


def get_uuid(remove_hyphen: bool = False):
    u = str(uuid4())
    if remove_hyphen:
        u = u.replace("-", "")
    return u


def get_root_dir():
    return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def resource_dir(sub_dir: str = ""):
    d = os.path.join(get_root_dir(), "resource")
    if sub_dir:
        d = os.path.join(d, sub_dir)
    return d

def task_dir(sub_dir: str = "") -> str:
    """获取任务目录路径
    Args:
        sub_dir (str, optional): 子目录名. Defaults to "".
    Returns:
        str: 任务目录的绝对路径
    """
    # 获取 backend 目录
    root_dir = get_root_dir()
    # 任务目录
    d = os.path.join(root_dir, "tasks")
    if sub_dir:
        d = os.path.join(d, sub_dir)
    
    # 确保目录存在
    os.makedirs(d, exist_ok=True)
    
    return d


def font_dir(sub_dir: str = ""):
    d = resource_dir("fonts")
    if sub_dir:
        d = os.path.join(d, sub_dir)
    if not os.path.exists(d):
        os.makedirs(d)
    return d


def song_dir(sub_dir: str = ""):
    d = resource_dir("songs")
    if sub_dir:
        d = os.path.join(d, sub_dir)
    if not os.path.exists(d):
        os.makedirs(d)
    return d


def public_dir(sub_dir: str = ""):
    d = resource_dir("public")
    if sub_dir:
        d = os.path.join(d, sub_dir)
    if not os.path.exists(d):
        os.makedirs(d)
    return d


def run_in_background(func, *args, **kwargs):
    def run():
        try:
            func(*args, **kwargs)
        except Exception as e:
            logger.error(f"run_in_background error: {e}")

    thread = threading.Thread(target=run)
    thread.start()
    return thread


def time_convert_seconds_to_hmsm(seconds) -> str:
    hours = int(seconds // 3600)
    seconds = seconds % 3600
    minutes = int(seconds // 60)
    milliseconds = int(seconds * 1000) % 1000
    seconds = int(seconds % 60)
    return "{:02d}:{:02d}:{:02d},{:03d}".format(hours, minutes, seconds, milliseconds)


def text_to_srt(idx: int, msg: str, start_time: float, end_time: float) -> str:
    start_time = time_convert_seconds_to_hmsm(start_time)
    end_time = time_convert_seconds_to_hmsm(end_time)
    srt = """%d
%s --> %s
%s
        """ % (
        idx,
        start_time,
        end_time,
        msg,
    )
    return srt


def str_contains_punctuation(word):
    for p in const.PUNCTUATIONS:
        if p in word:
            return True
    return False


def split_string_by_punctuations(s):
    result = []
    txt = ""

    previous_char = ""
    next_char = ""
    for i in range(len(s)):
        char = s[i]
        if char == "\n":
            result.append(txt.strip())
            txt = ""
            continue

        if i > 0:
            previous_char = s[i - 1]
        if i < len(s) - 1:
            next_char = s[i + 1]

        if char == "." and previous_char.isdigit() and next_char.isdigit():
            # # In the case of "withdraw 10,000, charged at 2.5% fee", the dot in "2.5" should not be treated as a line break marker
            txt += char
            continue

        if char not in const.PUNCTUATIONS:
            txt += char
        else:
            result.append(txt.strip())
            txt = ""
    result.append(txt.strip())
    # filter empty string
    result = list(filter(None, result))
    return result


def split_string_by_punctuations_new(text: str) -> List[str]:
    """按标点符号分割文本"""
    result = []
    txt = ""

    previous_char = ""
    next_char = ""
    for i in range(len(text)):
        char = text[i]
        if char == "\n":
            if txt.strip():
                result.append(txt.strip())
            txt = ""
            continue

        if i > 0:
            previous_char = text[i - 1]
        if i < len(text) - 1:
            next_char = text[i + 1]

        if char == "." and previous_char.isdigit() and next_char.isdigit():
            txt += char
            continue

        if char not in [".", "。", "！", "？", "...", "…"]:
            txt += char
        else:
            txt += char
            if txt.strip():
                result.append(txt.strip())
            txt = ""

    if txt.strip():
        result.append(txt.strip())
    return result


def random_str(length: int = 8) -> str:
    """生成随机字符串"""
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))


def md5(text):
    import hashlib

    return hashlib.md5(text.encode("utf-8")).hexdigest()


def get_system_locale():
    try:
        loc = locale.getdefaultlocale()
        # zh_CN, zh_TW return zh
        # en_US, en_GB return en
        language_code = loc[0].split("_")[0]
        return language_code
    except Exception:
        return "en"


def load_locales(i18n_dir):
    _locales = {}
    for root, dirs, files in os.walk(i18n_dir):
        for file in files:
            if file.endswith(".json"):
                lang = file.split(".")[0]
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    _locales[lang] = json.loads(f.read())
    return _locales


def parse_extension(filename):
    return os.path.splitext(filename)[1].strip().lower().replace(".", "")

def extract_id(video_file: str) -> str:
    """
    从路径中提取 ID（tasks 目录下的第一级子目录名）
    兼容 Windows 和 Linux
    """
    path = Path(video_file)

    # 遍历路径的所有部分，查找 "tasks" 目录
    try:
        parts = path.parts
        index = parts.index("tasks")  # 找到 "tasks" 目录的位置
        return parts[index + 1]  # 返回紧跟其后的部分作为 ID
    except (ValueError, IndexError):
        raise ValueError(f"Invalid path format: {video_file}")
