"""
课程模块视图
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, Count, Sum
from utils.response import APIResponse
from .models import Subject, Course, KnowledgeSummary, StudyProgress
from .serializers import (
    SubjectSerializer, CourseListSerializer, CourseDetailSerializer,
    KnowledgeSummarySerializer, StudyProgressSerializer, UpdateStudyProgressSerializer
)
from apps.ai_services.clients.deepseek_client import DeepSeekClient
from apps.ai_services.clients.openai_client import OpenAIClient
from apps.ai_services.prompt_manager import PromptManager


@api_view(['GET'])
@permission_classes([AllowAny])
def get_subjects(request):
    """获取学科列表"""
    subjects = Subject.objects.filter(is_active=True).order_by('order')
    serializer = SubjectSerializer(subjects, many=True)
    return APIResponse.success(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_courses(request):
    """获取课程列表"""
    # 获取查询参数
    subject_id = request.query_params.get('subject_id')
    subject_code = request.query_params.get('subject')  # 支持学科代码
    grade = request.query_params.get('grade')
    difficulty = request.query_params.get('difficulty')
    
    # 构建查询
    queryset = Course.objects.filter(is_active=True)
    
    # 支持通过学科ID或学科代码筛选
    if subject_id:
        queryset = queryset.filter(subject_id=subject_id)
    elif subject_code:
        queryset = queryset.filter(subject__code=subject_code)
    
    if grade:
        queryset = queryset.filter(grade=grade)
    if difficulty:
        queryset = queryset.filter(difficulty=difficulty)
    
    # 分页
    paginator = PageNumberPagination()
    paginator.page_size = 15
    page = paginator.paginate_queryset(queryset, request)
    
    if page is not None:
        serializer = CourseListSerializer(page, many=True)
        return APIResponse.success({
            'count': paginator.page.paginator.count,
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'results': serializer.data
        })
    
    serializer = CourseListSerializer(queryset, many=True)
    return APIResponse.success(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_course_detail(request, course_id):
    """获取课程详情"""
    try:
        course = Course.objects.get(id=course_id, is_active=True)
    except Course.DoesNotExist:
        return APIResponse.not_found("课程不存在")
    
    serializer = CourseDetailSerializer(course, context={'request': request})
    return APIResponse.success(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_knowledge_summary(request, course_id):
    """获取知识点总结"""
    try:
        course = Course.objects.get(id=course_id, is_active=True)
    except Course.DoesNotExist:
        return APIResponse.not_found("课程不存在")
    
    # 获取最新版本的总结
    summary = course.summaries.order_by('-version').first()
    if not summary:
        return APIResponse.error("暂无知识点总结", code=404)
    
    serializer = KnowledgeSummarySerializer(summary)
    return APIResponse.success(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])  # 暂时允许未认证访问
def generate_knowledge_summary(request, course_id):
    """生成知识点总结（调用AI基于课本内容生成）"""
    try:
        course = Course.objects.get(id=course_id, is_active=True)
    except Course.DoesNotExist:
        return APIResponse.not_found("课程不存在")
    
    # 检查课程是否有内容
    if not course.content or not course.content.strip():
        return APIResponse.error("该课程暂无课本内容，无法生成知识点总结", code=400)
    
    # 获取前端传来的参数
    api_key = request.data.get('api_key')
    model = request.data.get('model', 'deepseek-chat')  # 默认使用chat
    regenerate = request.data.get('regenerate', False)
    
    if not api_key:
        return APIResponse.error("请提供API Key", code=400)
    
    # 检查是否需要重新生成
    if not regenerate and course.summaries.exists():
        # 返回已有的总结
        summary = course.summaries.order_by('-version').first()
        serializer = KnowledgeSummarySerializer(summary)
        return APIResponse.success(serializer.data, message="使用已有的知识点总结")
    
    try:
        # 使用PromptManager的便捷方法：获取并渲染Prompt模板
        final_prompt = PromptManager.get_and_render(
            template_type='knowledge_summary',
            subject=course.subject.code,  # 参数名是subject，不是subject_code
            course_title=course.title,
            grade=course.get_grade_display(),
            keywords=course.keywords,
            course_content=course.content  # 传入完整的课本内容
        )
        
        # 根据模型选择AI客户端
        if 'deepseek' in model.lower():
            # DeepSeek系列：deepseek-chat, deepseek-reasoner
            ai_client = DeepSeekClient(api_key=api_key, model=model)
        elif 'gpt' in model.lower():
            # OpenAI系列：gpt-5
            ai_client = OpenAIClient(api_key=api_key, model=model)
        else:
            # 默认使用DeepSeek-Chat
            ai_client = DeepSeekClient(api_key=api_key, model='deepseek-chat')
        
        # 调用AI生成知识点总结
        ai_response = ai_client.call_api(final_prompt)
        
        if not ai_response:
            return APIResponse.error("AI生成失败，未返回内容", code=500)
        
        # 创建新的知识点总结
        version = course.summaries.count() + 1
        summary = KnowledgeSummary.objects.create(
            course=course,
            content=ai_response,
            version=version
        )
        
        # TODO: 记录Prompt使用日志（后续可以添加到PromptUsageLog表）
        
        serializer = KnowledgeSummarySerializer(summary)
        return APIResponse.success(serializer.data, message="✅ AI知识点总结生成成功")
        
    except Exception as e:
        return APIResponse.error(f"生成知识点总结失败：{str(e)}", code=500)


@api_view(['GET'])
@permission_classes([AllowAny])  # 临时允许匿名访问，方便前端测试
def get_study_progress(request):
    """获取学习进度"""
    # 暂时使用第一个用户，后续接入真实认证后使用 request.user
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user = User.objects.first()
    if not user:
        return APIResponse.error(message="暂无用户数据")
    subject_id = request.query_params.get('subject_id')
    grade = request.query_params.get('grade')
    
    # 获取用户的所有学习进度
    progress_queryset = StudyProgress.objects.filter(user=user).select_related('course', 'course__subject')
    
    if subject_id:
        progress_queryset = progress_queryset.filter(course__subject_id=subject_id)
    if grade:
        progress_queryset = progress_queryset.filter(course__grade=grade)
    
    # 统计数据
    total_courses = Course.objects.filter(is_active=True).count()
    completed = progress_queryset.filter(status='completed').count()
    in_progress = progress_queryset.filter(status='in_progress').count()
    not_started = total_courses - completed - in_progress
    
    overall_progress = int((completed / total_courses * 100)) if total_courses > 0 else 0
    total_study_time = progress_queryset.aggregate(Sum('study_time'))['study_time__sum'] or 0
    
    # 按学科统计
    subjects = Subject.objects.filter(is_active=True)
    subjects_progress = []
    for subject in subjects:
        subject_courses = Course.objects.filter(subject=subject, is_active=True).count()
        subject_completed = progress_queryset.filter(course__subject=subject, status='completed').count()
        subject_in_progress = progress_queryset.filter(course__subject=subject, status='in_progress').count()
        subject_progress = int((subject_completed / subject_courses * 100)) if subject_courses > 0 else 0
        
        subjects_progress.append({
            'subject_id': subject.id,
            'subject_name': subject.name,
            'total': subject_courses,
            'completed': subject_completed,
            'in_progress': subject_in_progress,
            'progress': subject_progress
        })
    
    # 最近学习的课程
    recent_courses = progress_queryset.order_by('-last_access')[:10]
    recent_serializer = StudyProgressSerializer(recent_courses, many=True)
    
    data = {
        'total_courses': total_courses,
        'completed_courses': completed,
        'in_progress_courses': in_progress,
        'not_started_courses': not_started,
        'overall_progress': overall_progress,
        'total_study_time': total_study_time,
        'subjects_progress': subjects_progress,
        'recent_courses': recent_serializer.data
    }
    
    return APIResponse.success(data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_study_progress(request, course_id):
    """更新学习进度"""
    try:
        course = Course.objects.get(id=course_id, is_active=True)
    except Course.DoesNotExist:
        return APIResponse.not_found("课程不存在")
    
    serializer = UpdateStudyProgressSerializer(data=request.data)
    if not serializer.is_valid():
        return APIResponse.error("参数错误", errors=serializer.errors)
    
    # 获取或创建学习进度
    progress, created = StudyProgress.objects.get_or_create(
        user=request.user,
        course=course,
        defaults={'status': 'not_started', 'progress': 0, 'study_time': 0}
    )
    
    # 更新字段
    if 'status' in serializer.validated_data:
        progress.status = serializer.validated_data['status']
    if 'progress' in serializer.validated_data:
        progress.progress = serializer.validated_data['progress']
    if 'study_time' in serializer.validated_data:
        progress.study_time += serializer.validated_data['study_time']
    
    progress.save()
    
    return APIResponse.success({
        'course_id': course.id,
        'status': progress.status,
        'progress': progress.progress,
        'study_time': progress.study_time,
        'last_access': progress.last_access.isoformat()
    }, message="学习进度更新成功")

