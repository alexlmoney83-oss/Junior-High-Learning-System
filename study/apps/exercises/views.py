"""
练习题模块视图
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Count, Q, Avg
from apps.courses.models import Course
from utils.response import APIResponse
from .models import Exercise, AnswerRecord
from .serializers import (
    ExerciseSerializer, ExerciseWithAnswerSerializer, AnswerRecordSerializer,
    SubmitAnswerSerializer, BatchSubmitAnswerSerializer, GenerateExercisesSerializer
)
from apps.ai_services.clients.deepseek_client import DeepSeekClient
from apps.ai_services.clients.openai_client import OpenAIClient
from apps.ai_services.prompt_manager import PromptManager
import json


@api_view(['GET'])
@permission_classes([AllowAny])
def get_exercises(request):
    """获取练习题列表"""
    course_id = request.query_params.get('course_id')
    if not course_id:
        return APIResponse.error("缺少course_id参数")
    
    try:
        course = Course.objects.get(id=course_id, is_active=True)
    except Course.DoesNotExist:
        return APIResponse.not_found("课程不存在")
    
    question_type = request.query_params.get('question_type')
    difficulty = request.query_params.get('difficulty')
    
    queryset = Exercise.objects.filter(course=course)
    if question_type:
        queryset = queryset.filter(question_type=question_type)
    if difficulty:
        queryset = queryset.filter(difficulty=difficulty)
    
    serializer = ExerciseSerializer(queryset, many=True)
    
    return APIResponse.success({
        'course_id': course.id,
        'course_title': course.title,
        'total_count': queryset.count(),
        'questions': serializer.data
    })


@api_view(['POST'])
@permission_classes([AllowAny])  # 暂时允许未认证访问
def generate_exercises(request):
    """使用AI生成练习题"""
    # 获取参数
    course_id = request.data.get('course_id')
    api_key = request.data.get('api_key')
    model = request.data.get('model', 'deepseek-chat')
    question_count = request.data.get('question_count', 5)
    difficulty = request.data.get('difficulty', 'basic')
    
    if not course_id:
        return APIResponse.error("缺少course_id参数", code=400)
    if not api_key:
        return APIResponse.error("请提供API Key", code=400)
    
    try:
        course = Course.objects.get(id=course_id, is_active=True)
    except Course.DoesNotExist:
        return APIResponse.not_found("课程不存在")
    
    # 检查课程是否有内容
    if not course.content or not course.content.strip():
        return APIResponse.error("该课程暂无课本内容，无法生成练习题", code=400)
    
    try:
        # 使用PromptManager获取并渲染Prompt模板
        final_prompt = PromptManager.get_and_render(
            template_type='exercise_generation',
            subject=course.subject.code,
            course_title=course.title,
            grade=course.get_grade_display(),
            keywords=course.keywords,
            difficulty=difficulty,
            question_count=question_count,  # 参数名应该是question_count
            course_content=course.content
        )
        
        # 根据模型选择AI客户端
        if 'deepseek' in model.lower():
            ai_client = DeepSeekClient(api_key=api_key, model=model)
        elif 'gpt' in model.lower():
            ai_client = OpenAIClient(api_key=api_key, model=model)
        else:
            ai_client = DeepSeekClient(api_key=api_key, model='deepseek-chat')
        
        # 调用AI生成练习题
        ai_response = ai_client.call_api(final_prompt)
        
        if not ai_response:
            return APIResponse.error("AI生成失败，未返回内容", code=500)
        
        # 解析AI返回的JSON格式练习题
        try:
            # AI可能返回markdown格式，需要提取JSON部分
            if '```json' in ai_response:
                json_start = ai_response.find('```json') + 7
                json_end = ai_response.find('```', json_start)
                json_str = ai_response[json_start:json_end].strip()
            elif '```' in ai_response:
                json_start = ai_response.find('```') + 3
                json_end = ai_response.find('```', json_start)
                json_str = ai_response[json_start:json_end].strip()
            else:
                json_str = ai_response.strip()
            
            exercises_data = json.loads(json_str)
            if not isinstance(exercises_data, list):
                return APIResponse.error("AI返回格式错误：期望JSON数组", code=500)
            
        except json.JSONDecodeError as e:
            return APIResponse.error(f"AI返回数据解析失败：{str(e)}", code=500)
        
        # 删除该课程的旧练习题（如果需要重新生成）
        Exercise.objects.filter(course=course, is_ai_generated=True).delete()
        
        # 创建新的练习题
        created_exercises = []
        for ex_data in exercises_data:
            try:
                # 字段映射：AI返回的字段名 → 数据库字段名
                question_type = ex_data.get('type') or ex_data.get('question_type', 'choice')
                question_text = ex_data.get('question') or ex_data.get('question_text', '')
                
                exercise = Exercise.objects.create(
                    course=course,
                    question_type=question_type,
                    question_text=question_text,
                    options=ex_data.get('options', []),
                    answer=ex_data.get('answer', ''),
                    explanation=ex_data.get('explanation', ''),
                    difficulty=ex_data.get('difficulty', difficulty),
                    is_ai_generated=True
                )
                created_exercises.append(exercise)
            except Exception as e:
                continue  # 跳过有问题的题目
        
        if not created_exercises:
            return APIResponse.error("未能成功创建任何练习题", code=500)
        
        serializer = ExerciseWithAnswerSerializer(created_exercises, many=True)
        
        return APIResponse.success({
            'course_id': course.id,
            'generated_count': len(created_exercises),
            'questions': serializer.data
        }, message=f"✅ 成功生成{len(created_exercises)}道练习题")
        
    except Exception as e:
        return APIResponse.error(f"生成练习题失败：{str(e)}", code=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_answer(request):
    """提交练习答案"""
    serializer = SubmitAnswerSerializer(data=request.data)
    if not serializer.is_valid():
        return APIResponse.error("参数错误", errors=serializer.errors)
    
    exercise_id = serializer.validated_data['exercise_id']
    user_answer = serializer.validated_data['user_answer']
    time_spent = serializer.validated_data['time_spent']
    
    try:
        exercise = Exercise.objects.get(id=exercise_id)
    except Exercise.DoesNotExist:
        return APIResponse.not_found("题目不存在")
    
    # 判断答案是否正确
    is_correct = user_answer.strip() == exercise.answer.strip()
    score = 100 if is_correct else 0
    
    # 创建答题记录
    record = AnswerRecord.objects.create(
        user=request.user,
        exercise=exercise,
        user_answer=user_answer,
        is_correct=is_correct,
        score=score,
        time_spent=time_spent
    )
    
    return APIResponse.success({
        'record_id': record.id,
        'exercise_id': exercise.id,
        'user_answer': user_answer,
        'is_correct': is_correct,
        'score': score,
        'standard_answer': exercise.answer,
        'explanation': exercise.explanation,
        'submitted_at': record.submitted_at.isoformat()
    }, message="提交成功")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def batch_submit_answers(request):
    """批量提交练习答案"""
    serializer = BatchSubmitAnswerSerializer(data=request.data)
    if not serializer.is_valid():
        return APIResponse.error("参数错误", errors=serializer.errors)
    
    course_id = serializer.validated_data['course_id']
    answers = serializer.validated_data['answers']
    
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return APIResponse.not_found("课程不存在")
    
    # 批量处理答案
    results = []
    correct_count = 0
    total_score = 0
    total_time = 0
    
    for answer_data in answers:
        exercise_id = answer_data.get('exercise_id')
        user_answer = answer_data.get('user_answer', '')
        time_spent = answer_data.get('time_spent', 0)
        
        try:
            exercise = Exercise.objects.get(id=exercise_id, course=course)
            is_correct = user_answer.strip() == exercise.answer.strip()
            score = 100 if is_correct else 0
            
            # 创建答题记录
            AnswerRecord.objects.create(
                user=request.user,
                exercise=exercise,
                user_answer=user_answer,
                is_correct=is_correct,
                score=score,
                time_spent=time_spent
            )
            
            if is_correct:
                correct_count += 1
            total_score += score
            total_time += time_spent
            
            results.append({
                'exercise_id': exercise.id,
                'is_correct': is_correct,
                'score': score,
                'user_answer': user_answer,
                'standard_answer': exercise.answer
            })
        except Exercise.DoesNotExist:
            continue
    
    total_count = len(results)
    avg_score = int(total_score / total_count) if total_count > 0 else 0
    
    return APIResponse.success({
        'total_count': total_count,
        'correct_count': correct_count,
        'wrong_count': total_count - correct_count,
        'total_score': avg_score,
        'time_spent': total_time,
        'results': results
    }, message="批量提交成功")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_answer_records(request):
    """获取答题记录"""
    user = request.user
    course_id = request.query_params.get('course_id')
    
    queryset = AnswerRecord.objects.filter(user=user).select_related('exercise', 'exercise__course')
    
    if course_id:
        queryset = queryset.filter(exercise__course_id=course_id)
    
    queryset = queryset.order_by('-submitted_at')[:50]  # 最近50条
    serializer = AnswerRecordSerializer(queryset, many=True)
    
    return APIResponse.success({
        'count': queryset.count(),
        'results': serializer.data
    })


@api_view(['GET'])
@permission_classes([AllowAny])  # 临时允许匿名访问，方便前端测试
def get_statistics(request):
    """获取答题统计"""
    # 暂时使用第一个用户，后续接入真实认证后使用 request.user
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user = User.objects.first()
    if not user:
        return APIResponse.success({
            'total_exercises': 0,
            'correct_exercises': 0,
            'accuracy_rate': 0,
            'avg_score': 0,
            'total_time_spent': 0
        })
    subject_id = request.query_params.get('subject_id')
    
    queryset = AnswerRecord.objects.filter(user=user)
    
    if subject_id:
        queryset = queryset.filter(exercise__course__subject_id=subject_id)
    
    total = queryset.count()
    if total == 0:
        return APIResponse.success({
            'total_exercises': 0,
            'correct_exercises': 0,
            'accuracy_rate': 0,
            'avg_score': 0,
            'total_time_spent': 0
        })
    
    correct = queryset.filter(is_correct=True).count()
    accuracy_rate = round((correct / total) * 100, 1) if total > 0 else 0
    avg_score = queryset.aggregate(Avg('score'))['score__avg'] or 0
    total_time = queryset.aggregate(total=Count('time_spent'))['total'] or 0
    
    return APIResponse.success({
        'total_exercises': total,
        'correct_exercises': correct,
        'accuracy_rate': accuracy_rate,
        'avg_score': round(avg_score, 1),
        'total_time_spent': total_time
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def ai_check_answer(request):
    """
    AI智能判题
    判断用户答案是否与标准答案数学等价
    """
    from apps.ai_services.clients.deepseek_client import DeepSeekClient
    from apps.ai_services.clients.openai_client import OpenAIClient
    
    # 获取参数
    question_text = request.data.get('question_text', '')
    question_type = request.data.get('question_type', 'choice')
    standard_answer = request.data.get('standard_answer', '')
    user_answer = request.data.get('user_answer', '')
    api_key = request.data.get('api_key')
    model = request.data.get('model', 'deepseek-chat')
    
    if not api_key:
        return APIResponse.error(message="缺少API Key")
    
    if not user_answer:
        return APIResponse.error(message="用户答案不能为空")
    
    if not standard_answer:
        return APIResponse.error(message="标准答案不能为空")
    
    # 构建判题Prompt
    prompt = f"""你是一位经验丰富的数学老师，请判断学生答案是否正确。

