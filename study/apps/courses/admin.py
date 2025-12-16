"""
课程模块Admin配置
"""
from django.contrib import admin
from .models import Subject, Course, KnowledgeSummary, StudyProgress


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'code', 'icon', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'code']
    ordering = ['order']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'subject', 'grade', 'course_number', 
                    'difficulty', 'is_active', 'created_at']
    list_filter = ['subject', 'grade', 'difficulty', 'is_active']
    search_fields = ['title', 'keywords']
    ordering = ['subject', 'grade', 'course_number']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('基本信息', {
            'fields': ('subject', 'grade', 'course_number', 'title')
        }),
        ('课程内容', {
            'fields': ('outline', 'keywords', 'cover_image')
        }),
        ('其他设置', {
            'fields': ('difficulty', 'order', 'is_active')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(KnowledgeSummary)
class KnowledgeSummaryAdmin(admin.ModelAdmin):
    list_display = ['id', 'course', 'version', 'generated_at']
    list_filter = ['generated_at']
    search_fields = ['course__title', 'content']
    readonly_fields = ['generated_at']


@admin.register(StudyProgress)
class StudyProgressAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'course', 'status', 'progress', 
                    'study_time', 'last_access']
    list_filter = ['status', 'last_access']
    search_fields = ['user__username', 'course__title']
    readonly_fields = ['created_at', 'last_access']

