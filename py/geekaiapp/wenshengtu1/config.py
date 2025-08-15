import os
import logging
from typing import Optional

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('jimeng_api.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class JimengConfig:
    """即梦API配置类"""
    
    def __init__(self):
        # 默认配置
        self.default_api_url = "https://api.jimeng.ai/v1/images/generations"
        self.backup_api_urls = [
            "https://api.jimeng.ai/v1/images/generations",
            "http://api.jimeng.ai/v1/images/generations",  # HTTP备用
        ]
        
        # 请求配置
        self.max_retries = 5
        self.backoff_factor = 2
        self.connect_timeout = 10
        self.read_timeout = 60
        
        # SSL配置
        self.verify_ssl = False
        self.ssl_ciphers = 'DEFAULT@SECLEVEL=1'
        
        # 默认模型参数
        self.default_model = "jimeng-2.1"
        self.default_width = 1080
        self.default_height = 720
        self.default_sample_strength = 0.5
        
        # 用户代理
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    
    def get_headers(self, api_key: str) -> dict:
        """获取请求头"""
        return {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            'User-Agent': self.user_agent,
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
    
    def get_api_urls(self) -> list:
        """获取API URL列表（包含备用）"""
        return self.backup_api_urls
    
    def log_error(self, error: Exception, context: str = ""):
        """记录错误日志"""
        logger.error(f"{context}: {str(error)}", exc_info=True)
    
    def log_info(self, message: str):
        """记录信息日志"""
        logger.info(message)

# 全局配置实例
config = JimengConfig()