import os
from streamlit_cookies_manager import EncryptedCookieManager

cookies = EncryptedCookieManager(
    prefix="taskflow/",
    password=os.getenv("COOKIES_PASSWORD", "taskflow-dev-cookie-secret")
)

if not cookies.ready():
    import streamlit as st
    st.stop()