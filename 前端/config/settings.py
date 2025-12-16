"""
前端配置文件
"""

# Django API配置
# 内网访问：将localhost改为服务器的内网IP（如：192.168.1.100）
# 本机访问：使用localhost
import os

# 支持环境变量配置，方便内网部署
SERVER_IP = os.getenv('SERVER_IP', 'localhost')
API_BASE_URL = f"http://{SERVER_IP}:8000/api/v1"

# 如果需要内网访问，请直接修改为服务器的内网IP地址：
# API_BASE_URL = "http://192.168.1.100:8000/api/v1"

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
    'deepseek-chat': {
        'name': 'DeepSeek-Chat',
        'endpoint': 'https://api.deepseek.com',
        'description': '推荐 | 快速高效，适合日常使用'
    },
    'deepseek-reasoner': {
        'name': 'DeepSeek-Reasoner',
        'endpoint': 'https://api.deepseek.com',
        'description': '推理 | 显示思考过程，适合作业批改'
    },
    'gpt-5': {
        'name': 'GPT-5',
        'endpoint': 'https://api.openai.com',
        'description': '高级 | OpenAI最新旗舰模型'
    }
}

