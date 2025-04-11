import asyncio
import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
from datetime import timedelta
from pathlib import Path

import edge_tts
from pydub import AudioSegment
# 根据时间戳截取视频片段
from pydub.exceptions import CouldntDecodeError

from cfg import ROOT_DIR, logger

# 所有裁剪的视频片段合并后的原始短视频
CAIJIAN_HEBING = 'cai-hebing.mp4'

# 所有文案配音合并后的原始音频
PEIYIN_HEBING = 'peiyin-hebing.wav'


def create_short_video(video_path, time_list="", srt_str="", role="", pitch="+0Hz", rate="+0%", insert_srt=False):
    # 创建工作目录
    dirname = Path(video_path).parent.as_posix()
    Path(dirname).mkdir(parents=True, exist_ok=True)
    srt_file = f'{dirname}/subtitle.srt'
    with open(srt_file, 'w', encoding='utf-8') as f:
        f.write(srt_str)
    # 根据时间片裁剪多个小片段
    t_list = time_list.strip().split(',')
    file_list = []
    print(f'{t_list=}')
    for i, it in enumerate(t_list):
        tmp = it.split('-')
        s = tmp[0]
        e = tmp[1]
        file_name = f'cai-{i}.mp4'
        file_list.append(f"file '{file_name}'")
        cut_from_video(source=video_path, ss=s, to=e, out=f'{dirname}/{file_name}')
    Path(f'{dirname}/file.txt').write_text('\n'.join(file_list), encoding='utf-8')
    concat_multi_mp4(out=f'{dirname}/{CAIJIAN_HEBING}', concat_txt=f'{dirname}/file.txt')

    # 开始配音
    create_tts(srt_file=srt_file, dirname=dirname, role=role, rate=rate, pitch=pitch, insert_srt=insert_srt)
    try:
        Path(f'{dirname}/file.txt').unlink(missing_ok=True)
    except:
        pass


