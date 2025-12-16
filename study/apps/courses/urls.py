"""
课程模块URL配置
"""
from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    # 学科
    path('subjects/', views.get_subjects, name='subjects'),
    
    # 课程
    path('courses/', views.get_courses, name='courses'),
    path('courses/<int:course_id>/', views.get_course_detail, name='course-detail'),
    
    # 知识点总结
    path('courses/<int:course_id>/summary/', views.get_knowledge_summary, name='knowledge-summary'),
    path('courses/<int:course_id>/generate-summary/', views.generate_knowledge_summary, name='generate-summary'),
    
    # 学习进度
    path('study-progress/', views.get_study_progress, name='study-progress'),
    path('study-progress/<int:course_id>/', views.update_study_progress, name='update-progress'),
]

