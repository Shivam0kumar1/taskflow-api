import streamlit as st
from ui.views.auth_page import render_auth_page
from ui.views.dashboard_page import render_dashboard
from ui.services.cookies import cookies

st.set_page_config(
    page_title="Taskflow",
    page_icon ="📋",
    layout="wide"
)

st.title("📋 Taskflow")
st.write("Welcome to Taskflow")

if (not st.session_state.get("logged_in") and cookies.get("token")):
    st.session_state["logged_in"] = True
    st.session_state["token"] = cookies["token"]

if st.session_state.get("logged_in"):
    render_dashboard()
else:
    render_auth_page()

