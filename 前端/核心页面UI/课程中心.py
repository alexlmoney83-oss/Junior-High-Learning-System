"""
课程中心页面
"""

import streamlit as st
import sys
from pathlib import Path

# 添加项目路径
sys.path.append(str(Path(__file__).parent.parent))

from 用户认证.auth import check_authentication, logout_user
from 基础架构.styles import load_custom_styles
from 基础架构.config import SUBJECTS, GRADES

# 页面配置
st.set_page_config(
    page_title="课程中心",
    page_icon="📚",
    layout="wide"
)

# 加载样式
load_custom_styles()

# 认证检查
if not check_authentication():
    st.error("❌ 请先登录")
    st.stop()

# 页面标题
st.title("📚 课程中心")

# 顶部导航
col1, col2, col3 = st.columns([6, 2, 2])
with col1:
    st.markdown(f"**欢迎，{st.session_state.username}**")
with col2:
    if st.button("🏠 返回首页", use_container_width=True):
        st.switch_page("app.py")
with col3:
    if st.button("🚪 退出登录", use_container_width=True):
        logout_user()

st.markdown("---")

# 获取当前选择的学科
selected_subject = st.session_state.get('selected_subject', 'chinese')
subject_info = SUBJECTS.get(selected_subject, SUBJECTS['chinese'])

# 学科和年级选择
col1, col2 = st.columns([1, 1])

with col1:
    subject_code = st.selectbox(
        "选择学科",
        options=list(SUBJECTS.keys()),
        format_func=lambda x: f"{SUBJECTS[x]['icon']} {SUBJECTS[x]['name']}",
        index=list(SUBJECTS.keys()).index(selected_subject)
    )
    if subject_code != selected_subject:
        st.session_state['selected_subject'] = subject_code
        st.rerun()

with col2:
    grade = st.selectbox(
        "选择年级",
        options=list(GRADES.keys()),
        format_func=lambda x: GRADES[x]
    )

st.markdown(f"## {subject_info['icon']} {subject_info['name']} - {GRADES[grade]}")

st.markdown("---")

# 从后端API获取课程数据
from utils.api_client import get_api_client

api_client = get_api_client()

with st.spinner("正在加载课程列表..."):
    result = api_client.get_courses(subject_code=subject_code, grade=grade)

if result.get('code') == 200:
    courses = result.get('data', [])
    
    if not courses:
        st.warning("⚠️ 该学科暂无课程数据，请联系管理员添加课程。")
        st.info("💡 提示：可以在Django Admin后台添加课程数据")
    else:
        # 显示课程列表
        st.markdown(f"### 📖 课程列表 (共 {len(courses)} 门课程)")

        for course in courses:
            # 难度标签
            difficulty_label = {
                'easy': '🟢 基础',
                'medium': '🟡 进阶',
                'hard': '🔴 提高'
            }.get(course.get('difficulty', 'easy'), '🟢 基础')
            
            # 课程卡片
            with st.container():
                col1, col2, col3 = st.columns([6, 2, 2])
                
                with col1:
                    st.markdown(f"### 📖 {course['title']}")
                    # 显示课程大纲的前100个字符
                    outline = course.get('outline', '暂无课程简介')
                    if len(outline) > 100:
                        outline = outline[:100] + "..."
                    st.markdown(f"<p style='color: #7f8c8d;'>{outline}</p>", unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"**难度**：{difficulty_label}")
                    # 显示关键词
                    keywords = course.get('keywords', '')
                    if keywords:
                        st.markdown(f"🏷️ {keywords[:30]}...")
                
                with col3:
                    st.markdown("　")  # 占位
                    if st.button("📖 查看详情", key=f"course_{course['id']}", use_container_width=True):
                        st.session_state['selected_course'] = course['id']
                        st.session_state['selected_course_data'] = course
                        st.switch_page("核心页面UI/课程详情.py")
                
                st.markdown("---")
else:
    st.error(f"❌ 加载课程失败: {result.get('message', '未知错误')}")
    st.info("💡 请确保Django后端服务已启动（http://localhost:8000）")

# 开发提示
with st.expander("💡 系统提示"):
    st.info(
        """
        **已连接Django后端API：**
        - 课程数据来自MySQL数据库
        - 如果没有课程显示，请在Django Admin后台添加课程
        - 后端地址：http://localhost:8000
        - Admin后台：http://localhost:8000/admin/
        """
    )

