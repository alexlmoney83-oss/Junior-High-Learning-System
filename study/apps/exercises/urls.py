"""
练习题模块URL配置
"""
from django.urls import path
from . import views

app_name = 'exercises'

urlpatterns = [
    # 练习题
    path('exercises/', views.get_exercises, name='exercises'),
    path('generate/', views.generate_exercises, name='generate'),
    
    # 答题
    path('submit/', views.submit_answer, name='submit'),
    path('batch-submit/', views.batch_submit_answers, name='batch-submit'),
    
    # 答题记录和统计
    path('records/', views.get_answer_records, name='records'),
    path('statistics/', views.get_statistics, name='statistics'),
    
    # AI判题
    path('ai-check/', views.ai_check_answer, name='ai-check'),
]

