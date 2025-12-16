"""
课程详情页面
"""

import streamlit as st
import sys
from pathlib import Path

# 添加父目录到路径
sys.path.append(str(Path(__file__).parent.parent))

from utils.auth import check_authentication, logout_user
from utils.styles import load_custom_styles
from utils.api_client import get_api_client
from utils.local_storage import load_api_config_to_session
from config.settings import SUBJECTS, GRADES

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
    if st.button("返回登录"):
        st.switch_page("app.py")
    st.stop()

# 从本地存储加载API配置（如果有）
load_api_config_to_session()

# 页面标题
st.title("📖 课程详情")

# 顶部导航
col1, col2, col3 = st.columns([6, 2, 2])
with col1:
    st.markdown(f"**欢迎，{st.session_state.username}**")
with col2:
    if st.button("◀️ 返回列表", use_container_width=True):
        st.switch_page("pages/1_📚_课程中心.py")
with col3:
    if st.button("🏠 返回首页", use_container_width=True):
        st.switch_page("app.py")

st.markdown("---")

# 获取课程ID和学科
course_id = st.session_state.get('selected_course', 1)
selected_subject = st.session_state.get('selected_subject', 'chinese')

# 初始化API客户端
api_client = get_api_client()

# 从后端API获取课程详情
with st.spinner("正在加载课程详情..."):
    course_detail, error = api_client.get_course_detail(course_id)

if error or not course_detail:
    st.error(f"❌ 加载课程详情失败：{error if error else '课程不存在'}")
    st.info("💡 请确保Django后端正在运行，或返回课程列表重新选择")
    if st.button("返回课程列表"):
        st.switch_page("pages/1_📚_课程中心.py")
    st.stop()

# 转换API数据为前端格式
mock_course = {
    'id': course_detail['id'],
    'title': course_detail['title'],
    'subject': course_detail.get('subject', {}).get('code', 'math'),
    'grade': course_detail.get('grade', 'grade1'),
    'difficulty': course_detail.get('difficulty', 'easy'),
    'description': course_detail.get('outline', '暂无课程简介')[:200],
    'outline': course_detail.get('outline', '').split('\n')[:5] if course_detail.get('outline') else ['暂无大纲'],
    'keywords': course_detail.get('keywords', '').split(',') if course_detail.get('keywords') else [],
    'progress': 0,  # TODO: 从学习进度API获取
    'has_content': course_detail.get('has_content', False),  # 后端返回的has_content字段
    'pdf_source': course_detail.get('pdf_source', ''),
    'pdf_page_range': course_detail.get('pdf_page_range', ''),
}

# 以下是备用Mock数据（仅在无法连接后端时使用）
mock_courses_db_backup = {
    'chinese': {
        1: {
            'title': '第一课：散步（莫怀戚）',
            'description': '本课讲述了一家三代人在田野上散步的故事，展现了浓浓的亲情和人生的选择。',
            'outline': ['一、作者简介', '二、字词积累', '三、课文理解', '四、写作手法', '五、主题思想'],
            'keywords': ['散文', '亲情', '选择', '责任', '人物描写', '环境描写'],
            'difficulty': 'easy',
            'progress': 60
        },
        2: {
            'title': '第二课：秋天的怀念（史铁生）',
            'description': '作者通过回忆母亲，表达了对母亲深深的怀念和愧疚之情。',
            'outline': ['一、作者简介', '二、文章背景', '三、情感分析', '四、重点段落赏析', '五、写作特色'],
            'keywords': ['回忆', '母爱', '愧疚', '生命', '坚强'],
            'difficulty': 'easy',
            'progress': 0
        },
        3: {
            'title': '第三课：羚羊木雕（张之路）',
            'description': '讲述了一个关于友情和亲情冲突的故事，引发对人际关系的思考。',
            'outline': ['一、故事梗概', '二、人物分析', '三、冲突解析', '四、主题探讨', '五、语言特点'],
            'keywords': ['友情', '亲情', '冲突', '诚信', '成长'],
            'difficulty': 'medium',
            'progress': 100
        },
    },
    'math': {
        1: {
            'title': '第10章 整式的加减',
            'description': '学习整式的概念、同类项的合并以及整式的加法和减法运算，掌握去括号、添括号的法则。',
            'outline': ['10.1 整式', '10.2 合并同类项', '10.3 整式的加法和减法', '内容提要', '复习题'],
            'keywords': ['整式', '单项式', '多项式', '同类项', '合并同类项', '整式加减'],
            'difficulty': 'easy',
            'progress': 0
        },
        2: {
            'title': '第11章 整式的乘除',
            'description': '学习整式的乘法运算法则，包括幂的运算、同底数幂的乘除、乘法公式（平方差、完全平方）的应用。',
            'outline': ['11.1 整式的乘法', '11.2 乘法公式', '内容提要', '复习题'],
            'keywords': ['整式乘法', '幂的运算', '同底数幂', '积的乘方', '乘法公式', '完全平方公式'],
            'difficulty': 'medium',
            'progress': 30
        },
        3: {
            'title': '第12章 因式分解',
            'description': '学习因式分解的概念和方法，掌握提公因式法、公式法（平方差、完全平方）等技巧。',
            'outline': ['12.1 因式分解', '12.2 提公因式法', '12.3 公式法', '内容提要', '复习题'],
            'keywords': ['因式分解', '提公因式法', '平方差公式', '完全平方公式', '分组分解法'],
            'difficulty': 'medium',
            'progress': 0
        },
        4: {
            'title': '第13章 分式',
            'description': '学习分式的概念、基本性质，掌握分式的四则运算和分式方程的解法。',
            'outline': ['13.1 分式', '13.2 分式的运算', '13.3 分式方程', '内容提要', '复习题'],
            'keywords': ['分式', '分式的性质', '约分', '通分', '分式运算', '分式方程'],
            'difficulty': 'hard',
            'progress': 0
        },
        5: {
            'title': '第14章 图形的运动',
            'description': '学习图形的三种基本运动：平移、旋转和轴对称，理解图形变换的性质和应用。',
            'outline': ['14.1 平移', '14.2 旋转', '14.3 轴对称', '内容提要', '复习题'],
            'keywords': ['平移', '旋转', '轴对称', '图形变换', '对称轴', '中心对称'],
            'difficulty': 'easy',
            'progress': 0
        },
    },
    'english': {
        1: {
            'title': 'Unit 1: My School Life',
            'description': '介绍学校生活相关的词汇和句型，学习如何用英语描述校园活动。',
            'outline': ['Vocabulary', 'Grammar: Present Simple', 'Reading', 'Speaking Practice', 'Writing'],
            'keywords': ['school', 'subjects', 'activities', 'daily routine'],
            'difficulty': 'easy',
            'progress': 0
        },
    }
}

