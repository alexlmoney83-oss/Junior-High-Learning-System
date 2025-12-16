"""
智能练习页面
"""

import streamlit as st
import sys
from pathlib import Path

# 添加父目录到路径
sys.path.append(str(Path(__file__).parent.parent))

from utils.auth import check_authentication, logout_user
from utils.styles import load_custom_styles
from utils.api_client import get_api_client
from utils.local_storage import load_api_config_to_session
from utils.math_keyboard import render_math_keyboard, get_math_answer, clear_math_answer
from config.settings import SUBJECTS, QUESTION_TYPES

# 页面配置
st.set_page_config(
    page_title="智能练习",
    page_icon="✍️",
    layout="wide"
)

# 加载样式
load_custom_styles()

# 认证检查
if not check_authentication():
    st.error("❌ 请先登录")
    if st.button("返回登录"):
        st.switch_page("app.py")
    st.stop()

# 从本地存储加载API配置（如果有）
load_api_config_to_session()

# 页面标题
st.title("✍️ 智能练习")

# 顶部导航
col1, col2, col3 = st.columns([6, 2, 2])
with col1:
    st.markdown(f"**欢迎，{st.session_state.username}**")
with col2:
    if st.button("◀️ 返回课程", use_container_width=True):
        st.switch_page("pages/2_📖_课程详情.py")
with col3:
    if st.button("🏠 返回首页", use_container_width=True):
        st.switch_page("app.py")

st.markdown("---")

# 获取选择的学科和课程
selected_subject = st.session_state.get('selected_subject', 'chinese')
course_id = st.session_state.get('selected_course')
has_content = st.session_state.get('selected_course_has_content', False)

# 如果没有选择课程，返回课程列表
if not course_id:
    st.warning("⚠️ 请先从课程中心选择一门课程")
    if st.button("📚 前往课程中心"):
        st.switch_page("pages/1_📚_课程中心.py")
    st.stop()

# 检查课程是否切换了，如果切换则清空旧的练习题
if 'current_course_id' not in st.session_state:
    st.session_state.current_course_id = course_id
elif st.session_state.current_course_id != course_id:
    # 课程切换了，清空旧的练习题
    st.session_state.current_course_id = course_id
    st.session_state.current_exercises = None
    st.session_state.current_question_index = 0
    st.session_state.user_answers = {}

# 检查用户是否配置了AI API Key
has_api_key = st.session_state.get('api_key') is not None
api_key = st.session_state.get('api_key')
api_model = st.session_state.get('api_model', 'deepseek-chat')  # 修正默认模型名称

# 初始化API客户端
api_client = get_api_client()