**题目信息：**
题目类型：{'选择题' if question_type == 'choice' else '填空题' if question_type == 'fill' else '解答题'}
题目内容：{question_text}

**答案对比：**
标准答案：{standard_answer}
学生答案：{user_answer}

**判断要求：**
1. 判断数学等价性（允许不同形式）
   - 允许展开与因式分解：如 (x+1)² 等价于 x²+2x+1
   - 允许顺序不同：如 x+1 等价于 1+x
   - 允许符号变体：如 x^2 等价于 x²，* 等价于 ×
   - 允许未化简的形式
2. 如果正确，给予鼓励性反馈
3. 如果错误，指出具体错误原因并给出提示
4. 返回JSON格式（只返回JSON，不要其他内容）：

{{
  "correct": true,
  "score": 100,
  "feedback": "✅ 正确！你的答案完全正确。",
  "hint": ""
}}

或错误时：

{{
  "correct": false,
  "score": 0,
  "feedback": "❌ 答案错误。",
  "hint": "提示：注意符号和运算顺序。"
}}
"""
    
    try:
        # 选择AI客户端
        if 'deepseek' in model.lower():
            ai_client = DeepSeekClient(api_key=api_key, model=model)
        elif 'gpt' in model.lower():
            ai_client = OpenAIClient(api_key=api_key, model=model)
        else:
            ai_client = DeepSeekClient(api_key=api_key, model='deepseek-chat')
        
        # 调用AI
        ai_response = ai_client.call_api(prompt)
        
        # 解析JSON响应
        import json
        import re
        
        # 尝试提取JSON（可能被markdown代码块包裹）
        json_match = re.search(r'```json\s*(.*?)\s*```', ai_response, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            # 尝试提取第一个完整的JSON对象
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
            else:
                json_str = ai_response
        
        result = json.loads(json_str)
        
        # 确保必要字段存在
        if 'correct' not in result:
            result['correct'] = False
        if 'score' not in result:
            result['score'] = 100 if result['correct'] else 0
        if 'feedback' not in result:
            result['feedback'] = "判断完成"
        if 'hint' not in result:
            result['hint'] = ""
        
        return APIResponse.success(result, message="AI判题完成")
        
    except json.JSONDecodeError as e:
        # JSON解析失败，返回原始响应
        return APIResponse.error(
            message=f"AI返回格式错误：{str(e)}",
            data={'raw_response': ai_response}
        )
    except Exception as e:
        return APIResponse.error(message=f"AI判题失败：{str(e)}")

