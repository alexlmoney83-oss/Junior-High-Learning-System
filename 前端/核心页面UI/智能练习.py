"""
智能练习页面
"""

import streamlit as st
import sys
from pathlib import Path

# 添加项目路径
sys.path.append(str(Path(__file__).parent.parent))

from 用户认证.auth import check_authentication
from 基础架构.styles import load_custom_styles

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
    st.stop()

# 获取当前课程
course_id = st.session_state.get('selected_course', 1)

# 顶部导航
col1, col2, col3 = st.columns([6, 2, 2])
with col1:
    st.markdown("**智能练习**")
with col2:
    if st.button("◀️ 返回课程", use_container_width=True):
        st.switch_page("核心页面UI/课程详情.py")
with col3:
    if st.button("🏠 返回首页", use_container_width=True):
        st.switch_page("app.py")

st.markdown("---")

# 检查是否有练习题
exercises = st.session_state.get('current_exercises', [])

if not exercises:
    # 还没有练习题，显示生成界面
    st.title("✍️ 智能练习")
    st.markdown("### 🤖 AI生成练习题")
    
    st.info(
        """
        **练习题说明：**
        - 系统将为你生成25道练习题
        - 包含选择题（10道）、填空题（10道）、简答题（5道）
        - 难度分为基础、中等、提高三个等级
        - 支持AI智能批改简答题
        """
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🤖 开始生成练习题", use_container_width=True, type="primary"):
            from utils.api_client import get_api_client
            api_client = get_api_client()
            
            with st.spinner("AI正在生成练习题，请稍候（可能需要30-60秒）..."):
                result = api_client.generate_exercises(course_id, count=25)
            
            if result.get('code') == 200:
                exercises_data = result.get('data', {}).get('exercises', [])
                if exercises_data:
                    st.session_state['current_exercises'] = exercises_data
                    st.session_state['current_question_index'] = 0
                    st.session_state['user_answers'] = {}
                    st.success(f"✅ 成功生成 {len(exercises_data)} 道练习题！")
                    st.rerun()
                else:
                    st.error("❌ 生成的练习题为空")
            else:
                st.error(f"❌ 生成失败: {result.get('message', '未知错误')}")
                st.info("💡 请确保已在个人中心配置AI API Key")
    
    # 系统提示
    with st.expander("💡 系统提示"):
        st.info(
            """
            **已连接Django后端API：**
            - 练习题由AI实时生成（25道题）
            - 需要先在个人中心配置AI API Key
            - 生成时间约30-60秒，请耐心等待
            - 题型：选择题10道、填空题10道、简答题5道
            """
        )

else:
    # 有练习题，显示答题界面
    st.title("✍️ 智能练习")
    
    current_index = st.session_state.get('current_question_index', 0)
    current_question = exercises[current_index]
    
    # 进度显示
    progress = (current_index + 1) / len(exercises)
    st.progress(progress, text=f"进度: {current_index + 1}/{len(exercises)}")
    
    st.markdown("---")
    
    # 题目导航
    st.markdown("### 📊 题目导航")
    nav_cols = st.columns(min(len(exercises), 10))
    for i in range(min(len(exercises), 10)):
        with nav_cols[i]:
            answered = i in st.session_state.get('user_answers', {})
            icon = "✅" if answered else "⚪"
            if st.button(f"{icon} {i+1}", key=f"nav_{i}", use_container_width=True):
                st.session_state['current_question_index'] = i
                st.rerun()
    
    st.markdown("---")
    
    # 显示当前题目
    st.markdown(f"### 第 {current_index + 1} 题")
    
    # 难度标签
    difficulty_label = {
        'basic': '🟢 基础',
        'medium': '🟡 中等',
        'advanced': '🔴 提高'
    }[current_question.get('difficulty', 'basic')]
    
    # 题型标签
    type_label = {
        'choice': '📝 选择题',
        'fill': '✏️ 填空题',
        'short_answer': '📄 简答题'
    }[current_question['type']]
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"**题型**：{type_label}")
    with col2:
        st.markdown(f"**难度**：{difficulty_label}")
    
    st.markdown(f"**题目**：{current_question['question']}")
    
    # 根据题型显示不同的输入方式
    user_answer = st.session_state.get('user_answers', {}).get(current_index, '')
    
    if current_question['type'] == 'choice':
        # 选择题
        answer = st.radio(
            "请选择答案：",
            options=current_question['options'],
            index=current_question['options'].index(user_answer) if user_answer in current_question['options'] else 0,
            key=f"answer_{current_index}"
        )
        st.session_state['user_answers'][current_index] = answer
    
    elif current_question['type'] == 'fill':
        # 填空题
        answer = st.text_input(
            "请输入答案：",
            value=user_answer,
            key=f"answer_{current_index}"
        )
        st.session_state['user_answers'][current_index] = answer
    
    elif current_question['type'] == 'short_answer':
        # 简答题
        answer = st.text_area(
            "请输入答案：",
            value=user_answer,
            height=150,
            key=f"answer_{current_index}"
        )
        st.session_state['user_answers'][current_index] = answer
    
    st.markdown("---")
    
    # 导航按钮
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if current_index > 0:
            if st.button("◀️ 上一题", use_container_width=True):
                st.session_state['current_question_index'] = current_index - 1
                st.rerun()
    
    with col3:
        if current_index < len(exercises) - 1:
            if st.button("下一题 ▶️", use_container_width=True):
                st.session_state['current_question_index'] = current_index + 1
                st.rerun()
        else:
            if st.button("提交答案 ✅", use_container_width=True, type="primary"):
                from utils.api_client import get_api_client
                api_client = get_api_client()
                
                with st.spinner("正在批改答案，请稍候..."):
                    # 批量提交所有答案
                    user_answers = st.session_state.get('user_answers', {})
                    
                    if not user_answers:
                        st.warning("⚠️ 你还没有作答任何题目")
                    else:
                        st.success(f"✅ 已提交 {len(user_answers)} 道题的答案！")
                        st.info("💡 批改功能开发中，敬请期待...")
                        # TODO: 实现批量批改API调用
    
    # 系统提示
    with st.expander("💡 系统提示"):
        st.info(
            """
            **已连接Django后端API：**
            - 练习题数据来自数据库
            - 简答题支持AI智能批改
            - 选择题和填空题自动判分
            - 批改功能开发中
            """
        )


