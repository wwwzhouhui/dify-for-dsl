"""
GeminiAI翻译字幕与转录音视频

@author https://pyvideotrans.com
"""
import traceback
from pathlib import Path

from waitress import serve

HOST = '127.0.0.1'
HOST2 = '192.168.2.2'
PORT = 15012
API_KEY = 'AIzaSyDLV1CQQaIKETwIgrhQtu1Wn0B7nSgCS9U'
PROXY = 'http://127.0.0.1:7897'

import re, os

import socket

import google.generativeai as genai

from google.api_core.exceptions import ServerError, TooManyRequests, RetryError

from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import threading, webbrowser, time
from google.generativeai.types import RequestOptions
from google.api_core import retry

import json
from cfg import ROOT_DIR, TMP_DIR, logger, safetySettings
import tools

app = Flask(__name__, template_folder=f'{ROOT_DIR}/templates', static_folder=os.path.join(ROOT_DIR, 'tmp'),
            static_url_path='/tmp')
CORS(app)


@app.route('/tmp/<path:filename>')
def static_files(filename):
    return send_from_directory(app.config['STATIC_FOLDER'], filename)


with open(ROOT_DIR + "/prompt.json", 'r', encoding='utf-8') as f:
    PROMPT_LIST = json.loads(f.read())


