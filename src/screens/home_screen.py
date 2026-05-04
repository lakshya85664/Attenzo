import streamlit as st
from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout, style_base_home

def home_screen():

    header_home()
    style_base_layout()
    style_base_home()
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.header("I'm Student")
        st.image("E:/Major_AI_Projects/Attenzo/src/components/images/student.svg", width=120)
        if st.button('Student Portal', type='primary', icon=':material/arrow_outward:'):
            st.session_state['login_type'] = 'student'
            st.rerun()

    with col2:
        st.header("I'm teacher")
        st.image("E:/Major_AI_Projects/Attenzo/src/components/images/teacher.svg", width=120)
        if st.button('Teacher Portal', type='primary', icon=':material/arrow_outward:'):
            st.session_state['login_type'] = 'teacher'
            st.rerun()

    footer_home()
        
