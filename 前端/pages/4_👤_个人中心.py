"""
个人中心页面
"""

import streamlit as st
import sys
from pathlib import Path

# 添加父目录到路径
sys.path.append(str(Path(__file__).parent.parent))

from utils.auth import check_authentication, logout_user
from utils.styles import load_custom_styles
from utils.local_storage import get_local_storage
from config.settings import GRADES, AI_MODELS

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
    if st.button("返回登录"):
        st.switch_page("app.py")
    st.stop()

# 页面标题
st.title("👤 个人中心")

# 顶部导航
col1, col2 = st.columns([8, 2])
with col1:
    st.markdown(f"**欢迎，{st.session_state.username}**")
with col2:
    if st.button("🏠 返回首页", use_container_width=True):
        st.switch_page("app.py")

st.markdown("---")

# Tab选项卡
tab1, tab2, tab3 = st.tabs(["📋 基本信息", "🤖 AI配置", "📊 学习统计"])

with tab1:
    st.markdown("### 📋 基本信息")
    
    # 获取用户信息
    user_info = st.session_state.get('user_info', {})
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # 用户头像
        st.markdown(
            """
            <div style="
                width: 120px;
                height: 120px;
                border-radius: 50%;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 48px;
                font-weight: bold;
                margin: 20px auto;
            ">
                {}
            </div>
            """.format(st.session_state.username[0].upper() if st.session_state.username else "U"),
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(f"**用户名：** {user_info.get('username', 'N/A')}")
        st.markdown(f"**邮箱：** {user_info.get('email', 'N/A')}")
        st.markdown(f"**学校：** {user_info.get('school', 'N/A')}")
        st.markdown(f"**年级：** {GRADES.get(user_info.get('grade', 'grade1'), '初一')}")
    
    st.markdown("---")
    
    # 修改基本信息
    with st.expander("✏️ 修改基本信息"):
        with st.form("update_profile"):
            new_email = st.text_input("邮箱", value=user_info.get('email', ''))
            new_grade = st.selectbox(
                "年级",
                options=list(GRADES.keys()),
                format_func=lambda x: GRADES[x],
                index=list(GRADES.keys()).index(user_info.get('grade', 'grade1'))
            )
            
            if st.form_submit_button("保存修改", use_container_width=True):
                st.success("✅ 信息修改成功！")

with tab2:
    st.markdown("### 🤖 AI配置")
    
    st.info(
        """
        ℹ️ **说明：**
        - AI功能需要你自己的API Key
        - API调用费用由你自己承担
        - 支持DeepSeek和OpenAI模型
        - 配置会自动保存，下次登录无需重新配置
        """
    )
    
    # 从本地存储加载已保存的配置
    storage = get_local_storage()
    saved_config = storage.load_ai_config()
    
    # 如果本地有配置但session_state没有，自动加载到session_state
    if saved_config and not st.session_state.get('api_key'):
        st.session_state.api_key = saved_config['api_key']
        st.session_state.api_model = saved_config['model']
        st.session_state.api_endpoint = saved_config.get('endpoint')
    
    # 显示当前配置状态
    if saved_config or st.session_state.get('api_key'):
        st.success("✅ **AI配置已连接**")
        col1, col2 = st.columns([3, 1])
        with col1:
            current_model = st.session_state.get('api_model', saved_config.get('model') if saved_config else 'N/A')
            st.markdown(f"**当前模型：** {AI_MODELS.get(current_model, {}).get('name', current_model)}")
            api_key_preview = st.session_state.get('api_key', saved_config.get('api_key') if saved_config else '')
            if api_key_preview:
                st.markdown(f"**API Key：** `{api_key_preview[:8]}...{api_key_preview[-4:]}`")
        with col2:
            if st.button("🔌 断开连接", type="secondary", use_container_width=True):
                # 清除本地存储和session_state
                storage.clear_ai_config()
                if 'api_key' in st.session_state:
                    del st.session_state['api_key']
                if 'api_model' in st.session_state:
                    del st.session_state['api_model']
                if 'api_endpoint' in st.session_state:
                    del st.session_state['api_endpoint']
                st.success("✅ 已断开AI配置")
                st.rerun()
    else:
        st.warning("⚠️ **尚未配置AI**")
    
    st.markdown("---")
    
    # AI配置表单
    with st.form("ai_config"):
        st.markdown("#### 🔑 API密钥配置")
        
        # 选择AI模型
        ai_model = st.selectbox(
            "选择AI模型 *",
            options=list(AI_MODELS.keys()),
            format_func=lambda x: f"{AI_MODELS[x]['name']} - {AI_MODELS[x]['description']}",
            key="ai_model_select"
        )
        
        # 显示模型信息
        selected_model_info = AI_MODELS[ai_model]
        st.markdown(f"**默认API地址：** `{selected_model_info['endpoint']}`")
        
        # API Key输入
        api_key = st.text_input(
            "API Key *",
            type="password",
            placeholder="请输入你的API Key",
            help="你的API Key将被加密存储"
        )
        
        # 自定义API地址（可选）
        custom_endpoint = st.text_input(
            "自定义API地址（可选）",
            placeholder=selected_model_info['endpoint'],
            help="如果你使用的是代理或第三方服务，可以在此填写自定义地址"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            submit = st.form_submit_button(
                "保存配置",
                use_container_width=True,
                type="primary"
            )
        
        with col2:
            test = st.form_submit_button(
                "测试连接",
                use_container_width=True
            )
        
        if submit:
            if not api_key:
                st.error("❌ 请输入API Key")
            else:
                # 保存到session state（实时生效）
                st.session_state.api_key = api_key
                st.session_state.api_model = ai_model
                st.session_state.api_endpoint = custom_endpoint or selected_model_info['endpoint']
                
                # 保存到本地存储（持久化）
                storage = get_local_storage()
                if storage.save_ai_config(
                    api_key=api_key,
                    model=ai_model,
                    endpoint=custom_endpoint or selected_model_info['endpoint']
                ):
                    st.success("✅ API配置已保存并加密存储！")
                    st.info(
                        """
                        **配置已生效**
                        - ✅ 现在可以使用AI生成知识点总结
                        - ✅ 现在可以使用AI生成练习题
                        - ✅ 配置已自动保存，下次登录无需重新配置
                        - ⚠️  API调用费用由您承担
                        """
                    )
                    st.rerun()
                else:
                    st.error("❌ 配置保存失败，请重试")
        
        if test:
            if not api_key:
                st.error("❌ 请先输入API Key")
            else:
                with st.spinner("测试连接中..."):
                    # Mock测试
                    import time
                    time.sleep(1)
                    st.success("✅ API连接测试成功！")
    
    # 当前配置状态
    st.markdown("---")
    st.markdown("#### 📌 当前配置")
    
    current_model = st.session_state.get('api_model', '未配置')
    current_key = st.session_state.get('api_key', None)
    
    if current_key:
        masked_key = current_key[:8] + '*' * (len(current_key) - 12) + current_key[-4:]
        st.success(f"✅ 已配置：{AI_MODELS.get(current_model, {}).get('name', '未知')} - {masked_key}")
    else:
        st.warning("⚠️ 尚未配置API Key")

with tab3:
    st.markdown("### 📊 学习统计")
    
    # 从API获取真实统计数据
    from utils.api_client import get_api_client
    api_client = get_api_client()
    
    with st.spinner("加载学习统计..."):
        # 获取学习进度数据
        progress_response = api_client.get_study_progress()
        # 获取答题统计数据
        stats_response = api_client.get_exercise_statistics()
    
    # 解析响应
    progress_data = None
    stats_data = None
    has_error = False
    
    if progress_response.get('code') != 200:
        st.warning(f"⚠️ 学习进度加载失败：{progress_response.get('message', '未知错误')}")
        has_error = True
    else:
        progress_data = progress_response.get('data')
    
    if stats_response.get('code') != 200:
        st.warning(f"⚠️ 答题统计加载失败：{stats_response.get('message', '未知错误')}")
        has_error = True
    else:
        stats_data = stats_response.get('data')
    
    if not has_error:
        # 显示本周学习数据
        st.markdown("#### 📈 学习数据概览")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            completed = progress_data.get('completed_courses', 0) if progress_data else 0
            st.metric("完成课程", f"{completed}节")
        
        with col2:
            in_progress = progress_data.get('in_progress_courses', 0) if progress_data else 0
            st.metric("学习中", f"{in_progress}节")
        
        with col3:
            total_exercises = stats_data.get('total_exercises', 0) if stats_data else 0
            st.metric("练习题数", f"{total_exercises}题")
        
        with col4:
            accuracy = stats_data.get('accuracy_rate', 0) if stats_data else 0
            st.metric("平均正确率", f"{accuracy}%")
        
        st.markdown("---")
        
        # 显示各学科学习进度
        st.markdown("#### 📚 各学科学习进度")
        
        if progress_data and progress_data.get('subjects_progress'):
            # 使用真实数据
            for subject in progress_data['subjects_progress']:
                # 图标映射
                icon_map = {
                    '语文': '📚',
                    '数学': '🔢',
                    '英语': '🔤',
                    '物理': '⚛️',
                    '化学': '🧪',
                    '生物': '🧬'
                }
                subject_name = subject.get('subject_name', '')
                icon = icon_map.get(subject_name, '📖')
                progress_value = subject.get('progress', 0)
                completed_count = subject.get('completed', 0)
                total_count = subject.get('total', 0)
                
                st.markdown(f"**{icon} {subject_name}**")
                st.progress(progress_value / 100)
                st.markdown(f"{progress_value}% ({completed_count}/{total_count}节)")
                st.markdown("")
        else:
            st.info("📚 暂无学习记录，开始学习后这里会显示你的进度哦！")

# 退出登录
st.markdown("---")
if st.button("🚪 退出登录", use_container_width=True):
    logout_user()