# 创建配音
def create_tts(*, srt_file, dirname, role="", rate='+0%', pitch="+0Hz", insert_srt=False):
    queue_tts = get_subtitle_from_srt(srt_file, is_file=True)
    logger.info(f'1{queue_tts=}')
    for i, it in enumerate(queue_tts):
        queue_tts[i]['filename'] = f'{dirname}/peiyin-{i}.mp3'
    logger.info(f'2{queue_tts=}')

    def _dubb(it):
        async def _async_dubb(it):
            communicate_task = edge_tts.Communicate(
                text=it["text"],
                voice=role,
                rate=rate,
                proxy=None,
                pitch=pitch)
            await communicate_task.save(it['filename'])

        try:
            asyncio.run(_async_dubb(it))
        except Exception as e:
            print(e)

    split_queue = [queue_tts[i:i + 5] for i in range(0, len(queue_tts), 5)]
    for items in split_queue:
        tasks = []
        for it in items:
            if it['text'].strip():
                tasks.append(threading.Thread(target=_dubb, args=(it,)))
        if len(tasks) < 1:
            continue
        for t in tasks:
            t.start()
        for t in tasks:
            t.join()

    # 连接所有音频片段

    for i, it in enumerate(queue_tts):
        the_ext = it['filename'].split('.')[-1]
        raw = it['end_time'] - it['start_time']
        if i > 0 and it['start_time'] < queue_tts[i - 1]['end_time']:
            diff = queue_tts[i - 1]['end_time'] - it['start_time'] + 50
            it['start_time'] += diff
            it['end_time'] += diff
        # 存在配音文件
        if os.path.exists(it['filename']) and os.path.getsize(it['filename']) > 0:
            try:
                seg_len = len(AudioSegment.from_file(it['filename'], format=the_ext))
                if seg_len > raw:
                    offset = seg_len - raw
                    it['end_time'] += offset
            except CouldntDecodeError:
                pass
        queue_tts[i] = it

    merged_audio = AudioSegment.empty()
    for i, it in enumerate(queue_tts):
        if i == 0:
            if it['start_time'] > 0:
                merged_audio += AudioSegment.silent(duration=it['start_time'])
        else:
            dur = it['start_time'] - queue_tts[i - 1]['end_time'] > 0
            if dur > 0:
                merged_audio += AudioSegment.silent(duration=dur)

        if os.path.isfile(it['filename']) and os.path.getsize(it['filename']) > 0:
            merged_audio += AudioSegment.from_file(it['filename'], format="mp3")
        else:
            merged_audio += AudioSegment.silent(duration=it['end_time'] - it['start_time'])

    srts = []
    for i, it in enumerate(queue_tts):
        srts.append(
            f'{it["line"]}\n{ms_to_time_string(ms=it["start_time"])} --> {ms_to_time_string(ms=it["end_time"])}\n' + it[
                "text"].replace('\n', ''))
    shutil.copy2(dirname + '/subtitle.srt', dirname + '/subtitle00.srt')
    Path(dirname + '/subtitle.srt').write_text('\n\n'.join(srts), encoding='utf-8')
    # 计算时长
    audio_time = len(merged_audio)
    # 获取视频的长度毫秒
    video_time = get_video_ms(f'{dirname}/{CAIJIAN_HEBING}')
    if audio_time < video_time:
        merged_audio += AudioSegment.silent(duration=video_time - audio_time)
    merged_audio.export(f'{dirname}/{PEIYIN_HEBING}', format="wav")
    os.chdir(dirname)
    tmp_wav = f"{dirname}/hunhe-{time.time()}.wav"
    yuan_wav = f'{dirname}/yuan.wav'
    # 1. 准备文件路径
    subtitle_file = Path(dirname) / 'subtitle.srt'
    ass_path = Path(dirname) / 'subtitle.ass'
    # 2. 确保字幕文件存在
    if not subtitle_file.exists():
        raise Exception(f"字幕文件不存在: {subtitle_file}")
    # 3. 将SRT转换为ASS格式（使用更可靠的转换方式）
    runffmpeg([
        '-y',
        '-i', str(subtitle_file).replace('\\', '/'),
        '-f', 'ass',  # 明确指定输出格式
        f'{dirname}/subtitle.ass'
    ])
    # aaaa = 'D\:/cursor/githubs/ai2srt/tmp/share_c1c018a9c572d1c00ec6b22563f9d09d1742791482699-8a6630af16010df0b7815bf96d873b86/subtitle.srt'
    runffmpeg(['-y', '-i', f'{dirname}/{CAIJIAN_HEBING}', '-vn', yuan_wav])
    runffmpeg([
        '-y',
        '-i',
        yuan_wav,
        '-i',
        f'{dirname}/{PEIYIN_HEBING}',
        '-filter_complex',
        "[1:a]apad[a1];[0:a]volume=0.15[a0];[a0][a1]amerge=inputs=2[aout]",
        '-map',
        '[aout]',
        tmp_wav])
    try:
        Path(yuan_wav).unlink(missing_ok=True)
    except:
        pass
    if insert_srt:
        # 软字幕
        # runffmpeg([
        #     "-y",
        #     "-i",
        #     f'{dirname}/{CAIJIAN_HEBING}',
        #     "-i",
        #     f'{tmp_wav}',
        #     "-i",
        #     f'subtitle.srt',
        #     "-map",
        #     "0:v",
        #     "-map",
        #     "1:a",
        #     "-map",
        #     "2:s",
        #     "-c:v",
        #     "copy",
        #     "-c:a",
        #     "aac",
        #     "-c:s",
        #     "mov_text",
        #     "-metadata:s:s:0",
        #     f"language=chi",
        #     '-af',
        #     'volume=1.8',
        #     "-shortest",  # 只处理最短的流（视频或音频）
        #     f'{dirname}/shortvideo.mp4'
        # ])
        # 硬字幕
        runffmpeg([
            '-y',
            '-i', f'{dirname}/{CAIJIAN_HEBING}',
            '-i', tmp_wav,
            '-vf', f'ass=subtitle.ass',
            # '-vf', f'ass={subtitle_file}',
            # '-vf', f'subtitles={aaaa}',
            '-map', '0:v',
            '-map', '1:a',
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-crf', '23',
            '-c:a', 'aac',
            '-af', 'volume=1.8',
            '-shortest',
            f'{dirname}/shortvideo.mp4'
        ])
        # accel_pre = ['ffmpeg',
        #              '-hide_banner',
        #              '-ignore_unknown',
        #              '-vsync',
        #              'vfr',
        #              '-extra_hw_frames',
        #              '2']
        # runffmpeg(accel_pre + [
        #     '-y',
        #     '-i',
        #     f'{dirname}/{CAIJIAN_HEBING}',
        #     '-i',
        #     tmp_wav,
        #     '-c:v',
        #     'libx264',
        #     '-c:a',
        #     'aac',
        #     '-vf',
        #     # f'subtitles={dirname}/subtitle.srt',
        #     # f'subtitles=\'{dirname}/subtitle.srt\'',  # 注意这里的引号
        #     f'ass={dirname}/subtitle.ass',  # 使用ASS格式
        #     f'{dirname}/shortvideo.mp4'
        # ])
    else:
        runffmpeg([
            "-y",
            "-i",
            f'{dirname}/{CAIJIAN_HEBING}',
            "-i",
            f'{tmp_wav}',
            "-map",
            "0:v",
            "-map",
            "1:a",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            '-af',
            'volume=1.8',
            "-shortest",  # 只处理最短的流（视频或音频）
            f'{dirname}/shortvideo.mp4'
        ])
    os.chdir(ROOT_DIR)
    try:
        Path(tmp_wav).unlink(missing_ok=True)
    except:
        pass


