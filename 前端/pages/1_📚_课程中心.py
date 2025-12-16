"""
课程中心页面
"""

import streamlit as st
import sys
from pathlib import Path

# 添加父目录到路径
sys.path.append(str(Path(__file__).parent.parent))

from utils.auth import check_authentication, logout_user
from utils.styles import load_custom_styles
from utils.api_client import get_api_client
from config.settings import SUBJECTS, GRADES

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
    if st.button("返回登录"):
        st.switch_page("app.py")
    st.stop()

# 页面标题
st.title("📚 课程中心")

# 顶部导航
col1, col2, col3, col4 = st.columns([5, 2, 2, 1])
with col1:
    st.markdown(f"**欢迎，{st.session_state.username}**")
with col2:
    if st.button("🏠 返回首页", key="btn_home_top", use_container_width=True):
        st.switch_page("app.py")
with col3:
    if st.button("🚪 退出登录", use_container_width=True):
        logout_user()
with col4:
    # 调试模式开关
    if st.checkbox("🐛", value=st.session_state.get('debug_mode', False), help="调试模式"):
        st.session_state['debug_mode'] = True
    else:
        st.session_state['debug_mode'] = False

st.markdown("---")

# 获取当前选择的学科（默认为数学，因为只有数学有数据）
selected_subject = st.session_state.get('selected_subject')
if selected_subject is None or selected_subject not in SUBJECTS:
    selected_subject = 'math'
    st.session_state['selected_subject'] = 'math'

subject_info = SUBJECTS.get(selected_subject, SUBJECTS['math'])

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

# 初始化API客户端
api_client = get_api_client()

# 从后端API获取课程数据
with st.spinner("正在加载课程数据..."):
    response = api_client.get_courses(subject_code, grade)

# 开发调试模式（显示API返回数据）
with st.expander("🐛 调试信息（点击查看）"):
    st.write("**API基础URL:**", api_client.base_url)
    st.write("**请求参数:**", {"subject": subject_code, "grade": grade})
    st.write("**API返回数据类型:**", type(response))
    st.write("**API返回数据:**", response)
    
    # 测试连接按钮
    if st.button("🔧 测试后端连接"):
        import requests
        try:
            test_response = requests.get(f"{api_client.base_url}/courses/subjects/", timeout=5)
            st.success(f"✅ 后端连接正常！状态码: {test_response.status_code}")
            st.json(test_response.json())
        except Exception as e:
            st.error(f"❌ 后端连接失败: {str(e)}")

# 解析响应
if response.get('code') != 200:
    st.error(f"❌ 加载课程失败：{response.get('message', '未知错误')}")
    st.info("💡 请确保Django后端正在运行（http://localhost:8000）")
    courses_data = []
else:
    # 正确解析数据
    data = response.get('data', [])
    if isinstance(data, dict):
        # 如果是分页数据，提取results
        courses_data = data.get('results', [])
    elif isinstance(data, list):
        # 如果直接是列表
        courses_data = data
    else:
        courses_data = []

