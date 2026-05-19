import streamlit as st
import base64

def header_home():
    with open("src/components/logo.jpg", "rb") as f:
        data = base64.b64encode(f.read()).decode()
    st.markdown(f"""
    <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; margin-bottom:30px; margin-top:30px; width:100%;">
        <img src="data:image/jpeg;base64,{data}" height="100" style="display:block; margin:0 auto; border-radius: 10px;">
        <h1 style='text-align:center; margin-left:20px'>Attenzo</h1>
    </div>
    """, unsafe_allow_html= True)

def header_dashboard():
    with open("src/components/logo.jpg", "rb") as f:
        data = base64.b64encode(f.read()).decode()
    st.markdown(f"""
    <div style="display:flex; align-items:center; justify-content:center; gap:15px; margin-bottom:10px;">
        <img src="data:image/jpeg;base64,{data}" height="95px;" style="display:block; border-radius: 10px;">
        <h2 style='text-align:left; color:#5865F2;'>Attenzo</h2>
    </div>
    """, unsafe_allow_html= True)