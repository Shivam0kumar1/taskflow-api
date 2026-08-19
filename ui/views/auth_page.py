import streamlit as st
from ui.services.auth import signup,login
from ui.services.cookies import cookies

def render_auth_page():
    tab_signup, tab_login = st.tabs(["Signup", "Login"])

    with tab_signup:
        st.subheader("Create Account")

        signup_username = st.text_input("Username", key="signup_username")
        signup_password = st.text_input(
            "Password",
            type="password",
            key="signup_password"
        )
        if st.button("Create Account"):
            response = signup(signup_username, signup_password)

            if response.status_code == 200:
                st.success("Account created successfully. You can login now.")
            else:
                detail = response.json().get("detail", "Signup failed")
                st.error(detail)

    with tab_login:
        st.subheader("Login")

        login_username = st.text_input("Username", key="login_username")
        login_password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login"):
            response = login(login_username, login_password)

            if response.status_code == 200:
                token = response.json()["access_token"]

                st.session_state["token"] = token
                st.session_state["logged_in"] = True
                st.success("Login successful.")

                cookies["token"] = token
                cookies.save()

                st.rerun()
            else:
                detail = response.json().get("detail", "Login failed")
                st.error(detail)