def runffprobe(cmd):
    try:
        if Path(cmd[-1]).is_file():
            cmd[-1] = Path(cmd[-1]).as_posix()
        p = subprocess.run(['ffprobe'] + cmd,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           encoding="utf-8",
                           text=True,
                           check=True,
                           creationflags=0 if sys.platform != 'win32' else subprocess.CREATE_NO_WINDOW)
        if p.stdout:
            return p.stdout.strip()
        raise Exception(str(p.stderr))
    except Exception as e:
        raise


# 获取视频信息
def get_video_ms(mp4_file):
    mp4_file = Path(mp4_file).as_posix()
    out = runffprobe(
        ['-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', mp4_file])
    if out is False:
        raise Exception(f'ffprobe error:dont get video information')
    out = json.loads(out)
    if "streams" not in out or len(out["streams"]) < 1:
        raise Exception(f'ffprobe error:streams is 0')

    if "format" in out and out['format']['duration']:
        return int(float(out['format']['duration']) * 1000)
    return 0


# 将字符串做 md5 hash处理
def get_md5(input_string: str):
    md5 = hashlib.md5()
    md5.update(input_string.encode('utf-8'))
    return md5.hexdigest()


# 获取程序执行目录
def _get_executable_path():
    if getattr(sys, 'frozen', False):
        # 如果程序是被“冻结”打包的，使用这个路径
        return Path(sys.executable).parent.as_posix()
    else:
        return Path(__file__).parent.as_posix()


# 将srt文件或合法srt字符串转为字典对象
def get_subtitle_from_srt(srtfile, *, is_file=True):
    def _readfile(file):
        content = ""
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
        except Exception as e:
            try:
                with open(file, 'r', encoding='gbk') as f:
                    content = f.read().strip()
            except Exception as e:
                raise
        return content

    content = ''
    if is_file:
        content = _readfile(srtfile)
    else:
        content = srtfile.strip()

    if len(content) < 1:
        raise Exception(f"srt is empty:{srtfile=},{content=}")

    result = format_srt(content)

    # txt 文件转为一条字幕
    if len(result) < 1:
        result = [
            {"line": 1,
             "time": "00:00:00,000 --> 00:00:02,000",
             "start_time": 0,
             "end_time": 2000,
             "text": "\n".join(content)}
        ]
    return result


'''
格式化毫秒或秒为符合srt格式的 2位小时:2位分:2位秒,3位毫秒 形式
print(ms_to_time_string(ms=12030))
-> 00:00:12,030
'''


def ms_to_time_string(*, ms=0, seconds=None):
    # 计算小时、分钟、秒和毫秒
    if seconds is None:
        td = timedelta(milliseconds=ms)
    else:
        td = timedelta(seconds=seconds)
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = td.microseconds // 1000

    time_string = f"{hours}:{minutes}:{seconds},{milliseconds}"
    return format_time(time_string, ',')


# 将不规范的 时:分:秒,|.毫秒格式为  aa:bb:cc,ddd形式
# eg  001:01:2,4500  01:54,14 等做处理
def format_time(s_time="", separate=','):
    if not s_time.strip():
        return f'00:00:00{separate}000'
    hou, min, sec, ms = 0, 0, 0, 0

    tmp = s_time.strip().split(':')
    if len(tmp) >= 3:
        hou, min, sec = tmp[-3].strip(), tmp[-2].strip(), tmp[-1].strip()
    elif len(tmp) == 2:
        min, sec = tmp[0].strip(), tmp[1].strip()
    elif len(tmp) == 1:
        sec = tmp[0].strip()

    if re.search(r',|\.', str(sec)):
        t = re.split(r',|\.', str(sec))
        sec = t[0].strip()
        ms = t[1].strip()
    else:
        ms = 0
    hou = f'{int(hou):02}'[-2:]
    min = f'{int(min):02}'[-2:]
    sec = f'{int(sec):02}'
    ms = f'{int(ms):03}'[-3:]
    return f"{hou}:{min}:{sec}{separate}{ms}"


