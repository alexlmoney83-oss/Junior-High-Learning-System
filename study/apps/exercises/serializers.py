"""
练习题模块序列化器
"""
from rest_framework import serializers
from .models import Exercise, AnswerRecord


class ExerciseSerializer(serializers.ModelSerializer):
    """练习题序列化器"""
    question_type_display = serializers.CharField(source='get_question_type_display', read_only=True)
    difficulty_display = serializers.CharField(source='get_difficulty_display', read_only=True)
    
    class Meta:
        model = Exercise
        fields = ['id', 'question_type', 'question_type_display', 'question_text', 
                  'options', 'difficulty', 'difficulty_display', 'is_ai_generated']


class ExerciseWithAnswerSerializer(serializers.ModelSerializer):
    """带答案的练习题序列化器（提交后）"""
    question_type_display = serializers.CharField(source='get_question_type_display', read_only=True)
    difficulty_display = serializers.CharField(source='get_difficulty_display', read_only=True)
    
    class Meta:
        model = Exercise
        fields = ['id', 'question_type', 'question_type_display', 'question_text', 
                  'options', 'answer', 'explanation', 'difficulty', 'difficulty_display']


class AnswerRecordSerializer(serializers.ModelSerializer):
    """答题记录序列化器"""
    exercise = ExerciseSerializer(read_only=True)
    course_title = serializers.CharField(source='exercise.course.title', read_only=True)
    subject_name = serializers.CharField(source='exercise.course.subject.name', read_only=True)
    
    class Meta:
        model = AnswerRecord
        fields = ['id', 'exercise', 'course_title', 'subject_name', 'user_answer', 
                  'is_correct', 'score', 'ai_feedback', 'time_spent', 'submitted_at']


class SubmitAnswerSerializer(serializers.Serializer):
    """提交答案序列化器"""
    exercise_id = serializers.IntegerField()
    user_answer = serializers.CharField()
    time_spent = serializers.IntegerField(default=0, min_value=0)


class BatchSubmitAnswerSerializer(serializers.Serializer):
    """批量提交答案序列化器"""
    course_id = serializers.IntegerField()
    answers = serializers.ListField(
        child=serializers.DictField()
    )


class GenerateExercisesSerializer(serializers.Serializer):
    """生成练习题序列化器"""
    course_id = serializers.IntegerField()
    regenerate = serializers.BooleanField(default=False)

