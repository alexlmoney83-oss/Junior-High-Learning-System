"""
课程详情页面
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
    page_title="课程详情",
    page_icon="📖",
    layout="wide"
)

# 加载样式
load_custom_styles()

# 认证检查
if not check_authentication():
    st.error("❌ 请先登录")
    st.stop()

# 获取当前课程ID和数据
course_id = st.session_state.get('selected_course', 1)
course_detail = st.session_state.get('selected_course_data', None)

# 如果没有课程数据，从API获取
if not course_detail:
    from utils.api_client import get_api_client
    api_client = get_api_client()
    
    with st.spinner("正在加载课程详情..."):
        result = api_client.get_course_detail(course_id)
    
    if result.get('code') == 200:
        course_detail = result.get('data')
    else:
        st.error(f"❌ 加载课程失败: {result.get('message', '未知错误')}")
        st.stop()

# 顶部导航
col1, col2, col3 = st.columns([6, 2, 2])
with col1:
    st.markdown("**课程详情**")
with col2:
    if st.button("◀️ 返回列表", use_container_width=True):
        st.switch_page("核心页面UI/课程中心.py")
with col3:
    if st.button("🏠 返回首页", use_container_width=True):
        st.switch_page("app.py")

st.markdown("---")

# 课程标题
st.title(f"📖 {course_detail.get('title', '课程详情')}")

# 课程元信息
col1, col2, col3, col4 = st.columns(4)
with col1:
    subject_name = course_detail.get('subject_name', '未知')
    st.metric("学科", subject_name)
with col2:
    grade_display = {'grade1': '初一', 'grade2': '初二', 'grade3': '初三'}.get(course_detail.get('grade', 'grade1'), '初一')
    st.metric("年级", grade_display)
with col3:
    difficulty_display = {'easy': '基础', 'medium': '进阶', 'hard': '提高'}.get(course_detail.get('difficulty', 'easy'), '基础')
    st.metric("难度", difficulty_display)
with col4:
    st.metric("课程序号", f"第{course_detail.get('course_number', 1)}课")

st.markdown("---")

# 课程描述
st.markdown("### 📝 课程大纲")
outline = course_detail.get('outline', '暂无课程大纲')
st.markdown(outline)

# 关键词标签
keywords_str = course_detail.get('keywords', '')
if keywords_str:
    st.markdown("### 🏷️ 关键词")
    keywords = [k.strip() for k in keywords_str.split(',') if k.strip()]
    if keywords:
        cols = st.columns(min(len(keywords), 5))
        for i, keyword in enumerate(keywords[:5]):
            with cols[i]:
                st.markdown(f"`{keyword}`")

st.markdown("---")

# 功能按钮
st.markdown("### 🎯 学习功能")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 📚 知识点总结")
    st.markdown("通过AI生成本课的知识点总结，帮助你快速掌握重点内容。")
    if st.button("🤖 查看/生成知识点总结", use_container_width=True, type="primary"):
        from utils.api_client import get_api_client
        api_client = get_api_client()
        
        with st.spinner("正在生成知识点总结，请稍候..."):
            result = api_client.generate_knowledge_summary(course_id)
        
        if result.get('code') == 200:
            summary = result.get('data', {}).get('content', '')
            st.success("✅ 知识点总结生成成功！")
            st.markdown(summary)
        else:
            st.error(f"❌ 生成失败: {result.get('message', '未知错误')}")
            st.info("💡 请确保已在个人中心配置AI API Key")

with col2:
    st.markdown("#### ✍️ 智能练习")
    st.markdown("通过AI生成25道练习题，包含选择题、填空题和简答题。")
    if st.button("🤖 开始智能练习", use_container_width=True, type="primary"):
        st.session_state['selected_course'] = course_id
        st.switch_page("核心页面UI/智能练习.py")

st.markdown("---")

# 学习进度更新
# 开发提示
with st.expander("💡 系统提示"):
    st.info(
        """
        **已连接Django后端API：**
        - 课程数据来自MySQL数据库
        - AI功能需要在个人中心配置API Key
        - 知识点总结和练习题由AI实时生成
        - 后端地址：http://localhost:8000
        """
    )

