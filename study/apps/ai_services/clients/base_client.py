"""
AI客户端基类
"""
from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseAIClient(ABC):
    """AI客户端基类"""
    
    def __init__(self, api_key: str, api_endpoint: str = None):
        self.api_key = api_key
        self.api_endpoint = api_endpoint
    
    @abstractmethod
    def call_api(self, prompt: str, **kwargs) -> str:
        """
        调用AI API
        
        Args:
            prompt: 提示词
            **kwargs: 其他参数
            
        Returns:
            AI生成的文本
        """
        pass
    
    @abstractmethod
    def test_connection(self) -> Dict[str, Any]:
        """
        测试API连接
        
        Returns:
            测试结果字典
        """
        pass
    
    def generate_summary(self, prompt: str) -> str:
        """生成知识点总结"""
        return self.call_api(prompt)
    
    def generate_exercises(self, prompt: str) -> str:
        """生成练习题"""
        return self.call_api(prompt)
    
    def correct_answer(self, prompt: str) -> str:
        """批改答案"""
        return self.call_api(prompt)

