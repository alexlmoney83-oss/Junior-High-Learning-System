"""
更新Prompt模板，添加课本内容参考
"""

import os
import sys
import django
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'middle_school_system.settings')
django.setup()

from apps.ai_services.models import PromptTemplate

print("\n" + "="*60)
print("  🔄 更新Prompt模板")
print("="*60 + "\n")

# 1. 更新知识点总结Prompt
knowledge_prompt = PromptTemplate.objects.get(
    template_type='knowledge_summary',
    subject='math'
)

knowledge_prompt.template_content = """你是一位经验丰富的数学老师，请根据提供的课本内容生成知识点总结。

**课程信息：**
- 标题：{course_title}
- 年级：{grade}
- 关键词：{keywords}

**课本原文内容：**
{course_content}

**任务要求：**
1. 严格基于上述课本内容进行总结，不要自我发挥
2. 提取本章的核心知识点（3-5个）
3. 用简洁的语言解释每个知识点
4. 包含重要的定义、定理、公式
5. 列举典型例题（直接引用课本中的例题）
6. 总结常见易错点

**输出格式（Markdown）：**

# {course_title} - 知识点总结

## 一、核心知识点

### 1. [知识点1名称]
[解释说明]

### 2. [知识点2名称]
[解释说明]

...

## 二、重要公式/定理

1. [公式1]：说明
2. [公式2]：说明

## 三、典型例题

### 例题1：[题目]
**解答：**[步骤]

## 四、易错点提醒

1. [易错点1]
2. [易错点2]

请开始总结：
"""

knowledge_prompt.save()
print("✅ 已更新：知识点总结Prompt")

# 2. 更新练习题生成Prompt
exercise_prompt = PromptTemplate.objects.get(
    template_type='exercise_generation',
    subject='math'
)

exercise_prompt.template_content = """你是一位数学老师，请根据课本内容生成练习题。

**课程信息：**
- 标题：{course_title}
- 年级：{grade}
- 难度：{difficulty}
- 关键词：{keywords}

**课本原文内容：**
{course_content}

**任务要求：**
1. 严格基于上述课本内容出题，题目应该覆盖课本中的知识点
2. 题目类型包括：选择题、填空题、解答题
3. 题目难度与课程难度匹配
4. 每道题需要详细的解答步骤和答案
5. 生成{question_count}道题目

**输出格式（JSON）：**
```json
[
  {{
    "type": "choice",
    "question": "题目内容",
    "options": ["A. 选项1", "B. 选项2", "C. 选项3", "D. 选项4"],
    "answer": "B",
    "explanation": "解析说明",
    "difficulty": "easy"
  }},
  {{
    "type": "fill",
    "question": "题目内容（用___表示填空位置）",
    "answer": "正确答案",
    "explanation": "解析说明",
    "difficulty": "medium"
  }},
  {{
    "type": "short_answer",
    "question": "题目内容",
    "answer": "参考答案",
    "explanation": "解析说明",
    "difficulty": "hard"
  }}
]
```

请生成练习题：
"""

exercise_prompt.save()
print("✅ 已更新：练习题生成Prompt")

print("\n" + "="*60)
print("  ✅ Prompt模板更新完成")
print("="*60 + "\n")

print("现在AI会：")
print("  1. 读取Course.content中的课本实际内容")
print("  2. 基于课本内容生成知识点总结")
print("  3. 基于课本内容生成练习题")
print("  4. 不会自我发挥，确保内容准确性")
print()

