"""
API密钥加密工具
"""
from cryptography.fernet import Fernet
from django.conf import settings


class APIKeyEncryption:
    """API密钥加密工具类"""
    
    def __init__(self):
        # 从环境变量获取加密密钥
        key = settings.ENCRYPTION_KEY
        if not key:
            # 如果没有配置，生成一个临时密钥（仅用于开发）
            key = Fernet.generate_key().decode()
        
        if isinstance(key, str):
            key = key.encode()
        
        self.cipher = Fernet(key)
    
    def encrypt(self, plain_text: str) -> str:
        """
        加密文本
        
        Args:
            plain_text: 明文
            
        Returns:
            加密后的密文（字符串格式）
        """
        if not plain_text:
            return ''
        encrypted = self.cipher.encrypt(plain_text.encode())
        return encrypted.decode()
    
    def decrypt(self, encrypted_text: str) -> str:
        """
        解密文本
        
        Args:
            encrypted_text: 密文
            
        Returns:
            解密后的明文
        """
        if not encrypted_text:
            return ''
        decrypted = self.cipher.decrypt(encrypted_text.encode())
        return decrypted.decode()

