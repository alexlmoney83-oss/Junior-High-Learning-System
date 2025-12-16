"""
用户模块视图
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from utils.response import APIResponse
from .models import UserProfile, AIConfig
from .serializers import (
    UserDetailSerializer, UserRegisterSerializer, UserLoginSerializer,
    UserProfileSerializer, ChangePasswordSerializer, SaveAIConfigSerializer,
    TestAIConnectionSerializer, AIConfigSerializer
)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """用户注册"""
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return APIResponse.created({
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'grade': user.profile.grade
        }, message="注册成功")
    return APIResponse.error("注册失败", errors=serializer.errors)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """用户登录"""
    serializer = UserLoginSerializer(data=request.data)
    if not serializer.is_valid():
        return APIResponse.error("参数错误", errors=serializer.errors)
    
    username = serializer.validated_data['username']
    password = serializer.validated_data['password']
    
    # 认证用户
    user = authenticate(username=username, password=password)
    if not user:
        return APIResponse.error("用户名或密码错误", code=401)
    
    # 生成JWT token
    refresh = RefreshToken.for_user(user)
    
    # 获取用户资料
    try:
        profile = user.profile
        avatar = profile.avatar.url if profile.avatar else None
    except UserProfile.DoesNotExist:
        # 如果用户资料不存在，创建一个默认的
        profile = UserProfile.objects.create(user=user, grade='grade1')
        avatar = None
    
    return APIResponse.success({
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
        'grade': profile.grade,
        'avatar': avatar,
        'access_token': str(refresh.access_token),
        'refresh_token': str(refresh),
        'expires_in': 86400  # 1天
    }, message="登录成功")


@api_view(['POST'])
@permission_classes([AllowAny])
def token_refresh(request):
    """刷新Token"""
    refresh_token = request.data.get('refresh_token')
    if not refresh_token:
        return APIResponse.error("缺少refresh_token参数")
    
    try:
        refresh = RefreshToken(refresh_token)
        return APIResponse.success({
            'access_token': str(refresh.access_token),
            'expires_in': 86400
        }, message="Token刷新成功")
    except Exception as e:
        return APIResponse.error(f"Token刷新失败: {str(e)}", code=401)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    """获取用户信息"""
    user = request.user
    
    # 获取用户资料
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user, grade='grade1')
    
    # 获取AI配置
    ai_config_data = None
    try:
        ai_config = user.aiconfig
        ai_config_data = {
            'model_type': ai_config.model_type,
            'api_endpoint': ai_config.api_endpoint
        }
    except AIConfig.DoesNotExist:
        pass
    
    data = {
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
        'phone': profile.phone,
        'school': profile.school,
        'grade': profile.grade,
        'avatar': profile.avatar.url if profile.avatar else None,
        'total_study_hours': profile.total_study_hours,
        'continuous_days': profile.continuous_days,
        'created_at': user.date_joined.isoformat(),
        'ai_config': ai_config_data
    }
    
    return APIResponse.success(data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """更新用户信息"""
    user = request.user
    
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user, grade='grade1')
    
    serializer = UserProfileSerializer(profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return APIResponse.success({
            'user_id': user.id,
            'phone': profile.phone,
            'school': profile.school,
            'avatar': profile.avatar.url if profile.avatar else None
        }, message="更新成功")
    return APIResponse.error("更新失败", errors=serializer.errors)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """修改密码"""
    serializer = ChangePasswordSerializer(data=request.data)
    if not serializer.is_valid():
        return APIResponse.error("参数错误", errors=serializer.errors)
    
    user = request.user
    old_password = serializer.validated_data['old_password']
    new_password = serializer.validated_data['new_password']
    
    # 验证旧密码
    if not user.check_password(old_password):
        return APIResponse.error("原密码错误")
    
    # 设置新密码
    user.set_password(new_password)
    user.save()
    
    return APIResponse.success(message="密码修改成功")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_ai_config(request):
    """保存AI配置"""
    serializer = SaveAIConfigSerializer(data=request.data)
    if not serializer.is_valid():
        return APIResponse.error("参数错误", errors=serializer.errors)
    
    user = request.user
    model_type = serializer.validated_data['model_type']
    api_key = serializer.validated_data['api_key']
    api_endpoint = serializer.validated_data.get('api_endpoint', '')
    
    # 创建或更新AI配置
    ai_config, created = AIConfig.objects.get_or_create(user=user)
    ai_config.model_type = model_type
    ai_config.set_api_key(api_key)
    ai_config.api_endpoint = api_endpoint
    ai_config.save()
    
    return APIResponse.success({
        'model_type': ai_config.model_type,
        'api_endpoint': ai_config.api_endpoint,
        'is_configured': True
    }, message="AI配置保存成功")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def test_ai_connection(request):
    """测试AI连接"""
    serializer = TestAIConnectionSerializer(data=request.data)
    if not serializer.is_valid():
        return APIResponse.error("参数错误", errors=serializer.errors)
    
    # TODO: 实际测试AI连接的逻辑
    # 这里先返回模拟数据
    model_type = serializer.validated_data['model_type']
    
    return APIResponse.success({
        'status': 'success',
        'model': model_type,
        'test_message': f'成功连接到 {model_type} 模型'
    }, message="AI连接测试成功")

