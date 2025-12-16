"""
用户模块数据模型
"""
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from utils.encryption import APIKeyEncryption
from utils.validators import validate_phone


class UserProfile(models.Model):
    """用户扩展信息表"""
    
    GRADE_CHOICES = [
        ('grade1', '初一'),
        ('grade2', '初二'),
        ('grade3', '初三'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户', related_name='profile')
    phone = models.CharField('手机号', max_length=11, unique=True, null=True, blank=True, validators=[validate_phone])
    school = models.CharField('学校名称', max_length=100, default=settings.DEFAULT_SCHOOL)
    grade = models.CharField('年级', max_length=20, choices=GRADE_CHOICES)
    avatar = models.ImageField('头像', upload_to='avatars/', null=True, blank=True)
    total_study_hours = models.IntegerField('总学习时长(秒)', default=0)
    continuous_days = models.IntegerField('连续学习天数', default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        db_table = 'users_userprofile'
        verbose_name = '用户资料'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['grade']),
        ]
    
    def __str__(self):
        return f"{self.user.username}的资料"


class AIConfig(models.Model):
    """AI配置表"""
    
    MODEL_TYPE_CHOICES = [
        ('deepseek-r1', 'DeepSeek-R1'),
        ('gpt-4', 'GPT-4'),
        ('gpt-4-turbo', 'GPT-4 Turbo'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户', related_name='aiconfig')
    model_type = models.CharField('模型类型', max_length=50, choices=MODEL_TYPE_CHOICES)
    encrypted_api_key = models.TextField('加密的API Key')
    api_endpoint = models.URLField('API端点', max_length=255, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        db_table = 'users_aiconfig'
        verbose_name = 'AI配置'
        verbose_name_plural = verbose_name
    
    def set_api_key(self, api_key):
        """加密存储API Key"""
        encryption = APIKeyEncryption()
        self.encrypted_api_key = encryption.encrypt(api_key)
    
    def get_api_key(self):
        """解密获取API Key"""
        if not self.encrypted_api_key:
            return ''
        encryption = APIKeyEncryption()
        return encryption.decrypt(self.encrypted_api_key)
    
    def __str__(self):
        return f"{self.user.username}的AI配置"

