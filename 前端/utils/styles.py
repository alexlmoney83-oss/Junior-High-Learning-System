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
        
        /* ==================== 输入框样式 ==================== */
        
        /* 文本输入框 */
        .stTextInput > div > div > input {
            font-size: 16px !important;
            padding: 14px !important;
            min-height: 50px !important;
            border-radius: 8px !important;
        }
        
        /* 文本域 */
        .stTextArea > div > div > textarea {
            font-size: 16px !important;
            padding: 14px !important;
            min-height: 120px !important;
            border-radius: 8px !important;
        }
        
        /* 选择框 */
        .stSelectbox > div > div > select {
            font-size: 16px !important;
            padding: 12px !important;
            height: 50px !important;
            border-radius: 8px !important;
        }
        
        /* ==================== 进度条样式 ==================== */
        
        .stProgress > div > div > div {
            height: 12px !important;
            border-radius: 6px !important;
        }
        
        /* ==================== 隐藏Streamlit默认元素 ==================== */
        
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display: none;}
        
        /* ==================== 响应式设计 ==================== */
        
        /* PAD横屏 (1024px - 1366px) */
        @media (min-width: 1024px) and (max-width: 1366px) {
            .block-container {
                padding: 2rem 3rem !important;
                max-width: 100% !important;
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
        }
        
        </style>
    """, unsafe_allow_html=True)