class Gemini():

    def __init__(self, *, language=None, text="", api_key="AIzaSyDLV1CQQaIKETwIgrhQtu1Wn0B7nSgCS9U",
                 model_name='gemini-1.5-flash', piliang=50, waitsec=10,
                 audio_file=None):
        self.language = language

        self.srt_text = text
        self.api_key = api_key
        self.model_name = model_name
        self.piliang = piliang
        self.waitsec = waitsec
        self.audio_file = audio_file

    # 三步反思翻译srt字幕
    def run_trans(self):
        text_list = tools.get_subtitle_from_srt(self.srt_text, is_file=False)
        split_source_text = [text_list[i:i + self.piliang] for i in range(0, len(text_list), self.piliang)]

        genai.configure(api_key=self.api_key)
        model = genai.GenerativeModel(self.model_name, safety_settings=safetySettings)

        result_str = ""
        req_nums = len(split_source_text)
        print(f'\n本次翻译将分 {req_nums} 次发送请求,每次发送 {self.piliang} 条字幕,可在 logs 目录下查看日志')
        for i, it in enumerate(split_source_text):
            srt_str = "\n\n".join(
                [f"{srtinfo['line']}\n{srtinfo['time']}\n{srtinfo['text'].strip()}" for srtinfo in it])
            response = None

            try:
                prompt = PROMPT_LIST['prompt_trans'].replace('{lang}', self.language).replace('<INPUT></INPUT>',
                                                                                              f'<INPUT>{srt_str}</INPUT>')

                print(f'开始发送请求 {i=}')
                response = model.generate_content(
                    prompt,
                    safety_settings=safetySettings
                )
                logger.info(f'\n[Gemini]返回:{response.text=}')
                result_it = self._extract_text_from_tag(response.text)
                if not result_it:
                    start_line = i * self.piliang + 1
                    msg = (f"{start_line}->{(start_line + len(it))}行翻译结果出错{response.text}")
                    logger.error(msg)
                    result_str += msg.strip() + "\n\n"
                    continue
                result_str += result_it.strip() + "\n\n"
            except (ServerError, RetryError, socket.timeout) as e:
                error = '无法连接到Gemini,请尝试使用或更换代理'
                raise Exception(error)
            except TooManyRequests as e:
                raise Exception('429请求太频繁')
            except Exception as e:
                error = str(e)
                if response and response.prompt_feedback.block_reason:
                    raise Exception(self._get_error(response.prompt_feedback.block_reason, "forbid"))

                if error.find('User location is not supported') > -1 or error.find('time out') > -1:
                    raise Exception("当前请求ip(或代理服务器)所在国家不在Gemini API允许范围")

                if response and len(response.candidates) > 0 and response.candidates[0].finish_reason not in [0, 1]:
                    raise Exception(self._get_error(response.candidates[0].finish_reason))

                if response and len(response.candidates) > 0 and response.candidates[0].finish_reason == 1 and \
                        response.candidates[0].content and response.candidates[0].content.parts:
                    result_it = self._extract_text_from_tag(response.text)
                    if not result_it:
                        raise Exception(f"翻译结果出错{response.text}")
                    result_str += result_it.strip() + "\n\n"
                    continue
                raise
            finally:
                if i < req_nums - 1:
                    print(f'请求 {i=} 结束，防止 429 错误， 暂停 {self.waitsec}s 后继续下次请求')
                    time.sleep(self.waitsec)
        print(f'翻译结束\n\n')
        return result_str

    # 转录音视频为字幕
    def run_recogn(self):
        tmpname = f'{TMP_DIR}/{time.time()}.mp3'
        tools.runffmpeg(['ffmpeg', '-y', '-i', self.audio_file, '-ac', '1', '-ar', '8000', tmpname])
        self.audio_file = tmpname
        prompt = PROMPT_LIST['prompt_recogn']
        if self.language:
            prompt += PROMPT_LIST['prompt_recogn_trans'].replace('{lang}', self.language)

        result = []
        while 1:
            try:
                genai.configure(api_key=self.api_key)
                model = genai.GenerativeModel(
                    self.model_name,
                    safety_settings=safetySettings
                )

                sample_audio = genai.upload_file(self.audio_file)
                response = model.generate_content([prompt, sample_audio], request_options={"timeout": 600})
                res_str = response.text.strip()

                logger.info(res_str)
                recogn_res = re.search(r'<RECONGITION>(.*)</RECONGITION>', res_str, re.I | re.S)
                if recogn_res:
                    result.append(recogn_res.group(1))

                trans_res = re.search(r'<TRANSLATE>(.*)</TRANSLATE>', res_str, re.I | re.S)
                if trans_res:
                    result.append(trans_res.group(1))
                if not result:
                    raise Exception('结果为空')
                return result
            except (ServerError, RetryError, socket.timeout) as e:
                error = '无法连接到Gemini,请尝试使用或更换代理'
                raise Exception(error)
            except TooManyRequests as e:
                print('429请求太频繁，暂停60s后重试')
                time.sleep(60)
                continue
            except Exception as e:
                raise
            finally:
                try:
                    Path(self.audio_file).unlink(missing_ok=True)
                except:
                    pass

    # 总结视频
    def run_zongjie(self):
        tmpname = f'{TMP_DIR}/{time.time()}.mp4'
        tools.runffmpeg(
            ['ffmpeg', '-y', '-i', self.audio_file, '-c:v', 'libx265', '-ac', '1', '-ar', '16000', '-preset',
             'superfast', tmpname])
        self.audio_file = tmpname
        prompt = PROMPT_LIST['prompt_zongjie']
        result = ""
        while 1:
            try:
                genai.configure(api_key=self.api_key)
                model = genai.GenerativeModel(
                    self.model_name,
                    safety_settings=safetySettings
                )

                sample_audio = genai.upload_file(self.audio_file)
                while sample_audio.state.name == "PROCESSING":
                    print('.', end='')
                    time.sleep(10)
                    sample_audio = genai.get_file(sample_audio.name)
                chat_session = model.start_chat(
                    history=[
                        {
                            "role": "user",
                            "parts": [
                                sample_audio,
                            ],
                        }
                    ])
                response = chat_session.send_message(
                    prompt,
                    request_options=RequestOptions(
                        retry=retry.Retry(initial=10, multiplier=2, maximum=60, timeout=900),
                        timeout=900
                    )
                )
                return response.text.strip()
            except (ServerError, RetryError, socket.timeout) as e:
                error = '无法连接到Gemini,请尝试使用或更换代理'
                raise Exception(error)
            except TooManyRequests as e:
                raise Exception('429请求太频繁')
            except Exception as e:
                raise
            finally:
                try:
                    Path(self.audio_file).unlink(missing_ok=True)
                except:
                    pass

    def run_jieshuo(self):
        tmpname = f'{TMP_DIR}/{time.time()}.mp4'
        tools.runffmpeg(
            ['ffmpeg', '-y', '-i', self.audio_file, '-c:v', 'libx265', '-ac', '1', '-ar', '16000', '-preset',
             'superfast', tmpname])
        self.audio_file = tmpname
        prompt = PROMPT_LIST['prompt_jieshuo']
        result = {"timelist": [], "srt": ""}
        while 1:
            try:
                genai.configure(api_key=self.api_key)
                model = genai.GenerativeModel(
                    self.model_name,
                    safety_settings=safetySettings
                )

                sample_audio = genai.upload_file(self.audio_file)
                while sample_audio.state.name == "PROCESSING":
                    print('.', end='')
                    time.sleep(10)
                    sample_audio = genai.get_file(sample_audio.name)
                chat_session = model.start_chat(
                    history=[
                        {
                            "role": "user",
                            "parts": [
                                sample_audio,
                            ],
                        }
                    ])
                response = chat_session.send_message(
                    prompt,
                    request_options=RequestOptions(
                        retry=retry.Retry(initial=10, multiplier=2, maximum=60, timeout=900),
                        timeout=900
                    )
                )

                res_str = response.text.strip()

                logger.info(res_str)
                time_1 = re.search(r'<TIME>\**?(.*)\**?</TIME>', res_str, re.I | re.S)
                if time_1:
                    result['timelist'] = time_1.group(1).strip()

                srt_2 = re.search(r'<SRT>\**?(.*)\**?</SRT>', res_str, re.I | re.S)
                if srt_2:
                    result["srt"] = srt_2.group(1).strip()
                if not result:
                    raise Exception('结果为空')
                return result
            except (ServerError, RetryError, socket.timeout) as e:
                error = '无法连接到Gemini,请尝试使用或更换代理'
                raise Exception(error)
            except TooManyRequests as e:
                raise Exception('429请求太频繁')
            except Exception as e:
                raise
            finally:
                try:
                    Path(self.audio_file).unlink(missing_ok=True)
                except:
                    pass

    def _extract_text_from_tag(self, text):
        match = re.search(r'<step3_refined_translation>(.*?)</step3_refined_translation>', text, re.S)
        if match:
            return match.group(1)
        else:
            return ""

    def _get_error(self, num=5, type='error'):
        REASON_CN = {
            2: "超出长度",
            3: "安全限制",
            4: "文字过度重复",
            5: "其他原因"
        }
        forbid_cn = {
            1: "被Gemini禁止翻译:出于安全考虑，提示已被屏蔽",
            2: "被Gemini禁止翻译:由于未知原因，提示已被屏蔽"
        }
        return REASON_CN[num] if type == 'error' else forbid_cn[num]


