"""
练习题模块Admin配置
"""
from django.contrib import admin
from .models import Exercise, AnswerRecord


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['id', 'course', 'question_type', 'difficulty', 'is_ai_generated', 'created_at']
    list_filter = ['question_type', 'difficulty', 'is_ai_generated', 'created_at']
    search_fields = ['question_text', 'course__title']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('基本信息', {
            'fields': ('course', 'question_type', 'difficulty', 'is_ai_generated')
        }),
        ('题目内容', {
            'fields': ('question_text', 'options', 'answer', 'explanation')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(AnswerRecord)
class AnswerRecordAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'exercise', 'is_correct', 'score', 'time_spent', 'submitted_at']
    list_filter = ['is_correct', 'submitted_at']
    search_fields = ['user__username', 'exercise__question_text']
    readonly_fields = ['submitted_at']
    
    fieldsets = (
        ('基本信息', {
            'fields': ('user', 'exercise', 'user_answer')
        }),
        ('批改结果', {
            'fields': ('is_correct', 'score', 'ai_feedback')
        }),
        ('其他信息', {
            'fields': ('time_spent', 'submitted_at')
        })
    )

