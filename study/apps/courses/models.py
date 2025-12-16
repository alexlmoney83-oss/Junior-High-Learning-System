"""
课程模块数据模型
"""
from django.db import models
from django.contrib.auth.models import User


class Subject(models.Model):
    """学科表"""
    
    CODE_CHOICES = [
        ('chinese', '语文'),
        ('math', '数学'),
        ('english', '英语'),
    ]
    
    name = models.CharField('学科名称', max_length=50)
    code = models.CharField('学科代码', max_length=20, unique=True, choices=CODE_CHOICES)
    icon = models.CharField('学科图标', max_length=100, blank=True)
    description = models.TextField('学科描述', blank=True)
    order = models.IntegerField('排序序号', default=0)
    is_active = models.BooleanField('是否启用', default=True)
    
    class Meta:
        db_table = 'courses_subject'
        verbose_name = '学科'
        verbose_name_plural = verbose_name
        ordering = ['order']
    
    def __str__(self):
        return self.name


class Course(models.Model):
    """课程表"""
    
    GRADE_CHOICES = [
        ('grade1', '初一'),
        ('grade2', '初二'),
        ('grade3', '初三'),
    ]
    
    SEMESTER_CHOICES = [
        ('first', '上学期'),
        ('second', '下学期'),
        ('all', '全学年'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('easy', '基础'),
        ('medium', '进阶'),
        ('hard', '提高'),
    ]
    
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='学科', related_name='courses')
    grade = models.CharField('年级', max_length=20, choices=GRADE_CHOICES)
    semester = models.CharField('学期', max_length=20, choices=SEMESTER_CHOICES, default='all')
    course_number = models.IntegerField('课程序号')
    title = models.CharField('课程标题', max_length=200)
    outline = models.TextField('课程大纲')
    keywords = models.CharField('关键词', max_length=500, blank=True, help_text='逗号分隔')
    cover_image = models.ImageField('封面图片', upload_to='courses/', blank=True, null=True)
    difficulty = models.CharField('难度级别', max_length=20, choices=DIFFICULTY_CHOICES)
    order = models.IntegerField('排序序号', default=0)
    is_active = models.BooleanField('是否启用', default=True)
    
    # PDF相关字段
    content = models.TextField('章节内容', blank=True, help_text='从PDF提取的课本实际文字内容，供AI参考')
    pdf_page_range = models.CharField('PDF页码范围', max_length=50, blank=True, help_text='如：18-50')
    pdf_source = models.CharField('PDF来源', max_length=500, blank=True, help_text='原始PDF文件名')
    
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        db_table = 'courses_course'
        verbose_name = '课程'
        verbose_name_plural = verbose_name
        ordering = ['subject', 'grade', 'course_number']
        unique_together = [['subject', 'grade', 'semester', 'course_number']]
        indexes = [
            models.Index(fields=['subject', 'grade']),
            models.Index(fields=['course_number']),
        ]
    
    def __str__(self):
        return f"{self.get_grade_display()} {self.subject.name} - {self.title}"


class KnowledgeSummary(models.Model):
    """知识点总结表"""
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程', related_name='summaries')
    content = models.TextField('知识点总结内容')
    generated_at = models.DateTimeField('生成时间', auto_now_add=True)
    version = models.IntegerField('版本号', default=1)
    
    class Meta:
        db_table = 'courses_knowledgesummary'
        verbose_name = '知识点总结'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['course']),
            models.Index(fields=['version']),
        ]
    
    def __str__(self):
        return f"{self.course.title} - 知识点总结 V{self.version}"


class StudyProgress(models.Model):
    """学习进度表"""
    
    STATUS_CHOICES = [
        ('not_started', '未开始'),
        ('in_progress', '学习中'),
        ('completed', '已完成'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户', related_name='study_progress')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程', related_name='progress_records')
    status = models.CharField('学习状态', max_length=20, choices=STATUS_CHOICES, default='not_started')
    progress = models.IntegerField('进度', default=0, help_text='0-100')
    study_time = models.IntegerField('学习时长', default=0, help_text='秒')
    last_access = models.DateTimeField('最后访问时间', auto_now=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    
    class Meta:
        db_table = 'courses_studyprogress'
        verbose_name = '学习进度'
        verbose_name_plural = verbose_name
        unique_together = [['user', 'course']]
        indexes = [
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.course.title}"

