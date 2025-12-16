"""
初中学习系统 - Streamlit前端主入口

运行方式:
streamlit run app.py
"""

import streamlit as st
import sys
from pathlib import Path

# 添加项目路径
sys.path.append(str(Path(__file__).parent))

from utils.auth import check_authentication, render_login_page
from utils.styles import load_custom_styles
from utils.state_manager import init_session_state

# 页面配置
st.set_page_config(
    page_title="初中学习系统",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"  # PAD上默认收起侧边栏
)

# 加载自定义样式
load_custom_styles()

# 初始化session状态
init_session_state()

# 认证检查
if not check_authentication():
    # 未登录，显示登录页面
    render_login_page()
else:
    # 已登录，显示主界面
    st.title("🎓 初中学习系统")
    
    # 欢迎信息
    user_name = st.session_state.get('username', '同学')
    st.markdown(f"### 欢迎回来，{user_name}！")
    
    st.markdown("---")
    
    # 学科选择卡片
    st.markdown("## 📚 选择学科开始学习")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📚 语文", use_container_width=True, key="chinese", type="primary"):
            st.session_state['selected_subject'] = 'chinese'
            st.switch_page("pages/1_📚_课程中心.py")
    
    with col2:
        if st.button("🔢 数学", use_container_width=True, key="math", type="primary"):
            st.session_state['selected_subject'] = 'math'
            st.switch_page("pages/1_📚_课程中心.py")
    
    with col3:
        if st.button("🔤 英语", use_container_width=True, key="english", type="primary"):
            st.session_state['selected_subject'] = 'english'
            st.switch_page("pages/1_📚_课程中心.py")
    
    st.markdown("---")
    
    # 快速入口
    st.markdown("## 🚀 快速入口")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📊 学习统计", use_container_width=True):
            st.info("学习统计功能开发中...")
    
    with col2:
        if st.button("✍️ 我的练习", use_container_width=True):
            st.info("我的练习功能开发中...")
    
    with col3:
        if st.button("📖 错题本", use_container_width=True):
            st.info("错题本功能开发中...")
    
    with col4:
        if st.button("👤 个人中心", use_container_width=True):
            st.switch_page("pages/4_👤_个人中心.py")
    
    # 页脚
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #666; font-size: 14px;">
            初中学习系统 | 适配华为PAD & iPad
        </div>
        """,
        unsafe_allow_html=True
    )