# 将 datetime.timedelta 对象的秒和微妙转为毫秒整数值
def toms(td):
    return (td.seconds * 1000) + int(td.microseconds / 1000)


# 将 时:分:秒,毫秒 转为毫秒整数值
def get_ms_from_hmsm(time_str):
    h, m, sec2ms = 0, 0, '00,000'
    tmp0 = time_str.split(":")
    if len(tmp0) == 3:
        h, m, sec2ms = tmp0[0], tmp0[1], tmp0[2]
    elif len(tmp0) == 2:
        m, sec2ms = tmp0[0], tmp0[1]

    tmp = sec2ms.split(',')
    ms = tmp[1] if len(tmp) == 2 else 0
    sec = tmp[0]

    return int(int(h) * 3600000 + int(m) * 60000 + int(sec) * 1000 + int(ms))


# 合法的srt字符串转为 dict list
def srt_str_to_listdict(content):
    import srt
    line = 0
    result = []
    for sub in srt.parse(content):
        line += 1
        it = {
            "start_time": toms(sub.start),
            "end_time": toms(sub.end),
            "line": line,
            "text": sub.content
        }
        it['startraw'] = ms_to_time_string(ms=it['start_time'])
        it['endraw'] = ms_to_time_string(ms=it['end_time'])
        it["time"] = f"{it['startraw']} --> {it['endraw']}"
        result.append(it)
    return result


# 判断是否是srt字符串
def is_srt_string(input_text):
    input_text = input_text.strip()
    if not input_text:
        return False

    # 将文本按换行符切割成列表
    text_lines = input_text.replace("\r", "").splitlines()
    if len(text_lines) < 3:
        return False

    # 正则表达式：第一行应为1到2个纯数字
    first_line_pattern = r'^\d{1,2}$'

    # 正则表达式：第二行符合时间格式
    second_line_pattern = r'^\s*?\d{1,2}:\d{1,2}:\d{1,2}(\W\d+)?\s*-->\s*\d{1,2}:\d{1,2}:\d{1,2}(\W\d+)?\s*$'

    # 如果前两行符合条件，返回原字符串
    if not re.match(first_line_pattern, text_lines[0].strip()) or not re.match(second_line_pattern,
                                                                               text_lines[1].strip()):
        return False
    return True


# 将普通文本转为合法的srt字符串
def process_text_to_srt_str(input_text: str):
    if is_srt_string(input_text):
        return input_text

    # 将文本按换行符切割成列表
    text_lines = [line.strip() for line in input_text.replace("\r", "").splitlines() if line.strip()]

    # 分割大于50个字符的行
    text_str_list = []
    for line in text_lines:
        if len(line) > 50:
            # 按标点符号分割为多个字符串
            split_lines = re.split(r'[,.，。]', line)
            text_str_list.extend([l.strip() for l in split_lines if l.strip()])
        else:
            text_str_list.append(line)
    # 创建字幕字典对象列表
    dict_list = []
    start_time_in_seconds = 0  # 初始时间，单位秒

    for i, text in enumerate(text_str_list, start=1):
        # 计算开始时间和结束时间（每次增加1s）
        start_time = ms_to_time_string(seconds=start_time_in_seconds)
        end_time = ms_to_time_string(seconds=start_time_in_seconds + 1)
        start_time_in_seconds += 1

        # 创建字幕字典对象
        srt = f"{i}\n{start_time} --> {end_time}\n{text}"
        dict_list.append(srt)

    return "\n\n".join(dict_list)


# 将字符串或者字幕文件内容，格式化为有效字幕数组对象
# 格式化为有效的srt格式
def format_srt(content):
    result = []
    try:
        result = srt_str_to_listdict(content)
    except Exception:
        result = srt_str_to_listdict(process_text_to_srt_str(content))
    return result


# 将字幕字典列表写入srt文件
def save_srt(srt_list, srt_file):
    txt = get_srt_from_list(srt_list)
    with open(srt_file, "w", encoding="utf-8") as f:
        f.write(txt)
    return True


def get_current_time_as_yymmddhhmmss(format='hms'):
    """将当前时间转换为 YYMMDDHHmmss 格式的字符串。"""
    now = datetime.datetime.now()
    return now.strftime("%y%m%d%H%M%S" if format != 'hms' else "%H%M%S")


