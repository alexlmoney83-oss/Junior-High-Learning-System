"""
用户模块Admin配置
"""
from django.contrib import admin
from .models import UserProfile, AIConfig


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'school', 'grade', 'total_study_hours', 'continuous_days', 'created_at']
    list_filter = ['grade', 'school', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('基本信息', {
            'fields': ('user', 'phone', 'school', 'grade', 'avatar')
        }),
        ('学习统计', {
            'fields': ('total_study_hours', 'continuous_days')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(AIConfig)
class AIConfigAdmin(admin.ModelAdmin):
    list_display = ['user', 'model_type', 'api_endpoint', 'created_at']
    list_filter = ['model_type', 'created_at']
    search_fields = ['user__username']
    readonly_fields = ['created_at', 'updated_at', 'encrypted_api_key']
    
    fieldsets = (
        ('配置信息', {
            'fields': ('user', 'model_type', 'api_endpoint')
        }),
        ('密钥信息', {
            'fields': ('encrypted_api_key',),
            'classes': ('collapse',)
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

