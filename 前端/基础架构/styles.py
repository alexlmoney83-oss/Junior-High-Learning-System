"""
自定义样式 - PAD适配优化
"""

import streamlit as st


def load_custom_styles():
    """加载自定义CSS样式，优化PAD端体验"""
    
    st.markdown("""
        <style>
        /* ==================== 全局样式 ==================== */
        
        /* 全局字体增大 */
        html, body, [class*="css"] {
            font-size: 16px !important;
        }
        
        /* ==================== 按钮样式 ==================== */
        
        /* 所有按钮统一增大 */
        .stButton > button {
            height: 60px !important;
            font-size: 18px !important;
            padding: 12px 24px !important;
            min-width: 140px !important;
            border-radius: 8px !important;
            font-weight: 500 !important;
            transition: all 0.2s ease !important;
        }
        
        /* 按钮触摸反馈 */
        .stButton > button:active {
            transform: scale(0.98) !important;
            opacity: 0.8 !important;
        }
        
        /* 主要按钮样式 */
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border: none !important;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4) !important;
        }
        
        .stButton > button[kind="primary"]:hover {
            box-shadow: 0 6px 16px rgba(102, 126, 234, 0.6) !important;
        }
        
        /* 次要按钮样式 */
        .stButton > button[kind="secondary"] {
            background: white !important;
            color: #667eea !important;
            border: 2px solid #667eea !important;
        }
        
        /* ==================== 输入框样式 ==================== */
        
        /* 文本输入框 */
        .stTextInput > div > div > input {
            font-size: 16px !important;
            padding: 14px !important;
            min-height: 50px !important;
            border-radius: 8px !important;
            border: 2px solid #e0e0e0 !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #667eea !important;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        }
        
        /* 文本域 */
        .stTextArea > div > div > textarea {
            font-size: 16px !important;
            padding: 14px !important;
            min-height: 120px !important;
            border-radius: 8px !important;
            border: 2px solid #e0e0e0 !important;
        }
        
        .stTextArea > div > div > textarea:focus {
            border-color: #667eea !important;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        }
        
        /* 选择框 */
        .stSelectbox > div > div > select {
            font-size: 16px !important;
            padding: 12px !important;
            height: 50px !important;
            border-radius: 8px !important;
        }
        
        /* ==================== 卡片样式 ==================== */
        
        /* 课程卡片 */
        .course-card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
            cursor: pointer;
            min-height: 120px;
        }
        
        .course-card:hover {
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
            transform: translateY(-2px);
        }
        
        .course-card:active {
            transform: translateY(0);
        }
        
        .course-card-title {
            font-size: 20px;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 8px;
        }
        
        .course-card-meta {
            font-size: 14px;
            color: #7f8c8d;
        }
        
        /* 学科卡片 */
        .subject-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 16px;
            padding: 30px 20px;
            text-align: center;
            min-height: 180px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }
        
        .subject-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }
        
        .subject-card:active {
            transform: translateY(-2px);
        }
        
        .subject-card-icon {
            font-size: 48px;
            margin-bottom: 12px;
        }
        
        .subject-card-name {
            font-size: 24px;
            font-weight: 600;
        }
        
        /* ==================== 进度条样式 ==================== */
        
        .stProgress > div > div > div {
            height: 12px !important;
            border-radius: 6px !important;
        }
        
        /* ==================== 侧边栏样式 ==================== */
        
        [data-testid="stSidebar"] {
            background: #f8f9fa;
            padding-top: 20px;
        }
        
        [data-testid="stSidebar"] > div:first-child {
            width: 300px !important;
        }
        
        /* ==================== 隐藏Streamlit默认元素 ==================== */
        
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* 隐藏部署按钮 */
        .stDeployButton {display: none;}
        
        /* ==================== 响应式设计 ==================== */
        
        /* PAD横屏 (1024px - 1366px) */
        @media (min-width: 1024px) and (max-width: 1366px) {
            .block-container {
                padding: 2rem 3rem !important;
                max-width: 100% !important;
            }
            
            .stButton > button {
                height: 60px !important;
                font-size: 18px !important;
            }
        }
        
        /* PAD竖屏 (768px - 1023px) */
        @media (min-width: 768px) and (max-width: 1023px) {
            .block-container {
                padding: 1.5rem 2rem !important;
            }
            
            .stButton > button {
                height: 56px !important;
                font-size: 17px !important;
            }
            
            .course-card {
                padding: 16px;
                min-height: 100px;
            }
            
            .subject-card {
                padding: 24px 16px;
                min-height: 150px;
            }
            
            .subject-card-icon {
                font-size: 40px;
            }
            
            .subject-card-name {
                font-size: 20px;
            }
        }
        
        /* 小屏平板/大屏手机 (480px - 767px) */
        @media (max-width: 767px) {
            .block-container {
                padding: 1rem !important;
            }
            
            .stButton > button {
                height: 52px !important;
                font-size: 16px !important;
                width: 100% !important;
            }
            
            .course-card {
                padding: 12px;
                min-height: 80px;
            }
            
            .course-card-title {
                font-size: 18px;
            }
            
            .subject-card {
                padding: 20px 12px;
                min-height: 120px;
            }
            
            .subject-card-icon {
                font-size: 36px;
            }
            
            .subject-card-name {
                font-size: 18px;
            }
        }
        
        /* ==================== 虚拟键盘适配 ==================== */
        
        /* 输入框获得焦点时的样式 */
        input:focus, textarea:focus, select:focus {
            scroll-margin-top: 100px;
        }
        
        /* ==================== 加载动画 ==================== */
        
        .loading-spinner {
            display: inline-block;
            width: 40px;
            height: 40px;
            border: 4px solid rgba(102, 126, 234, 0.2);
            border-top-color: #667eea;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        /* ==================== 提示消息样式 ==================== */
        
        .stAlert {
            border-radius: 8px !important;
            padding: 16px !important;
            font-size: 16px !important;
        }
        
        </style>
    """, unsafe_allow_html=True)

