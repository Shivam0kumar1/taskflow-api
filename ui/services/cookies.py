import os
import streamlit as st
from dotenv import load_dotenv
from streamlit_cookies_manager import EncryptedCookieManager

load_dotenv()

cookies = EncryptedCookieManager(
    prefix="taskflow/",
    password=os.getenv("COOKIES_PASSWORD")
)

# cookies = st.session_state["cookie_manager"]

if not cookies.ready():
    st.stop()