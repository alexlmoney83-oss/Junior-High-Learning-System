"""
用户模块序列化器
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from .models import UserProfile, AIConfig


class UserProfileSerializer(serializers.ModelSerializer):
    """用户资料序列化器"""
    
    class Meta:
        model = UserProfile
        fields = ['phone', 'school', 'grade', 'avatar', 'total_study_hours', 
                  'continuous_days', 'created_at', 'updated_at']
        read_only_fields = ['total_study_hours', 'continuous_days', 
                           'created_at', 'updated_at']


class AIConfigSerializer(serializers.ModelSerializer):
    """AI配置序列化器（不包含API Key）"""
    
    class Meta:
        model = AIConfig
        fields = ['model_type', 'api_endpoint']


class UserDetailSerializer(serializers.ModelSerializer):
    """用户详情序列化器"""
    profile = UserProfileSerializer(read_only=True)
    aiconfig = AIConfigSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined', 'profile', 'aiconfig']
        read_only_fields = ['id', 'date_joined']


class UserRegisterSerializer(serializers.Serializer):
    """用户注册序列化器"""
    username = serializers.CharField(max_length=150, min_length=3)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    phone = serializers.CharField(max_length=11, required=False, allow_blank=True)
    school = serializers.CharField(max_length=100, required=False, allow_blank=True)
    grade = serializers.ChoiceField(choices=UserProfile.GRADE_CHOICES)
    
    def validate_username(self, value):
        """验证用户名唯一性"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("用户名已存在")
        return value
    
    def validate_email(self, value):
        """验证邮箱唯一性"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("邮箱已被注册")
        return value
    
    def validate(self, attrs):
        """验证密码一致性"""
        if attrs['password'] != attrs.get('password_confirm'):
            raise serializers.ValidationError({"password_confirm": "两次输入的密码不一致"})
        
        # Django密码强度验证
        try:
            validate_password(attrs['password'])
        except DjangoValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        
        return attrs
    
    def create(self, validated_data):
        """创建用户"""
        validated_data.pop('password_confirm')
        phone = validated_data.pop('phone', None)
        school = validated_data.pop('school', '')
        grade = validated_data.pop('grade')
        
        # 创建用户
        user = User.objects.create_user(**validated_data)
        
        # 创建用户资料
        UserProfile.objects.create(
            user=user,
            phone=phone,
            school=school if school else '',  # 如果没有提供学校，使用空字符串
            grade=grade
        )
        
        return user


class UserLoginSerializer(serializers.Serializer):
    """用户登录序列化器"""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class ChangePasswordSerializer(serializers.Serializer):
    """修改密码序列化器"""
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)
    new_password_confirm = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        """验证密码"""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({"new_password_confirm": "两次输入的密码不一致"})
        
        # Django密码强度验证
        try:
            validate_password(attrs['new_password'])
        except DjangoValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})
        
        return attrs


class SaveAIConfigSerializer(serializers.Serializer):
    """保存AI配置序列化器"""
    model_type = serializers.ChoiceField(choices=AIConfig.MODEL_TYPE_CHOICES)
    api_key = serializers.CharField(write_only=True)
    api_endpoint = serializers.URLField(required=False, allow_blank=True)


class TestAIConnectionSerializer(serializers.Serializer):
    """测试AI连接序列化器"""
    model_type = serializers.ChoiceField(choices=AIConfig.MODEL_TYPE_CHOICES)
    api_key = serializers.CharField()
    api_endpoint = serializers.URLField(required=False, allow_blank=True)

