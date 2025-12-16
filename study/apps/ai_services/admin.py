"""
AI服务模块Admin配置
"""
from django.contrib import admin
from .models import PromptTemplate, PromptUsageLog


@admin.register(PromptTemplate)
class PromptTemplateAdmin(admin.ModelAdmin):
    list_display = ['id', 'template_name', 'template_type', 'subject', 'version', 'is_active', 'created_at']
    list_filter = ['template_type', 'subject', 'is_active', 'created_at']
    search_fields = ['template_name', 'template_content']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('基本信息', {
            'fields': ('template_type', 'subject', 'template_name', 'version', 'is_active')
        }),
        ('模板内容', {
            'fields': ('template_content',)
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(PromptUsageLog)
class PromptUsageLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'template', 'course', 'quality_score', 'used_at']
    list_filter = ['quality_score', 'used_at']
    search_fields = ['user__username', 'template__template_name']
    readonly_fields = ['used_at']
    
    fieldsets = (
        ('基本信息', {
            'fields': ('user', 'template', 'course', 'quality_score')
        }),
        ('使用数据', {
            'fields': ('input_data', 'output_data')
        }),
        ('时间信息', {
            'fields': ('used_at',)
        })
    )

