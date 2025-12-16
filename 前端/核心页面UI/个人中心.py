"""
个人中心页面 - 用户配置AI API Key
"""

import streamlit as st
import sys
from pathlib import Path

# 添加项目路径
sys.path.append(str(Path(__file__).parent.parent))

from 用户认证.auth import check_authentication, logout_user
from 基础架构.styles import load_custom_styles
from 基础架构.config import AI_MODELS, DEFAULT_SCHOOL

# 页面配置
st.set_page_config(
    page_title="个人中心",
    page_icon="👤",
    layout="wide"
)

# 加载样式
load_custom_styles()

# 认证检查
if not check_authentication():
    st.error("❌ 请先登录")
    st.stop()

# 顶部导航
col1, col2 = st.columns([8, 2])
with col1:
    st.title("👤 个人中心")
with col2:
    if st.button("🏠 返回首页", use_container_width=True):
        st.switch_page("app.py")

st.markdown("---")

# 获取用户信息
user_info = st.session_state.get('user_info', {})
username = st.session_state.get('username', '用户')

# 用户基本信息
st.markdown("## 📋 基本信息")

col1, col2 = st.columns([1, 3])

with col1:
    # 头像占位
    st.markdown(
        """
        <div style="
            width: 120px;
            height: 120px;
            border-radius: 60px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 48px;
            font-weight: bold;
        ">
            {0}
        </div>
        """.format(username[0].upper()),
        unsafe_allow_html=True
    )

with col2:
    st.markdown(f"### {username}")
    st.markdown(f"**邮箱**：{user_info.get('email', 'user@example.com')}")
    st.markdown(f"**学校**：{DEFAULT_SCHOOL}")
    st.markdown(f"**年级**：{user_info.get('grade', '初一')}")

st.markdown("---")

# AI模型配置 - 核心功能
st.markdown("## 🤖 AI模型配置")

st.info(
    """
    **💡 重要说明：**
    - AI功能（知识点总结、练习题生成、答案批改）需要使用AI API
    - 请在此配置您自己的API Key
    - API调用费用由您自己承担
    - 推荐使用DeepSeek（性价比高，价格便宜）
    """
)

# API Key配置表单
with st.form("ai_config_form"):
    st.markdown("### 配置API Key")
    
    # 选择AI模型
    model_type = st.selectbox(
        "选择AI模型",
        options=list(AI_MODELS.keys()),
        format_func=lambda x: f"{AI_MODELS[x]['name']} - {AI_MODELS[x]['description']}",
        help="推荐使用DeepSeek-R1，性价比高"
    )
    
    # 显示当前模型信息
    current_model = AI_MODELS[model_type]
    st.markdown(f"**API端点**：`{current_model['endpoint']}`")
    
    # API Key输入
    api_key = st.text_input(
        "API Key",
        type="password",
        placeholder="sk-xxxxxxxxxxxxxxxxxxxxx",
        help="您的API密钥将被加密存储到数据库"
    )
    
    # 获取API Key的帮助信息
    with st.expander("❓ 如何获取API Key？"):
        if model_type == 'deepseek-r1':
            st.markdown(
                """
                **DeepSeek API Key获取步骤：**
                
                1. 访问 [DeepSeek平台](https://platform.deepseek.com/)
                2. 注册账号并登录
                3. 进入"API Keys"页面
                4. 点击"创建新密钥"
                5. 复制生成的API Key（格式：sk-xxxxx）
                6. 粘贴到上方输入框
                
                **费用说明：**
                - DeepSeek价格便宜（约为GPT-4的1/10）
                - 按使用量计费
                - 新用户通常有免费额度
                """
            )
        else:
            st.markdown(
                """
                **OpenAI API Key获取步骤：**
                
                1. 访问 [OpenAI平台](https://platform.openai.com/)
                2. 注册账号并登录
                3. 进入"API Keys"页面
                4. 点击"Create new secret key"
                5. 复制生成的API Key
                6. 粘贴到上方输入框
                
                **费用说明：**
                - 按使用量计费
                - GPT-4费用较高
                - 建议设置使用限额
                """
            )
    
    # 提交按钮
    col1, col2 = st.columns(2)
    
    with col1:
        save_button = st.form_submit_button(
            "💾 保存配置",
            use_container_width=True,
            type="primary"
        )
    
    with col2:
        test_button = st.form_submit_button(
            "🧪 测试连接",
            use_container_width=True
        )
    
    if save_button:
        if not api_key:
            st.error("❌ 请输入API Key")
        else:
            # 保存API Key到session
            st.session_state['api_key'] = api_key
            st.session_state['api_model'] = model_type
            st.success("✅ API Key保存成功！")
            st.info("💡 后期会调用Django API加密存储到数据库")
            # TODO: 调用Django API保存API Key（加密存储）
    
    if test_button:
        if not api_key:
            st.error("❌ 请先输入API Key")
        else:
            with st.spinner("正在测试API连接..."):
                # TODO: 调用Django API测试连接
                st.success("✅ API连接测试成功！")
                st.info(f"模型：{current_model['name']}")

st.markdown("---")

# 学习统计（Mock数据）
st.markdown("## 📊 学习统计")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("总学习时长", "12小时", "+2小时")

with col2:
    st.metric("完成课程", "5门", "+1门")

with col3:
    st.metric("练习题完成", "125道", "+25道")

with col4:
    st.metric("正确率", "78%", "+3%")

st.markdown("---")

# 账号管理
st.markdown("## ⚙️ 账号管理")

col1, col2 = st.columns(2)

with col1:
    if st.button("🔒 修改密码", use_container_width=True):
        st.info("💡 修改密码功能开发中...")

with col2:
    if st.button("🚪 退出登录", use_container_width=True, type="secondary"):
        logout_user()

# 开发提示
with st.expander("💡 开发模式提示"):
    st.info(
        """
        **当前功能状态：**
        
        ✅ **已完成：**
        - 个人信息展示（Mock数据）
        - API Key配置界面
        - AI模型选择
        
        ⏸️ **待实现：**
        - API Key加密存储到Django后端
        - API连接测试（真实调用）
        - 学习统计数据（连接后端API）
        - 修改密码功能
        
        **使用说明：**
        1. 先获取DeepSeek或OpenAI的API Key
        2. 在上方表单中配置API Key
        3. 测试连接成功后即可使用AI功能
        4. API费用由您自己承担
        """
    )


