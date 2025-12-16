"""
全局状态管理器
"""

import streamlit as st
from typing import Any


def init_session_state():
    """初始化session状态"""
    
    # 用户认证状态
    if 'is_authenticated' not in st.session_state:
        st.session_state.is_authenticated = False
    
    if 'username' not in st.session_state:
        st.session_state.username = None
    
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    
    if 'user_info' not in st.session_state:
        st.session_state.user_info = {}
    
    # 当前选择的学科和课程
    if 'selected_subject' not in st.session_state:
        st.session_state.selected_subject = None
    
    if 'selected_course' not in st.session_state:
        st.session_state.selected_course = None
    
    # 练习题状态
    if 'current_exercises' not in st.session_state:
        st.session_state.current_exercises = []
    
    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0
    
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = {}
    
    # API配置
    if 'api_key' not in st.session_state:
        st.session_state.api_key = None
    
    if 'api_model' not in st.session_state:
        st.session_state.api_model = 'deepseek-r1'

