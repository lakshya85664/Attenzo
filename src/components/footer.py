import streamlit as st

def footer_home():
    st.markdown(f"""
    <hr style="margin-top:50px;">

<div style="text-align:center; color:white; padding:20px;">
    <p style="margin:0; font-weight:bold">Smart Attendance powered by AI</p>
    <p style="margin-top:15px; font-size:12px; font-weight:bold">
        © 2026 Attenzo. All rights reserved.
    </p>
</div>
    """, unsafe_allow_html= True)