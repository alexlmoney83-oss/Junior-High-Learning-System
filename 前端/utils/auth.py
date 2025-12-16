"""
用户认证模块
"""

import streamlit as st
from .local_storage import get_local_storage


def check_authentication() -> bool:
    """检查用户是否已认证"""
    # 先检查session_state（必须是True才返回，避免False被当作已检查）
    if st.session_state.get('is_authenticated') is True:
        return True
    
    # 如果session_state中没有或为False，检查本地存储
    try:
        storage = get_local_storage()
        auth_data = storage.load_auth()
        
        if auth_data:
            # 从本地存储恢复登录状态
            st.session_state['is_authenticated'] = True
            st.session_state['username'] = auth_data['username']
            st.session_state['user_id'] = 1  # Mock user_id
            st.session_state['user_info'] = {
                'username': auth_data['username'],
                'email': f'{auth_data["username"]}@example.com',
                'school': '上海市新北郊初级中学',
                'grade': 'grade1'
            }
            
            # 调试信息（可选）
            # st.info(f"🔄 已从本地存储恢复登录状态：{auth_data['username']}")
            
            return True
    except Exception as e:
        # 如果加载失败，打印错误但不影响流程
        print(f"加载本地登录状态失败: {e}")
        pass
    
    return False


def login_user(username: str, password: str, remember_me: bool = False) -> bool:
    """
    用户登录（当前使用Mock数据模拟）
    
    Args:
        username: 用户名
        password: 密码
        remember_me: 是否记住登录状态（7天内免登录）
    
    TODO: 后期替换为真实API调用
    """
    # Mock登录逻辑 - 任何用户名密码组合都可以登录（用于开发测试）
    if username and password:
        # 模拟登录成功
        st.session_state['is_authenticated'] = True
        st.session_state['username'] = username
        st.session_state['user_id'] = 1  # Mock user_id
        st.session_state['user_info'] = {
            'username': username,
            'email': f'{username}@example.com',
            'school': '上海市新北郊初级中学',
            'grade': 'grade1'
        }
        
        # 如果勾选了"记住我"，保存到本地存储
        if remember_me:
            try:
                storage = get_local_storage()
                success = storage.save_auth(username, remember_days=7)
                if success:
                    print(f"✅ 登录状态已保存到: {storage.auth_file}")
                else:
                    print(f"❌ 登录状态保存失败")
            except Exception as e:
                print(f"❌ 保存登录状态时出错: {e}")
        
        return True
    return False


def register_user(username: str, email: str, password: str, grade: str, school: str = '') -> bool:
    """
    用户注册 - 调用Django后端API
    """
    if not username or not email or not password or not grade:
        return False
    
    try:
        # 调用API客户端注册
        api_client = get_api_client()
        result = api_client.register(username, email, password, grade, school)
        
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
    # 清除本地存储
    storage = get_local_storage()
    storage.clear_auth()
    
    # 清除所有session state
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()


def render_login_page():
    """渲染登录/注册页面"""
    
    # 页面居中布局
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h1 style='text-align: center;'>🎓</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center;'>初中学习系统</h2>", unsafe_allow_html=True)
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
                    if login_user(username, password, remember_me):
                        if remember_me:
                            st.success("✅ 登录成功！已保存登录状态（7天内免登录）")
                        else:
                            st.success("✅ 登录成功！正在跳转...")
                        st.rerun()
                    else:
                        st.error("❌ 用户名或密码错误")
        
        if forgot_password:
            st.info("📧 请联系管理员重置密码")


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
        
        # 学校输入（用户可自行填写）
        school = st.text_input(
            "学校名称 *",
            placeholder="请输入学校名称",
            key="register_school"
        )
        
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
            elif not school:
                st.error("❌ 请填写学校名称")
            else:
                with st.spinner("注册中..."):
                    if register_user(username, email, password, grade, school):
                        st.success("✅ 注册成功！请使用新账号登录")
                    else:
                        st.error("❌ 注册失败，请重试")

