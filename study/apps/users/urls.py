"""
用户模块URL配置
"""
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # 认证相关
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('token/refresh/', views.token_refresh, name='token-refresh'),
    
    # 用户信息
    path('profile/', views.get_profile, name='get-profile'),
    path('profile/update/', views.update_profile, name='update-profile'),
    path('change-password/', views.change_password, name='change-password'),
    
    # AI配置
    path('ai-config/', views.save_ai_config, name='save-ai-config'),
    path('test-ai-connection/', views.test_ai_connection, name='test-ai-connection'),
]