# 学科和年级信息
subject_info = SUBJECTS.get(mock_course['subject'], SUBJECTS['chinese'])
grade_name = GRADES.get(mock_course['grade'], '初一')

# 课程标题卡片
st.markdown(
    f"""
    <div style="
        background: linear-gradient(135deg, {subject_info['color']} 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 12px;
        color: white;
        margin-bottom: 20px;
    ">
        <h2>{subject_info['icon']} {mock_course['title']}</h2>
        <p style="font-size: 16px; margin-top: 10px;">{mock_course['description']}</p>
        <div style="margin-top: 15px;">
            <span style="background: rgba(255,255,255,0.2); padding: 5px 15px; border-radius: 20px; margin-right: 10px;">
                {subject_info['name']}
            </span>
            <span style="background: rgba(255,255,255,0.2); padding: 5px 15px; border-radius: 20px; margin-right: 10px;">
                {grade_name}
            </span>
            <span style="background: rgba(255,255,255,0.2); padding: 5px 15px; border-radius: 20px;">
                🟢 基础
            </span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# 学习进度
st.markdown("### 📊 学习进度")
st.progress(mock_course['progress'] / 100)
st.markdown(f"已完成 {mock_course['progress']}%")

st.markdown("---")

# 课程大纲
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📚 课程大纲")
    for item in mock_course['outline']:
        st.markdown(f"- {item}")

with col2:
    st.markdown("### 🏷️ 知识点标签")
    for keyword in mock_course['keywords']:
        st.markdown(f"`{keyword}`", unsafe_allow_html=True)

st.markdown("---")

# 操作按钮
col1, col2, col3 = st.columns(3)

# 检查用户是否配置了AI API Key
has_api_key = st.session_state.get('api_key') is not None

with col1:
    if st.button("📝 查看知识总结", use_container_width=True, type="primary"):
        if not has_api_key:
            st.warning("⚠️ 请先在【个人中心】配置AI API Key")
            st.info("知识点总结需要调用AI大模型生成，请先配置您的API Key")
        elif not mock_course.get('has_content'):
            st.warning("⚠️ 该课程暂无课本内容")
            st.info("需要先导入课本PDF内容，AI才能基于真实内容生成知识点总结")
        else:
            # 生成知识点总结
            with st.spinner("🤖 AI正在生成知识点总结..."):
                api_key = st.session_state.get('api_key')
                model = st.session_state.get('api_model', 'deepseek-r1')
                summary, error = api_client.generate_knowledge_summary(course_id, api_key, model)
                
                if error:
                    st.error(f"❌ 生成失败：{error}")
                else:
                    st.success("✅ 知识点总结生成成功！")
                    st.markdown(summary.get('content', ''))

with col2:
    if st.button("✍️ 开始练习", use_container_width=True, type="primary"):
        if not has_api_key:
            st.warning("⚠️ 请先在【个人中心】配置AI API Key")
            st.info("练习题需要AI大模型生成，请先配置您的API Key")
        else:
            st.session_state['selected_course'] = course_id
            st.session_state['selected_course_has_content'] = mock_course.get('has_content', False)
            st.switch_page("pages/3_✍️_智能练习.py")

with col3:
    if st.button("📈 学习统计", use_container_width=True):
        st.info("📊 学习统计功能即将上线...")

# 课程来源信息
if mock_course.get('pdf_source'):
    with st.expander("📄 课本来源信息"):
        st.markdown(f"""
        **PDF来源：** {mock_course['pdf_source']}
        
        **页码范围：** {mock_course['pdf_page_range']}
        
        **内容状态：** {'✅ 已导入课本内容' if mock_course.get('has_content') else '⚠️ 暂无课本内容'}
        """)

