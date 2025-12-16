"""
前端配置文件
"""

# Django API配置
API_BASE_URL = "http://localhost:8000/api/v1"

# 应用配置
APP_NAME = "上海市初中学习系统"
APP_VERSION = "1.0.0"
DEFAULT_SCHOOL = "上海市新北郊初级中学"

# 分页配置
PAGE_SIZE = 15

# 学科配置
SUBJECTS = {
    'chinese': {
        'name': '语文',
        'code': 'chinese',
        'icon': '📚',
        'color': '#e74c3c'
    },
    'math': {
        'name': '数学',
        'code': 'math',
        'icon': '🔢',
        'color': '#3498db'
    },
    'english': {
        'name': '英语',
        'code': 'english',
        'icon': '🔤',
        'color': '#2ecc71'
    }
}

# 年级配置
GRADES = {
    'grade1': '初一',
    'grade2': '初二',
    'grade3': '初三'
}

# 难度配置
DIFFICULTIES = {
    'easy': '基础',
    'medium': '进阶',
    'hard': '提高'
}

# 题型配置
QUESTION_TYPES = {
    'choice': '选择题',
    'fill': '填空题',
    'short_answer': '简答题'
}

# AI模型配置
AI_MODELS = {
    'deepseek-r1': {
        'name': 'DeepSeek-R1',
        'endpoint': 'https://api.deepseek.com',
        'description': '推荐 | 性价比高'
    },
    'gpt-4': {
        'name': 'GPT-4',
        'endpoint': 'https://api.openai.com',
        'description': '高级 | 性能强大'
    },
    'gpt-4-turbo': {
        'name': 'GPT-4 Turbo',
        'endpoint': 'https://api.openai.com',
        'description': '高级 | 速度更快'
    }
}

