"""
练习题模块数据模型
"""
from django.db import models
from django.contrib.auth.models import User
from apps.courses.models import Course


class Exercise(models.Model):
    """练习题表"""
    
    QUESTION_TYPE_CHOICES = [
        ('choice', '选择题'),
        ('fill', '填空题'),
        ('short_answer', '简答题'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('basic', '基础'),
        ('medium', '中等'),
        ('advanced', '拓展'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程', related_name='exercises')
    question_type = models.CharField('题型', max_length=20, choices=QUESTION_TYPE_CHOICES)
    question_text = models.TextField('题目内容')
    options = models.JSONField('选项', null=True, blank=True, help_text='选择题选项，JSON格式')
    answer = models.TextField('标准答案')
    explanation = models.TextField('答案解析')
    difficulty = models.CharField('难度', max_length=20, choices=DIFFICULTY_CHOICES)
    is_ai_generated = models.BooleanField('是否AI生成', default=False)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        db_table = 'exercises_exercise'
        verbose_name = '练习题'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['course']),
            models.Index(fields=['question_type']),
            models.Index(fields=['difficulty']),
        ]
    
    def __str__(self):
        return f"{self.course.title} - {self.get_question_type_display()}"


class AnswerRecord(models.Model):
    """答题记录表"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户', related_name='answer_records')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, verbose_name='题目', related_name='answer_records')
    user_answer = models.TextField('用户答案')
    is_correct = models.BooleanField('是否正确', null=True, blank=True)
    score = models.IntegerField('得分', null=True, blank=True, help_text='0-100')
    ai_feedback = models.TextField('AI批改反馈', blank=True)
    time_spent = models.IntegerField('答题耗时', default=0, help_text='秒')
    submitted_at = models.DateTimeField('提交时间', auto_now_add=True)
    
    class Meta:
        db_table = 'exercises_answerrecord'
        verbose_name = '答题记录'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['user', 'exercise']),
            models.Index(fields=['submitted_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.exercise.question_text[:30]}"

