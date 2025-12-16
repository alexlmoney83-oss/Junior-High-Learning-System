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


def set_state(key: str, value: Any):
    """设置状态值"""
    st.session_state[key] = value


def get_state(key: str, default: Any = None) -> Any:
    """获取状态值"""
    return st.session_state.get(key, default)


def remove_state(key: str):
    """移除状态值"""
    if key in st.session_state:
        del st.session_state[key]


def clear_exercise_state():
    """清除练习题相关状态"""
    keys = ['current_exercises', 'current_question_index', 'user_answers']
    for key in keys:
        remove_state(key)


def clear_all_state():
    """清除所有状态（用于登出）"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    init_session_state()

