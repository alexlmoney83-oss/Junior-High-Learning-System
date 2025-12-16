"""
虚拟数学键盘组件
适用于数学练习答题，方便输入数学符号
"""

import streamlit as st


def render_math_keyboard(answer_key: str = "user_answer"):
    """
    渲染虚拟数学键盘
    
    Args:
        answer_key: session_state中存储答案的键名
    """
    
    # 确保session_state中有答案字段
    if answer_key not in st.session_state:
        st.session_state[answer_key] = ""
    
    # 显示当前答案（可编辑）
    st.markdown("### ✍️ 你的答案")
    current_answer = st.text_input(
        "输入答案（可使用下方键盘）",
        value=st.session_state[answer_key],
        key=f"{answer_key}_display",
        placeholder="点击下方按钮输入，或直接在此输入",
        label_visibility="collapsed"
    )
    
    # 更新session_state
    st.session_state[answer_key] = current_answer
    
    st.markdown("---")
    st.markdown("### 🎹 数学键盘")
    
    # ==================== 数字和基础运算符 ====================
    st.markdown("#### 数字和基础运算")
    
    # 第一行：7 8 9 ÷ ← ( )
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    with col1:
        if st.button("7", key="key_7", use_container_width=True):
            st.session_state[answer_key] += "7"
            st.rerun()
    with col2:
        if st.button("8", key="key_8", use_container_width=True):
            st.session_state[answer_key] += "8"
            st.rerun()
    with col3:
        if st.button("9", key="key_9", use_container_width=True):
            st.session_state[answer_key] += "9"
            st.rerun()
    with col4:
        if st.button("÷", key="key_div", use_container_width=True):
            st.session_state[answer_key] += "÷"
            st.rerun()
    with col5:
        if st.button("⌫", key="key_back", use_container_width=True):
            if st.session_state[answer_key]:
                st.session_state[answer_key] = st.session_state[answer_key][:-1]
                st.rerun()
    with col6:
        if st.button("(", key="key_lparen", use_container_width=True):
            st.session_state[answer_key] += "("
            st.rerun()
    with col7:
        if st.button(")", key="key_rparen", use_container_width=True):
            st.session_state[answer_key] += ")"
            st.rerun()
    
    # 第二行：4 5 6 × x y z
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    with col1:
        if st.button("4", key="key_4", use_container_width=True):
            st.session_state[answer_key] += "4"
            st.rerun()
    with col2:
        if st.button("5", key="key_5", use_container_width=True):
            st.session_state[answer_key] += "5"
            st.rerun()
    with col3:
        if st.button("6", key="key_6", use_container_width=True):
            st.session_state[answer_key] += "6"
            st.rerun()
    with col4:
        if st.button("×", key="key_mul", use_container_width=True):
            st.session_state[answer_key] += "×"
            st.rerun()
    with col5:
        if st.button("x", key="key_x", use_container_width=True):
            st.session_state[answer_key] += "x"
            st.rerun()
    with col6:
        if st.button("y", key="key_y", use_container_width=True):
            st.session_state[answer_key] += "y"
            st.rerun()
    with col7:
        if st.button("z", key="key_z", use_container_width=True):
            st.session_state[answer_key] += "z"
            st.rerun()
    
    # 第三行：1 2 3 - = a b
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    with col1:
        if st.button("1", key="key_1", use_container_width=True):
            st.session_state[answer_key] += "1"
            st.rerun()
    with col2:
        if st.button("2", key="key_2", use_container_width=True):
            st.session_state[answer_key] += "2"
            st.rerun()
    with col3:
        if st.button("3", key="key_3", use_container_width=True):
            st.session_state[answer_key] += "3"
            st.rerun()
    with col4:
        # 使用更明确的标签避免显示问题
        if st.button("➖", key="key_minus", help="减号 -", use_container_width=True):
            st.session_state[answer_key] += "-"
            st.rerun()
    with col5:
        if st.button("=", key="key_equal", use_container_width=True):
            st.session_state[answer_key] += "="
            st.rerun()
    with col6:
        if st.button("a", key="key_a", use_container_width=True):
            st.session_state[answer_key] += "a"
            st.rerun()
    with col7:
        if st.button("b", key="key_b", use_container_width=True):
            st.session_state[answer_key] += "b"
            st.rerun()
    
    # 第四行：0 . 清空 + √ ± 空格
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    with col1:
        if st.button("0", key="key_0", use_container_width=True):
            st.session_state[answer_key] += "0"
            st.rerun()
    with col2:
        if st.button(".", key="key_dot", use_container_width=True):
            st.session_state[answer_key] += "."
            st.rerun()
    with col3:
        if st.button("清空", key="key_clear", use_container_width=True, type="secondary"):
            st.session_state[answer_key] = ""
            st.rerun()
    with col4:
        # 使用更明确的标签避免显示问题
        if st.button("➕", key="key_plus", help="加号 +", use_container_width=True):
            st.session_state[answer_key] += "+"
            st.rerun()
    with col5:
        if st.button("√", key="key_sqrt", use_container_width=True):
            st.session_state[answer_key] += "√"
            st.rerun()
    with col6:
        if st.button("±", key="key_pm", help="正负号", use_container_width=True):
            st.session_state[answer_key] += "±"
            st.rerun()
    with col7:
        if st.button("空格", key="key_space", use_container_width=True):
            st.session_state[answer_key] += " "
            st.rerun()
    
    st.markdown("---")
    
    # ==================== 常用模板 ====================
    st.markdown("#### 快捷模板")
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        if st.button("x²", key="template_square", use_container_width=True):
            st.session_state[answer_key] += "²"
            st.rerun()
    
    with col2:
        if st.button("x³", key="template_cube", use_container_width=True):
            st.session_state[answer_key] += "³"
            st.rerun()
    
    with col3:
        if st.button("x^n", key="template_power", use_container_width=True):
            st.session_state[answer_key] += "^"
            st.rerun()
            
    with col4:
        if st.button("√(  )", key="template_sqrt_paren", use_container_width=True):
            st.session_state[answer_key] += "√()"
            st.rerun()
    
    with col5:
        if st.button("(  )/( )", key="template_fraction", use_container_width=True):
            st.session_state[answer_key] += "()/()"
            st.rerun()
    
    with col6:
        if st.button("(  )²", key="template_square_paren", use_container_width=True):
            st.session_state[answer_key] += "()²"
            st.rerun()
    
    # 第二行模板
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        if st.button("≠", key="template_neq", use_container_width=True):
            st.session_state[answer_key] += "≠"
            st.rerun()
    
    with col2:
        if st.button("≥", key="template_geq", use_container_width=True):
            st.session_state[answer_key] += "≥"
            st.rerun()
    
    with col3:
        if st.button("≤", key="template_leq", use_container_width=True):
            st.session_state[answer_key] += "≤"
            st.rerun()
    
    with col4:
        # 使用转义或特殊字符避免markdown冲突
        if st.button("＞", key="template_gt", help="大于号 >", use_container_width=True):
            st.session_state[answer_key] += ">"
            st.rerun()
    
    with col5:
        if st.button("＜", key="template_lt", help="小于号 <", use_container_width=True):
            st.session_state[answer_key] += "<"
            st.rerun()
    
    with col6:
        if st.button("π", key="template_pi", use_container_width=True):
            st.session_state[answer_key] += "π"
            st.rerun()
    
    # ==================== 输入提示 ====================
    with st.expander("💡 输入提示", expanded=False):
        st.markdown("""
        **快捷输入说明：**
        
        - **平方/立方**：点击 `x²` `x³` 按钮
        - **高次方**：点击 `x^n` 后输入数字，如 `x^5`
        - **根式**：点击 `√(  )` 后在括号内输入
        - **分式**：点击 `(  )/( )` 模板，在括号内输入分子和分母
        - **括号的平方**：点击 `(  )²` 后在括号内输入
        
        **按钮说明：**
        
        - `➕` = 加号 `+`
        - `➖` = 减号 `-`
        - `±` = 正负号
        - `＞` = 大于号 `>`
        - `＜` = 小于号 `<`
        
        **等价输入方式：**
        
        - `x²` = `x^2` （系统自动识别）
        - `x³` = `x^3`
        - `×` = `*` （乘号）
        - `÷` = `/` （除号）
        
        **AI智能判题：**
        
        系统会智能判断答案的数学等价性，以下形式都视为正确：
        - `(x+1)²` = `x²+2x+1` = `(x+1)(x+1)`
        - `2/3` = `2÷3`
        - 顺序不同也可以：`x+1` = `1+x`
        """)
    
    return st.session_state[answer_key]


def get_math_answer(answer_key: str = "user_answer") -> str:
    """
    获取用户输入的数学答案
    
    Args:
        answer_key: session_state中存储答案的键名
    
    Returns:
        str: 用户输入的答案
    """
    return st.session_state.get(answer_key, "")


def clear_math_answer(answer_key: str = "user_answer"):
    """
    清空数学答案
    
    Args:
        answer_key: session_state中存储答案的键名
    """
    st.session_state[answer_key] = ""

