"""
用户认证模块
"""

import streamlit as st
from 基础架构.state_manager import set_state, clear_all_state
import sys
from pathlib import Path

# 添加utils路径
sys.path.append(str(Path(__file__).parent.parent))
from utils.api_client import get_api_client


def check_authentication() -> bool:
    """检查用户是否已认证"""
    return st.session_state.get('is_authenticated', False)


def login_user(username: str, password: str) -> bool:
    """
    用户登录 - 调用Django后端API
    """
    if not username or not password:
        return False
    
    try:
        # 调用API客户端登录
        api_client = get_api_client()
        result = api_client.login(username, password)
        
        if result.get('code') == 200:
            # 登录成功，保存用户信息
            user_data = result['data']
            set_state('is_authenticated', True)
            set_state('username', user_data['username'])
            set_state('user_id', user_data['user_id'])
            set_state('api_token', user_data['access_token'])
            set_state('user_info', {
                'username': user_data['username'],
                'email': user_data['email'],
                'school': '上海市新北郊初级中学',
                'grade': user_data.get('grade', 'grade1')
            })
            return True
        else:
            # 登录失败
            st.error(f"❌ {result.get('message', '登录失败')}")
            return False
    
    except Exception as e:
        st.error(f"❌ 登录失败: {str(e)}")
        return False


def register_user(username: str, email: str, password: str, grade: str) -> bool:
    """
    用户注册 - 调用Django后端API
    """
    if not username or not email or not password or not grade:
        return False
    
    try:
        # 调用API客户端注册
        api_client = get_api_client()
        result = api_client.register(username, email, password, grade)
        
        if result.get('code') == 200:
            return True
        else:
            st.error(f"❌ {result.get('message', '注册失败')}")
            return False
    
    except Exception as e:
        st.error(f"❌ 注册失败: {str(e)}")
        return False


def logout_user():
    """用户登出"""
    clear_all_state()
    st.rerun()


def render_login_page():
    """渲染登录/注册页面"""
    
    # 页面居中布局
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h1 style='text-align: center;'>🎓</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center;'>上海市初中学习系统</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #7f8c8d;'>欢迎使用 | 适配华为PAD & iPad</p>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 选项卡：登录 / 注册
        tab1, tab2 = st.tabs(["🔐 登录", "📝 注册"])
        
        with tab1:
            render_login_form()
        
        with tab2:
            render_register_form()


def render_login_form():
    """渲染登录表单"""
    
    st.markdown("### 登录账号")
    
    with st.form("login_form"):
        username = st.text_input(
            "用户名",
            placeholder="请输入用户名",
            key="login_username"
        )
        
        password = st.text_input(
            "密码",
            type="password",
            placeholder="请输入密码",
            key="login_password"
        )
        
        remember_me = st.checkbox("记住我（7天内免登录）")
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button(
                "登录",
                use_container_width=True,
                type="primary"
            )
        with col2:
            forgot_password = st.form_submit_button(
                "忘记密码",
                use_container_width=True
            )
        
        if submit:
            if not username or not password:
                st.error("❌ 请填写用户名和密码")
            else:
                with st.spinner("登录中..."):
                    if login_user(username, password):
                        st.success("✅ 登录成功！正在跳转...")
                        st.rerun()
                    else:
                        st.error("❌ 用户名或密码错误")
        
        if forgot_password:
            st.info("📧 请联系管理员重置密码")
    
    # 系统提示
    with st.expander("💡 系统提示"):
        st.info(
            """
            **已连接Django后端API：**
            - 使用真实的用户认证系统
            - 需要先注册账号才能登录
            - 后端地址：http://localhost:8000
            
            **如果没有账号：**
            - 请切换到"注册"标签页创建账号
            - 或在Django Admin后台创建用户
            """
        )


def render_register_form():
    """渲染注册表单"""
    
    st.markdown("### 注册新账号")
    
    with st.form("register_form"):
        username = st.text_input(
            "用户名 *",
            placeholder="3-20个字符",
            key="register_username"
        )
        
        email = st.text_input(
            "邮箱 *",
            placeholder="example@email.com",
            key="register_email"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            password = st.text_input(
                "密码 *",
                type="password",
                placeholder="至少8位",
                key="register_password"
            )
        with col2:
            password_confirm = st.text_input(
                "确认密码 *",
                type="password",
                placeholder="再次输入密码",
                key="register_password_confirm"
            )
        
        # 学校固定显示（不可编辑）
        st.info("🏫 **学校**：上海市新北郊初级中学（固定）")
        
        grade = st.selectbox(
            "年级 *",
            options=["grade1", "grade2", "grade3"],
            format_func=lambda x: {"grade1": "初一", "grade2": "初二", "grade3": "初三"}[x],
            key="register_grade"
        )
        
        submit = st.form_submit_button(
            "注册",
            use_container_width=True,
            type="primary"
        )
        
        if submit:
            # 表单验证
            if not username or not email or not password:
                st.error("❌ 请填写所有必填项")
            elif password != password_confirm:
                st.error("❌ 两次输入的密码不一致")
            elif len(password) < 8:
                st.error("❌ 密码至少8位")
            else:
                with st.spinner("注册中..."):
                    if register_user(username, email, password, grade):
                        st.success("✅ 注册成功！请使用新账号登录")
                    else:
                        st.error("❌ 注册失败，请重试")
    
    # 系统提示
    with st.expander("💡 系统提示"):
        st.info(
            """
            **已连接Django后端API：**
            - 注册会在数据库中创建真实账号
            - 学校固定为：上海市新北郊初级中学
            - 注册成功后请切换到登录标签页登录
            """
        )

