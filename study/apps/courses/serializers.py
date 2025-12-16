"""
课程模块序列化器
"""
from rest_framework import serializers
from .models import Subject, Course, KnowledgeSummary, StudyProgress


class SubjectSerializer(serializers.ModelSerializer):
    """学科序列化器"""
    
    class Meta:
        model = Subject
        fields = ['id', 'name', 'code', 'icon', 'description', 'order']


class CourseListSerializer(serializers.ModelSerializer):
    """课程列表序列化器"""
    subject = SubjectSerializer(read_only=True)
    grade_display = serializers.CharField(source='get_grade_display', read_only=True)
    difficulty_display = serializers.CharField(source='get_difficulty_display', read_only=True)
    
    class Meta:
        model = Course
        fields = ['id', 'subject', 'grade', 'grade_display', 'course_number', 
                  'title', 'outline', 'keywords', 'cover_image', 'difficulty', 
                  'difficulty_display', 'is_active', 'created_at']


class CourseDetailSerializer(serializers.ModelSerializer):
    """课程详情序列化器"""
    subject = SubjectSerializer(read_only=True)
    grade_display = serializers.CharField(source='get_grade_display', read_only=True)
    difficulty_display = serializers.CharField(source='get_difficulty_display', read_only=True)
    has_summary = serializers.SerializerMethodField()
    has_content = serializers.SerializerMethodField()
    exercises_count = serializers.SerializerMethodField()
    user_progress = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = ['id', 'subject', 'grade', 'grade_display', 'course_number', 
                  'title', 'outline', 'keywords', 'cover_image', 'difficulty', 
                  'difficulty_display', 'is_active', 'created_at', 'has_summary',
                  'has_content', 'content', 'pdf_source', 'pdf_page_range',
                  'exercises_count', 'user_progress']
    
    def get_has_summary(self, obj):
        """是否有知识点总结"""
        return obj.summaries.exists()
    
    def get_has_content(self, obj):
        """是否有课本内容"""
        return bool(obj.content and obj.content.strip())
    
    def get_exercises_count(self, obj):
        """练习题数量"""
        return obj.exercises.count()
    
    def get_user_progress(self, obj):
        """用户学习进度"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                progress = StudyProgress.objects.get(user=request.user, course=obj)
                return {
                    'status': progress.status,
                    'progress': progress.progress,
                    'study_time': progress.study_time,
                    'last_access': progress.last_access.isoformat()
                }
            except StudyProgress.DoesNotExist:
                return None
        return None


class KnowledgeSummarySerializer(serializers.ModelSerializer):
    """知识点总结序列化器"""
    
    class Meta:
        model = KnowledgeSummary
        fields = ['id', 'course', 'content', 'generated_at', 'version']
        read_only_fields = ['generated_at']


class StudyProgressSerializer(serializers.ModelSerializer):
    """学习进度序列化器"""
    course_title = serializers.CharField(source='course.title', read_only=True)
    subject_name = serializers.CharField(source='course.subject.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = StudyProgress
        fields = ['id', 'course', 'course_title', 'subject_name', 'status', 
                  'status_display', 'progress', 'study_time', 'last_access', 'created_at']
        read_only_fields = ['created_at', 'last_access']


class UpdateStudyProgressSerializer(serializers.Serializer):
    """更新学习进度序列化器"""
    status = serializers.ChoiceField(choices=StudyProgress.STATUS_CHOICES, required=False)
    progress = serializers.IntegerField(min_value=0, max_value=100, required=False)
    study_time = serializers.IntegerField(min_value=0, required=False)

