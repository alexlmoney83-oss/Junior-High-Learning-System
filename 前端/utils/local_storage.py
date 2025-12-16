"""
本地持久化存储模块
用于保存登录状态和API配置
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
import hashlib


class LocalStorage:
    """本地存储管理器"""
    
    def __init__(self):
        # 存储目录：用户主目录/.streamlit_learning_system/
        self.storage_dir = Path.home() / '.streamlit_learning_system'
        self.storage_dir.mkdir(exist_ok=True)
        
        self.auth_file = self.storage_dir / 'auth.json'
        self.config_file = self.storage_dir / 'config.json'
    
    # ==================== 认证相关 ====================
    
    def save_auth(self, username: str, remember_days: int = 7):
        """保存登录状态"""
        auth_data = {
            'username': username,
            'login_time': datetime.now().isoformat(),
            'expire_time': (datetime.now() + timedelta(days=remember_days)).isoformat(),
            'token': self._generate_token(username)
        }
        
        try:
            with open(self.auth_file, 'w', encoding='utf-8') as f:
                json.dump(auth_data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存登录状态失败: {e}")
            return False
    
    def load_auth(self):
        """加载登录状态"""
        if not self.auth_file.exists():
            return None
        
        try:
            with open(self.auth_file, 'r', encoding='utf-8') as f:
                auth_data = json.load(f)
            
            # 检查是否过期
            expire_time = datetime.fromisoformat(auth_data['expire_time'])
            if datetime.now() > expire_time:
                # 已过期，删除文件
                self.clear_auth()
                return None
            
            return auth_data
        except Exception as e:
            print(f"加载登录状态失败: {e}")
            return None
    
    def clear_auth(self):
        """清除登录状态"""
        try:
            if self.auth_file.exists():
                self.auth_file.unlink()
            return True
        except Exception as e:
            print(f"清除登录状态失败: {e}")
            return False
    
    def is_authenticated(self):
        """检查是否已登录且未过期"""
        auth_data = self.load_auth()
        return auth_data is not None
    
    # ==================== AI配置相关 ====================
    
    def save_ai_config(self, api_key: str, model: str, endpoint: str = None):
        """保存AI配置"""
        config_data = {
            'api_key': api_key,
            'model': model,
            'endpoint': endpoint,
            'saved_time': datetime.now().isoformat()
        }
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存AI配置失败: {e}")
            return False
    
    def load_ai_config(self):
        """加载AI配置"""
        if not self.config_file.exists():
            return None
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            return config_data
        except Exception as e:
            print(f"加载AI配置失败: {e}")
            return None
    
    def clear_ai_config(self):
        """清除AI配置"""
        try:
            if self.config_file.exists():
                self.config_file.unlink()
            return True
        except Exception as e:
            print(f"清除AI配置失败: {e}")
            return False
    
    # ==================== 工具方法 ====================
    
    def _generate_token(self, username: str) -> str:
        """生成简单的token"""
        timestamp = datetime.now().isoformat()
        raw = f"{username}:{timestamp}:learning_system"
        return hashlib.sha256(raw.encode()).hexdigest()
    
    def clear_all(self):
        """清除所有本地存储"""
        self.clear_auth()
        self.clear_ai_config()


# 全局实例
_storage = None

def get_local_storage() -> LocalStorage:
    """获取本地存储实例（单例）"""
    global _storage
    if _storage is None:
        _storage = LocalStorage()
    return _storage


def load_api_config_to_session():
    """
    从本地存储加载API配置到session_state
    在每个需要使用API的页面调用此函数
    """
    import streamlit as st
    
    # 如果session_state中已经有API Key，不需要重新加载
    if st.session_state.get('api_key'):
        return True
    
    # 从本地存储加载
    storage = get_local_storage()
    config_data = storage.load_ai_config()
    
    if config_data:
        st.session_state['api_key'] = config_data['api_key']
        st.session_state['api_model'] = config_data['model']
        st.session_state['api_endpoint'] = config_data.get('endpoint')
        return True
    
    return False