@app.route('/')
def index():
    return render_template(
        'index.html',
        prompt_trans=PROMPT_LIST['prompt_trans'],
        prompt_recogn=PROMPT_LIST['prompt_recogn'],
        prompt_recogn_trans=PROMPT_LIST['prompt_recogn_trans'],
        prompt_jieshuo=PROMPT_LIST['prompt_jieshuo'],
        prompt_zongjie=PROMPT_LIST['prompt_zongjie'],
    )


@app.route('/update_prompt', methods=['POST'])
def update_prompt():
    global PROMPT_LIST
    id = request.form.get('id')
    text = request.form.get('value')
    PROMPT_LIST[id] = text
    with open(ROOT_DIR + "/prompt.json", 'w', encoding='utf-8') as f:
        f.write(json.dumps(PROMPT_LIST, ensure_ascii=False))
    return jsonify({"code": 0, "msg": "ok"})


@app.route('/upload', methods=['POST'])
def upload():
    try:
        if 'audio' not in request.files:  # 检查是否上传了文件
            return jsonify({"code": 1, 'msg': 'No file part'})

        file = request.files['audio']
        if file.filename == '':  # 检查是否选择了文件
            return jsonify({"code": 1, 'msg': 'No selected file'})

        # 获取文件扩展名
        file_ext = os.path.splitext(file.filename)[1]
        name = re.sub(r'["\'?,\[\]{}()`!@#$%\^&*+=\\;:><，。、？：；“”‘’—｛（）｝·|~]', '_', file.filename)
        # 使用时间戳生成文件名
        filename = f'{TMP_DIR}/{time.time()}{file_ext}'
        file.save(filename)
        return jsonify({'code': 0, 'msg': 'ok', 'data': filename})
    except Exception as e:
        return jsonify({"code": 1, 'msg': str(e)})