# 从 字幕 对象中获取 srt 字幕串
def get_srt_from_list(srt_list):
    txt = ""
    line = 0
    # it中可能含有完整时间戳 it['time']   00:00:01,123 --> 00:00:12,345
    # 开始和结束时间戳  it['startraw']=00:00:01,123  it['endraw']=00:00:12,345
    # 开始和结束毫秒数值  it['start_time']=126 it['end_time']=678
    for it in srt_list:
        line += 1
        if "startraw" not in it:
            # 存在完整开始和结束时间戳字符串 时:分:秒,毫秒 --> 时:分:秒,毫秒
            if 'time' in it:
                startraw, endraw = it['time'].strip().split(" --> ")
                startraw = format_time(startraw.strip().replace('.', ','), ',')
                endraw = format_time(endraw.strip().replace('.', ','), ',')
            elif 'start_time' in it and 'end_time' in it:
                # 存在开始结束毫秒数值
                startraw = ms_to_time_string(ms=it['start_time'])
                endraw = ms_to_time_string(ms=it['end_time'])
            else:
                raise Exception(
                    f'字幕中不存在 time/startraw/start_time 任何有效时间戳形式')
        else:
            # 存在单独开始和结束  时:分:秒,毫秒 字符串
            startraw = it['startraw']
            endraw = it['endraw']
        txt += f"{line}\n{startraw} --> {endraw}\n{it['text']}\n\n"
    return txt


def runffmpeg(cmd):
    import subprocess
    try:
        if cmd[0] != 'ffmpeg':
            cmd.insert(0, 'ffmpeg')
        logger.info(f'{cmd=}')
        subprocess.run(cmd,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE,
                       encoding="utf-8",
                       check=True,
                       text=True,
                       creationflags=0 if sys.platform != 'win32' else subprocess.CREATE_NO_WINDOW)

    except Exception as e:
        raise Exception(str(e.stderr) if hasattr(e, 'stderr') and e.stderr else f'执行Ffmpeg操作失败:{cmd=}')
    return True


# 从视频中切出一段时间的视频片段 cuda + h264_cuvid
def cut_from_video(*, ss="", to="", source="", out=""):
    cmd1 = [
        "-y",
        "-ss",
        format_time(ss, '.')]
    if to != '':
        cmd1.append("-to")
        cmd1.append(format_time(to, '.'))  # 如果开始结束时间相同，则强制持续时间1s)
    cmd1.append('-i')
    cmd1.append(source)

    cmd = cmd1 + [f'{out}']
    return runffmpeg(cmd)


# 创建 多个连接文件
def create_concat_txt(filelist, concat_txt=None):
    txt = []
    for it in filelist:
        if not Path(it).exists() or Path(it).stat().st_size == 0:
            continue
        txt.append(f"file '{os.path.basename(it)}'")
    if len(txt) < 1:
        raise Exception(f'file list no vail')
    with Path(concat_txt).open('w', encoding='utf-8') as f:
        f.write("\n".join(txt))
        f.flush()
    return concat_txt


# 多个视频片段连接 cuda + h264_cuvid
def concat_multi_mp4(*, out=None, concat_txt=None):
    os.chdir(os.path.dirname(concat_txt))
    runffmpeg(
        # ['-y', '-f', 'concat', '-i', concat_txt,  '-vf', "subtitles={subtitle.srt}:force_style='Fontsize=24,PrimaryColour=&HFFFFFF&'", '-c:v',  f"libx264",  out])
        ['-y', '-f', 'concat', '-i', concat_txt, '-c:v', f"libx264", out])
    os.chdir(ROOT_DIR)
    return True


def precise_speed_up_audio(*, file_path=None, target_duration_ms=120000, max_rate=100):
    from pydub import AudioSegment
    audio = AudioSegment.from_file(file_path)

    # 首先确保原时长和目标时长单位一致（毫秒）
    current_duration_ms = len(audio)
    # 计算音频变速比例
    # current_duration_ms = len(audio)
    # speedup_ratio = current_duration_ms / target_duration_ms
    # 计算速度变化率
    speedup_ratio = current_duration_ms / target_duration_ms

    if target_duration_ms <= 0 or speedup_ratio <= 1:
        return True
    rate = min(max_rate, speedup_ratio)
    # 变速处理
    try:
        fast_audio = audio.speedup(playback_speed=rate)
        # 如果处理后的音频时长稍长于目标时长，进行剪裁
        if len(fast_audio) > target_duration_ms:
            fast_audio = fast_audio[:target_duration_ms]
    except Exception:
        fast_audio = audio[:target_duration_ms]

    fast_audio.export(file_path, format=file_path.split('.')[-1])
    # 返回速度调整后的音频
    return True
