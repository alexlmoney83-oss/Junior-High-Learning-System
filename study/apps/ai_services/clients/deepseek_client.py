"""
DeepSeek AI客户端
"""
import requests
import json
from .base_client import BaseAIClient


class DeepSeekClient(BaseAIClient):
    """DeepSeek AI客户端"""
    
    def __init__(self, api_key: str, api_endpoint: str = None, model: str = None):
        super().__init__(api_key, api_endpoint)
        self.api_endpoint = api_endpoint or "https://api.deepseek.com"
        # 支持多种DeepSeek模型：deepseek-chat, deepseek-reasoner
        self.model = model or "deepseek-chat"
    
    def call_api(self, prompt: str, **kwargs) -> str:
        """
        调用DeepSeek API
        
        Args:
            prompt: 提示词
            **kwargs: temperature, max_tokens等参数
            
        Returns:
            AI生成的文本
        """
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': self.model,
            'messages': [
                {
                    'role': 'system',
                    'content': '你是一位资深的上海市初中教师。'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            'temperature': kwargs.get('temperature', 0.7),
            'max_tokens': kwargs.get('max_tokens', 4000)  # 增加到4000，支持长知识点总结
        }
        
        try:
            response = requests.post(
                f'{self.api_endpoint}/v1/chat/completions',
                headers=headers,
                json=data,
                timeout=120  # 增加到120秒，处理长文本
            )
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content']
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"DeepSeek API调用失败: {str(e)}")
    
    def test_connection(self) -> dict:
        """测试DeepSeek API连接"""
        try:
            result = self.call_api("你好", max_tokens=50)
            return {
                'status': 'success',
                'model': self.model,
                'test_message': result
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