@app.route('/upload_video', methods=['POST'])
def upload_video():
    try:
        if 'audio' not in request.files:  # 检查是否上传了文件
            return jsonify({"code": 1, 'msg': 'No file part'})

        file = request.files['audio']
        if file.filename == '':  # 检查是否选择了文件
            return jsonify({"code": 1, 'msg': 'No selected file'})

        # 获取文件扩展名
        name, file_ext = os.path.splitext(file.filename)
        name = re.sub(r'["\'?,\[\]{}()`!@#$%\^&*+=\\;:><，。、？：；“”‘’—｛（）｝·|~ \s]', '_', name.strip())
        # 使用时间戳生成文件名
        filename = name + "-" + tools.get_md5(file.filename)
        # 创建目录
        target_dir = TMP_DIR + f'/{filename}'
        Path(target_dir).mkdir(parents=True, exist_ok=True)
        file.save(f'{target_dir}/raw{file_ext}')
        # 保存文件到 /tmp 目录
        if file_ext.lower() != '.mp4':
            tools.runffmpeg(['-y', '-i', f'{target_dir}/raw{file_ext}', '-c:v', 'copy', f'{target_dir}/raw.mp4'])
        return jsonify({'code': 0, 'msg': 'ok', 'data': f'{target_dir}/raw.mp4'})
    except Exception as e:
        return jsonify({"code": 1, 'msg': str(e)})


def _checkparam(rate='0', pitch='0'):
    try:
        pitch = int(pitch)
        pitch = f'+{pitch}' if pitch >= 0 else pitch
    except:
        pitch = '+0'
    pitch = f'{pitch}Hz'

    try:
        rate = int(rate)
        rate = f'+{rate}' if rate >= 0 else rate
    except:
        rate = '+0'
    rate = f'{rate}%'
    return rate, pitch


@app.route('/zongjie', methods=['POST'])
def zongjie():
    data = request.get_json()
    model_name = data.get('model_name')
    api_key = data.get('api_key', API_KEY)
    proxy = data.get('proxy', PROXY)
    video_file = data.get('video_file')

    if not all([api_key]):  # Include audio_filename in the check
        api_key = API_KEY
        # return jsonify({"code": 1, "msg": "必须输入api_key"})
    if not video_file:
        return jsonify({"code": 2, "msg": "视频文件必须要上传"})

    if proxy:
        os.environ['https_proxy'] = proxy
    try:
        task = Gemini(model_name=model_name, api_key=api_key, audio_file=video_file)
        result = task.run_zongjie()
        if not result:
            return jsonify({"code": 3, "msg": '无总结文本生成'})

        return jsonify({"code": 0, "msg": "ok", "data": result})
    except Exception as e:
        logger.exception(e, exc_info=True)
        return jsonify({"code": 2, "msg": str(e)})


