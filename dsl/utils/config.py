import configparser
import json
import os



def common_config(config_file='config.ini'):
    config = configparser.ConfigParser()
    config.read(config_file,encoding='utf-8')
    config_data = {}
    config_data['region'] = config.get('common', 'region')
    config_data['secret_id'] = config.get('common', 'secret_id')
    config_data['secret_key'] = config.get('common', 'secret_key')
    config_data['bucket'] = config.get('common', 'bucket')
    return config_data

# Load 302 config
def load_302_config(config_file='config.ini'):
    config = configparser.ConfigParser()
    config.read(config_file,encoding='utf-8')
    config_data = {}
    config_data['api_key'] = config.get('302', 'api_key')
    return config_data

# Load siliconflow config
def load_siliconflow_config(config_file='siliconflow/config.json'):
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config

# Load difyforgitee config
def load_difyforgitee_config(config_file='config.ini'):
    config = configparser.ConfigParser()
    config.read(config_file, encoding='utf-8')
    config_data = {}
    config_data['api_key'] = config.get('gitee', 'api_key')
    config_data['output_path'] = config.get('gitee', 'output_path')
    config_data['textprompt'] = config.get('gitee', 'textprompt')
    config_data['imageprompt'] = config.get('gitee', 'imageprompt')
    config_data['audiourl'] = config.get('AudioService', 'url')
    config_data['package_id'] = config.get('AudioService', 'package_id')
    config_data['model'] = config.get('AudioService', 'model')
    return config_data

# Load jimeng config
def load_jimeng_config(config_file='config.ini'):
    config = configparser.ConfigParser()
    config.read(config_file,encoding='utf-8')
    config_data = {}
    config_data['image_generation_url'] = config.get('jimeng', 'image_generation_url')
    config_data['audio_generation_url'] = config.get('jimeng', 'audio_generation_url')
    config_data['image_api_key'] = config.get('jimeng', 'image_api_key')
    config_data['audio_model'] = config.get('jimeng', 'audio_model')
    config_data['audio_voice'] = config.get('jimeng', 'audio_voice')
    config_data['tts_model'] = config.get('jimeng', 'tts_model')
    config_data['tts_voice'] = config.get('jimeng', 'tts_voice')
    config_data['speed'] = config.get('jimeng', 'speed')
    config_data['response_format'] = config.get('jimeng', 'response_format')
    return config_data

# Load bizyair config
def load_bizyair_config(config_file='config.ini'):
    config = configparser.ConfigParser()
    config.read(config_file, encoding='utf-8')
    config_data = {}
    config_data['output_path'] = config.get('bizyair', 'output_path')
    config_data['workflowfile'] = config.get('bizyair', 'workflowfile')
    config_data['comfyui_endpoit'] = config.get('bizyair', 'comfyui_endpoit')
    return config_data

def load_edgetts_config(config_file='config.ini'):
    config = configparser.ConfigParser()
    config.read(config_file, encoding='utf-8')
    config_data = {}
    config_data['openai_api_key'] = config.get('edgetts', 'openai_api_key')
    config_data['openai_base_url'] = config.get('edgetts', 'openai_base_url')
    config_data['output_path'] = config.get('edgetts', 'output_path')
    return config_data
