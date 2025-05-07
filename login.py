# login.py
import streamlit as st

def show_login():
    st.set_page_config(page_title="Farmer Login", layout="centered")
    st.title("👨‍🌾 Welcome to Smart Agriculture Platform")
    st.subheader("Please enter your name to continue")

    st.markdown("""
        <style>
        .stTextInput > div > div > input {
            font-size: 40px;
            padding: 10px;
        }
        .stButton > button {
            font-size: 100px;
            background-color: #4CAF50;
            color: white;
            padding: 10px 24px;
            border-radius: 8px;
        }
        </style>
    """, unsafe_allow_html=True)

    farmer_name = st.text_input("👤 Farmer Name", "")

    if st.button("Login"):
        if farmer_name.strip():
            st.session_state["farmer_name"] = farmer_name.strip()
            st.experimental_rerun()
        else:
            st.warning("Please enter your name before proceeding.")
