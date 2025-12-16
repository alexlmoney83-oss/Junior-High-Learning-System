"""
AI服务模块数据模型
"""
from django.db import models
from django.contrib.auth.models import User
from apps.courses.models import Course


class PromptTemplate(models.Model):
    """Prompt模板表"""
    
    TEMPLATE_TYPE_CHOICES = [
        ('knowledge_summary', '知识点总结'),
        ('exercise_generation', '练习题生成'),
        ('answer_correction', '答案批改'),
    ]
    
    SUBJECT_CHOICES = [
        ('chinese', '语文'),
        ('math', '数学'),
        ('english', '英语'),
        ('all', '通用'),
    ]
    
    template_type = models.CharField('模板类型', max_length=50, choices=TEMPLATE_TYPE_CHOICES)
    subject = models.CharField('适用学科', max_length=20, choices=SUBJECT_CHOICES)
    template_name = models.CharField('模板名称', max_length=100)
    template_content = models.TextField('模板内容', help_text='支持变量如{course_name}')
    version = models.IntegerField('版本号', default=1)
    is_active = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        db_table = 'ai_services_prompttemplate'
        verbose_name = 'Prompt模板'
        verbose_name_plural = verbose_name
        unique_together = [['template_type', 'subject', 'version']]
        indexes = [
            models.Index(fields=['template_type', 'subject']),
            models.Index(fields=['is_active']),
        ]
    
    def render(self, **kwargs):
        """渲染模板，替换变量"""
        try:
            return self.template_content.format(**kwargs)
        except KeyError as e:
            raise ValueError(f"模板变量缺失: {str(e)}")
    
    def __str__(self):
        return f"{self.template_name} (V{self.version})"


class PromptUsageLog(models.Model):
    """Prompt使用日志表"""
    
    template = models.ForeignKey(PromptTemplate, on_delete=models.CASCADE, verbose_name='模板', related_name='usage_logs')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户', related_name='prompt_logs')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程', related_name='prompt_logs', null=True, blank=True)
    input_data = models.JSONField('输入参数')
    output_data = models.TextField('AI输出结果')
    quality_score = models.IntegerField('质量评分', null=True, blank=True, help_text='1-5分')
    used_at = models.DateTimeField('使用时间', auto_now_add=True)
    
    class Meta:
        db_table = 'ai_services_promptusagelog'
        verbose_name = 'Prompt使用日志'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['template']),
            models.Index(fields=['user']),
            models.Index(fields=['used_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.template.template_name}"