# 如果没有配置API Key，提示用户
if not has_api_key:
    st.warning("⚠️ **请先配置AI API Key**")
    st.info(
        """
        **练习题需要AI大模型生成**
        
        请前往【个人中心】配置您的AI API Key：
        - 选择AI模型（DeepSeek-R1 / GPT-4）
        - 输入您的API Key
        - 保存配置
        
        配置完成后即可使用AI生成练习题功能。
        """
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏠 返回首页", use_container_width=True):
            st.switch_page("app.py")
    with col2:
        if st.button("👤 去配置API Key", use_container_width=True, type="primary"):
            st.switch_page("pages/4_👤_个人中心.py")
    st.stop()

# Mock练习题数据库 - 按学科分类（备用）
mock_exercises_by_subject = {
    'chinese': [
        {
            'id': 1,
            'type': 'choice',
            'question': '下列词语中加点字注音完全正确的一项是（ ）',
            'options': [
                'A. 蹒跚(pán)  霎时(shà)  分歧(qí)',
                'B. 粼粼(lín)  一霎(shà)  熬煎(áo)',
                'C. 委屈(wěi)  拆散(chāi)  嫩芽(nèn)',
                'D. 水波(bō)  蹲下(dūn)  信服(xìn)'
            ],
            'correct_answer': 'B',
            'explanation': '选项B的注音完全正确。A项"蹒跚"应读"pán shān"；C项"拆散"应读"chāi sàn"；D项"信服"应读"xìn fú"。'
        },
        {
            'id': 2,
            'type': 'fill',
            'question': '《散步》一文中，"我"最终选择走大路，是因为___________。',
            'correct_answer': '我伴同儿子的时日还长，伴同母亲的时日已短',
            'explanation': '这道题考查对文章主题的理解。作者选择走大路，体现了对母亲的孝顺和对亲情的珍惜。'
        },
        {
            'id': 3,
            'type': 'short_answer',
            'question': '请简要分析《散步》一文中环境描写的作用。',
            'correct_answer': '文中的环境描写渲染了温馨和谐的氛围，衬托了一家人其乐融融的情感，同时也象征着生命的传承和延续。',
            'explanation': '环境描写不仅营造氛围，还具有象征意义，体现了作者高超的写作技巧。'
        }
    ],
    'math': [
        {
            'id': 1,
            'type': 'choice',
            'question': '下列运算正确的是（ ）',
            'options': [
                'A. 2a + 3b = 5ab',
                'B. 5m - 3m = 2',
                'C. 3x² + 2x² = 5x²',
                'D. 7a + a = 7a²'
            ],
            'correct_answer': 'C',
            'explanation': '合并同类项时，只把系数相加，字母和字母的指数不变。C选项：3x² + 2x² = (3+2)x² = 5x²，正确。'
        },
        {
            'id': 2,
            'type': 'fill',
            'question': '计算：(2x + 3)(2x - 3) = ___________',
            'correct_answer': '4x² - 9',
            'explanation': '这是平方差公式：(a+b)(a-b) = a² - b²。所以(2x+3)(2x-3) = (2x)² - 3² = 4x² - 9。'
        },
        {
            'id': 3,
            'type': 'short_answer',
            'question': '化简并求值：2(x² - xy) - 3(x² - xy)，其中x = 2，y = -1。',
            'correct_answer': '先化简：2(x² - xy) - 3(x² - xy) = -1(x² - xy) = -x² + xy。代入x=2, y=-1：-4 + (-2) = -6',
            'explanation': '先合并同类项，再代入数值计算。注意符号的处理。'
        }
    ],
    'english': [
        {
            'id': 1,
            'type': 'choice',
            'question': 'I _______ to school every day.',
            'options': [
                'A. go',
                'B. goes',
                'C. going',
                'D. went'
            ],
            'correct_answer': 'A',
            'explanation': '主语I是第一人称，谓语动词用原形go。'
        },
        {
            'id': 2,
            'type': 'fill',
            'question': 'She _______ (like) reading books.',
            'correct_answer': 'likes',
            'explanation': '主语She是第三人称单数，动词要加-s。'
        },
        {
            'id': 3,
            'type': 'short_answer',
            'question': 'What do you usually do after school?',
            'correct_answer': 'I usually do my homework / play sports / read books after school.',
            'explanation': '用一般现在时描述日常习惯。'
        }
    ]
}

# 获取或初始化练习数据
if 'current_exercises' not in st.session_state or not st.session_state.current_exercises:
    st.info("📝 **生成练习题**")
    
    # 选择题目数量
    question_count = st.slider("选择题目数量：", min_value=3, max_value=10, value=5)
    
    if st.button("🤖 AI生成练习题", type="primary", use_container_width=True):
        if not has_content:
            st.warning("⚠️ 该课程暂无课本内容，AI将根据课程标题和大纲生成题目")
        
        with st.spinner(f"🤖 AI正在生成 {question_count} 道题目..."):
            response = api_client.generate_exercises(course_id, question_count, api_key, api_model)
            
            if response.get('code') != 200:
                st.error(f"❌ 生成失败：{response.get('message', '未知错误')}")
                st.info("请检查：\n1. API Key是否正确\n2. 网络连接是否正常\n3. Django后端是否运行")
                
                # 提供备用Mock数据
                if st.button("使用示例题目（不调用AI）"):
                    st.session_state.current_exercises = mock_exercises_by_subject.get(selected_subject, mock_exercises_by_subject['chinese'])
                    st.session_state.current_question_index = 0
                    st.session_state.user_answers = {}
                    st.rerun()
            else:
                result = response.get('data', {})
                # 提取题目列表（API返回格式：{course_id, generated_count, questions: [...]}）
                exercises = result.get('questions', []) if isinstance(result, dict) else []
                
                # 转换API返回的题目格式
                formatted_exercises = []
                for idx, ex in enumerate(exercises, 1):
                    # 确保ex是字典类型
                    if not isinstance(ex, dict):
                        continue
                    
                    formatted_ex = {
                        'id': ex.get('id', idx),
                        'type': ex.get('question_type', 'choice'),
                        'question': ex.get('question_text', ''),
                        'correct_answer': ex.get('answer', ''),
                        'explanation': ex.get('explanation', '')
                    }
                    
                    # 如果是选择题，添加选项
                    if formatted_ex['type'] == 'choice' and ex.get('options'):
                        formatted_ex['options'] = ex['options'].split('\n') if isinstance(ex['options'], str) else ex['options']
                    
                    formatted_exercises.append(formatted_ex)
                
                st.session_state.current_exercises = formatted_exercises
                st.session_state.current_question_index = 0
                st.session_state.user_answers = {}
                st.success(f"✅ 成功生成 {len(formatted_exercises)} 道题目！")
                st.rerun()
    
    st.stop()

# 当前题目索引
current_index = st.session_state.current_question_index
total_questions = len(st.session_state.current_exercises)

# 进度显示
st.markdown(f"### 📝 第 {current_index + 1} / {total_questions} 题")
st.progress((current_index + 1) / total_questions)

st.markdown("---")

# 当前题目
if current_index < total_questions:
    question = st.session_state.current_exercises[current_index]
    question_id = question['id']
    
    # 题型标签
    type_label = QUESTION_TYPES.get(question['type'], '未知题型')
    st.markdown(f"**题型：** `{type_label}`")
    
    st.markdown("---")
    
    # 题目内容
    st.markdown(f"### {question['question']}")
    
    st.markdown("")
    
    # 根据题型显示不同的输入组件
    if question['type'] == 'choice':
        # 选择题
        user_answer = st.radio(
            "请选择答案：",
            options=question['options'],
            key=f"answer_{question_id}",
            index=None
        )
        if user_answer:
            st.session_state.user_answers[question_id] = user_answer[0]  # 提取选项字母（A/B/C/D）
    
    elif question['type'] == 'fill':
        # 填空题
        # 只有数学科目使用虚拟键盘
        if selected_subject == 'math':
            st.markdown("#### 📝 输入答案（使用数学键盘）")
            answer_key = f"math_answer_{question_id}"
            user_answer = render_math_keyboard(answer_key)
            if user_answer:
                st.session_state.user_answers[question_id] = user_answer
        else:
            user_answer = st.text_input(
                "请输入答案：",
                key=f"answer_{question_id}",
                placeholder="在此输入你的答案..."
            )
            if user_answer:
                st.session_state.user_answers[question_id] = user_answer
    
    elif question['type'] == 'short_answer':
        # 简答题
        # 只有数学科目使用虚拟键盘
        if selected_subject == 'math':
            st.markdown("#### 📝 输入答案（使用数学键盘）")
            answer_key = f"math_answer_{question_id}"
            user_answer = render_math_keyboard(answer_key)
            if user_answer:
                st.session_state.user_answers[question_id] = user_answer
        else:
            user_answer = st.text_area(
                "请输入答案：",
                key=f"answer_{question_id}",
                placeholder="在此输入你的答案...",
                height=150
            )
            if user_answer:
                st.session_state.user_answers[question_id] = user_answer
    
    st.markdown("---")
    
    # 导航按钮（5列布局，支持AI判题和查看解析同时显示）
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    
    with col1:
        if current_index > 0:
            if st.button("⬅️ 上一题", use_container_width=True):
                st.session_state.current_question_index -= 1
                st.rerun()
    
    with col2:
        if current_index < total_questions - 1:
            if st.button("下一题 ➡️", use_container_width=True, type="primary"):
                st.session_state.current_question_index += 1
                st.rerun()
    
    with col3:
        # 数学科目且有答案时，显示AI判题按钮
        if selected_subject == 'math' and question_id in st.session_state.user_answers and has_api_key:
            if st.button("🤖 AI判题", use_container_width=True, type="secondary"):
                user_answer = st.session_state.user_answers.get(question_id, '')
                
                if not user_answer:
                    st.warning("请先输入答案")
                else:
                    with st.spinner("🤖 AI正在判题..."):
                        result, error = api_client.ai_check_answer(
                            question_text=question['question'],
                            question_type=question['type'],
                            standard_answer=question['correct_answer'],
                            user_answer=user_answer,
                            api_key=api_key,
                            model=api_model
                        )
                        
                        if error:
                            st.error(f"❌ 判题失败：{error}")
                        elif result:
                            # 显示判题结果
                            if result.get('correct'):
                                st.success(f"✅ {result.get('feedback', '正确！')}")
                            else:
                                st.error(f"❌ {result.get('feedback', '答案错误')}")
                                if result.get('hint'):
                                    st.info(f"💡 提示：{result['hint']}")
                            
                            # 显示详细信息
                            with st.expander("📊 详细评分"):
                                st.write(f"**得分：** {result.get('score', 0)}/100")
                                st.write(f"**你的答案：** {user_answer}")
                                st.write(f"**标准答案：** {question['correct_answer']}")
    
    with col4:
        # 所有题目都可以查看解析（不论科目和是否答题）
        if st.button("💡 查看解析", use_container_width=True):
            with st.expander("📖 答案解析", expanded=True):
                st.success(f"**正确答案：** {question['correct_answer']}")
                st.info(f"**解析：** {question['explanation']}")
    
    with col5:
        if current_index == total_questions - 1:
            if st.button("✅ 提交答案", use_container_width=True, type="primary"):
                # 计算得分
                correct_count = 0
                for q in st.session_state.current_exercises:
                    user_ans = st.session_state.user_answers.get(q['id'], '')
                    if user_ans and user_ans == q['correct_answer']:
                        correct_count += 1
                
                score = (correct_count / total_questions) * 100
                
                # 更新学习进度（完成练习，进度+10%）
                try:
                    api_client.update_study_progress(
                        course_id=course_id,
                        status='in_progress',
                        progress=min(100, 10)  # 每次完成练习增加10%进度
                    )
                except:
                    pass  # 静默处理错误
                
                st.balloons()
                st.success(f"🎉 提交成功！你的得分：{score:.1f}分（{correct_count}/{total_questions}题正确）")

else:
    # 所有题目已完成
    st.success("✅ 恭喜！你已完成所有练习题！")
    
    if st.button("🔄 重新开始", use_container_width=True):
        st.session_state.current_question_index = 0
        st.session_state.user_answers = {}
        st.rerun()

