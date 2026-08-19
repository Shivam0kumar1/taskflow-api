import os
from dotenv import load_dotenv
from streamlit_cookies_manager import EncryptedCookieManager

load_dotenv()

cookies = EncryptedCookieManager(
    prefix="taskflow/",
    password=os.getenv("COOKIES_PASSWORD")
)

if not cookies.ready():
    import streamlit as st
    st.stop()