@app.route('/jieshuo', methods=['POST'])
def jieshuo():
    data = request.get_json()
    model_name = data.get('model_name')
    api_key = data.get('api_key')
    proxy = data.get('proxy', PROXY)
    video_file = data.get('video_file')
    role = data.get('role')
    rate = data.get('rate', 0)
    pitch = data.get('pitch', 0)
    autoend = int(data.get('autoend', 0))
    rate, pitch = _checkparam(rate, pitch)
    insert_srt = int(data.get('insert', 0))

    if not all([api_key]):  # Include audio_filename in the check
        api_key = API_KEY
        # return jsonify({"code": 1, "msg": "必须输入api_key"})
    if not video_file:
        return jsonify({"code": 2, "msg": "视频文件必须要上传"})

    if proxy:
        os.environ['https_proxy'] = proxy
    try:

        task = Gemini(model_name=model_name, api_key=api_key, audio_file=video_file)
        result = task.run_jieshuo()
        if not result:
            return jsonify({"code": 3, "msg": '无解说文案生成'})
        if autoend != 1:
            return jsonify({"code": 0, "msg": "ok", "data": result})

            # 开始根据时间戳截取视频
        tools.create_short_video(
            video_path=video_file,
            time_list=result['timelist'],
            srt_str=result['srt'],
            role=role,
            pitch=pitch,
            rate=rate,
            insert_srt=insert_srt
        )
        # 开始根据字幕配音
        video_url = '/tmp/' + str(Path(video_file).parent.stem) + '/shortvideo.mp4'
        print(f'完成 {video_url=}')
        return jsonify({"code": 0, "msg": "ok", "data": result, "url": video_url})
    except Exception as e:
        logger.exception(e, exc_info=True)
        return jsonify({"code": 2, "msg": str(e)})


@app.route('/gocreate', methods=['POST'])
def gocreate():
    # 开始根据时间戳截取视频
    data = request.get_json()
    timelist = data.get('timelist')
    srt = data.get('srt')
    video_file = data.get('video_file')
    role = data.get('role')
    insert_srt = int(data.get('insert', 0))
    pitch = data.get('pitch', 0)
    rate = data.get('rate', 0)
    rate, pitch = _checkparam(rate, pitch)
    print(f'{rate=},{pitch=}')
    try:
        tools.create_short_video(
            video_path=video_file,
            time_list=timelist,
            srt_str=srt,
            role=role,
            pitch=pitch,
            rate=rate,
            insert_srt=insert_srt
        )
        # 开始根据字幕配音
        video_url = '/tmp/' + str(Path(video_file).parent.stem) + '/shortvideo.mp4'
        print('完成')
        return jsonify({"code": 0, "msg": "ok", "url": video_url})
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({"code": 1, "msg": str(e)})


@app.route('/api', methods=['POST'])
def api():
    data = request.get_json()
    text = data.get('text')
    language = data.get('language')
    model_name = data.get('model_name')
    api_key = data.get('api_key', API_KEY)
    proxy = data.get('proxy', PROXY)
    audio_file = data.get('audio_file')

    if not all([api_key]):  # Include audio_filename in the check
        api_key = API_KEY
        # return jsonify({"code": 1, "msg": "必须输入api_key"})
    if not text and not audio_file:
        return jsonify({"code": 2, "msg": "srt字幕文件和音视频文件必须要选择一个"})

    if proxy:
        os.environ['https_proxy'] = proxy
    try:
        # logger.info(f'[API] 请求数据 {data=}')
        if text:
            task = Gemini(text=text, language=language, model_name=model_name, api_key=api_key)
            result = task.run_trans()
            if not result:
                return jsonify({"code": 3, "msg": '无翻译结果'})
            return jsonify({"code": 0, "msg": "ok", "data": result})
        # 视频转录
        task = Gemini(text='', language=None if not language or language == '' else language, model_name=model_name,
                      api_key=api_key, audio_file=audio_file)
        result = task.run_recogn()
        if not result:
            return jsonify({"code": 3, "msg": '没有识别出字幕'})
        return jsonify({"code": 0, "msg": "ok", "data": result})
    except Exception as e:
        logger.exception(e, exc_info=True)
        return jsonify({"code": 2, "msg": str(e)})


def openurl(url):
    def op():
        time.sleep(5)
        try:

            webbrowser.open_new_tab(url)
        except:
            pass

    threading.Thread(target=op).start()


if __name__ == '__main__':
    # uvicorn.run(app, host="0.0.0.0", port=PORT)
    try:
        print(f"api接口地址  http://{HOST}:{PORT}")
        # openurl(f'http://{HOST}:{PORT}')
        # serve(app, host=HOST, port=PORT)
        serve(app, host="0.0.0.0", port=PORT)
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        logger.error(traceback.format_exc())