# 如果API返回数据为空，显示"数据整理中"提示
if not courses_data:
    st.info(f"📚 {subject_info['name']} - {GRADES[grade]}")
    st.markdown("---")
    
    # 使用友好的空状态提示
    st.markdown(
        """
        <div style="text-align: center; padding: 60px 20px;">
            <div style="font-size: 80px; margin-bottom: 20px;">📦</div>
            <h3 style="color: #666;">数据整理中</h3>
            <p style="color: #999; margin-top: 15px;">
                该学科年级的课程数据正在准备中，敬请期待...
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # 提示哪些数据已经可用
    with st.expander("💡 查看已有数据"):
        st.markdown(
            """
            **当前已上线课程：**
            - ✅ **数学 - 初一**：5门课程（七年级上册）
            
            **即将上线：**
            - ⏳ 数学 - 初二
            - ⏳ 数学 - 初三
            - ⏳ 语文 - 初一/初二/初三
            - ⏳ 英语 - 初一/初二/初三
            
            如需添加课程，请联系管理员或在Django Admin后台导入。
            """
        )
    
    # 返回首页按钮
    if st.button("🏠 返回首页", key="btn_home_no_data", use_container_width=True):
        st.switch_page("app.py")
    
    st.stop()

# 转换API数据为前端格式
mock_courses = []
try:
    for course in courses_data:
        if isinstance(course, dict):
            mock_courses.append({
                'id': course.get('id', 0),
                'title': course.get('title', '未知课程'),
                'description': course.get('outline', '暂无描述')[:100] + '...' if course.get('outline') else '暂无描述',
                'difficulty': course.get('difficulty', 'easy'),
                'progress': 0,  # TODO: 从学习进度API获取
                'status': 'not_started'  # TODO: 从学习进度API获取
            })
except Exception as e:
    st.error(f"❌ 数据解析错误：{e}")
    st.write("原始数据：", courses_data)
    st.stop()

# 以下是备用Mock数据（仅在无法连接后端时使用）
mock_courses_by_subject_backup = {
    'chinese': [
        {
            'id': 1,
            'title': '第一课：散步（莫怀戚）',
            'description': '本课讲述了一家三代人在田野上散步的故事...',
            'difficulty': 'easy',
            'progress': 60,
            'status': 'in_progress'
        },
        {
            'id': 2,
            'title': '第二课：秋天的怀念（史铁生）',
            'description': '作者通过回忆母亲，表达了对母亲深深的怀念...',
            'difficulty': 'easy',
            'progress': 0,
            'status': 'not_started'
        },
        {
            'id': 3,
            'title': '第三课：羚羊木雕（张之路）',
            'description': '讲述了一个关于友情和亲情冲突的故事...',
            'difficulty': 'medium',
            'progress': 100,
            'status': 'completed'
        },
    ],
    'math': [
        {
            'id': 1,
            'title': '第10章 整式的加减',
            'description': '学习整式的概念、同类项的合并以及整式的加法和减法运算',
            'difficulty': 'easy',
            'progress': 0,
            'status': 'not_started'
        },
        {
            'id': 2,
            'title': '第11章 整式的乘除',
            'description': '学习整式的乘法运算法则和乘法公式的应用',
            'difficulty': 'medium',
            'progress': 30,
            'status': 'in_progress'
        },
        {
            'id': 3,
            'title': '第12章 因式分解',
            'description': '学习因式分解的方法，包括提公因式法和公式法',
            'difficulty': 'medium',
            'progress': 0,
            'status': 'not_started'
        },
        {
            'id': 4,
            'title': '第13章 分式',
            'description': '学习分式的概念、基本性质以及分式的四则运算',
            'difficulty': 'hard',
            'progress': 0,
            'status': 'not_started'
        },
        {
            'id': 5,
            'title': '第14章 图形的运动',
            'description': '学习图形的三种基本运动：平移、旋转和轴对称',
            'difficulty': 'easy',
            'progress': 0,
            'status': 'not_started'
        },
    ],
    'english': [
        {
            'id': 1,
            'title': 'Unit 1: My School Life',
            'description': '介绍学校生活相关的词汇和句型...',
            'difficulty': 'easy',
            'progress': 0,
            'status': 'not_started'
        },
        {
            'id': 2,
            'title': 'Unit 2: Family and Friends',
            'description': '学习描述家人和朋友的表达方式...',
            'difficulty': 'easy',
            'progress': 0,
            'status': 'not_started'
        },
        {
            'id': 3,
            'title': 'Unit 3: Daily Routines',
            'description': '掌握日常作息和习惯的英语表达...',
            'difficulty': 'medium',
            'progress': 0,
            'status': 'not_started'
        },
    ]
}

# 显示课程列表
st.markdown("### 📖 课程列表")

if not mock_courses:
    st.info("暂无课程数据")

for course in mock_courses:
    # 状态图标
    status_icon = {
        'not_started': '⚪',
        'in_progress': '🔵',
        'completed': '✅'
    }.get(course.get('status', 'not_started'), '⚪')
    
    # 难度标签
    difficulty_map = {
        'easy': '🟢 基础',
        'medium': '🟡 进阶',
        'hard': '🔴 提高'
    }
    difficulty_label = difficulty_map.get(course.get('difficulty', 'easy'), '🟢 基础')
    
    # 课程卡片
    with st.container():
        col1, col2, col3 = st.columns([6, 2, 2])
        
        with col1:
            st.markdown(f"### {status_icon} {course['title']}")
            st.markdown(f"<p style='color: #7f8c8d;'>{course['description']}</p>", unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"**难度**：{difficulty_label}")
            if course['progress'] > 0:
                st.progress(course['progress'] / 100)
                st.markdown(f"进度：{course['progress']}%")
        
        with col3:
            st.markdown("　")  # 占位
            if st.button("📖 查看详情", key=f"course_{course['id']}", use_container_width=True):
                st.session_state['selected_course'] = course['id']
                st.switch_page("pages/2_📖_课程详情.py")
        
        st.markdown("---")

# 开发提示
with st.expander("💡 开发模式提示"):
    if subject_code == 'math':
        st.success(
            """
            **📚 数学课程数据说明：**
            - ✅ 这5门课程对应Django后端数据库中的真实数据
            - ✅ 课程内容已从PDF课本提取（共68,192字符）
            - ⏸️ 当前使用Mock显示，待连接API后将显示真实数据
            - 📖 数据来源：7上-沪教版初中数学课本（2024新版）上海.pdf
            """
        )
    else:
        st.info(
            """
            **当前显示Mock数据：**
            - 课程列表为示例数据
            - 真实数据需要连接Django后端API
            - 后期会替换为真实课程数据
            """
        )

