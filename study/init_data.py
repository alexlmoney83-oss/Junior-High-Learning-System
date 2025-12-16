#!/usr/bin/env python
"""
初始化基础数据脚本
"""
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'middle_school_system.settings')
django.setup()

from apps.courses.models import Subject

def init_subjects():
    """初始化学科数据"""
    subjects_data = [
        {'name': '语文', 'code': 'chinese', 'icon': '📚', 'description': '初中语文课程', 'order': 1},
        {'name': '数学', 'code': 'math', 'icon': '🔢', 'description': '初中数学课程', 'order': 2},
        {'name': '英语', 'code': 'english', 'icon': '🔤', 'description': '初中英语课程', 'order': 3},
    ]
    
    for data in subjects_data:
        subject, created = Subject.objects.get_or_create(
            code=data['code'],
            defaults=data
        )
        if created:
            print(f"✅ 创建学科: {subject.name}")
        else:
            print(f"ℹ️  学科已存在: {subject.name}")

if __name__ == '__main__':
    print("开始初始化基础数据...")
    init_subjects()
    print("✅ 基础数据初始化完成！")

