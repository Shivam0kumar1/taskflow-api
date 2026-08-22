import streamlit as st

from ui.components.jobs_table import render_jobs_table
from ui.components.create_job import render_create_jobs
from ui.components.update_job import render_update_jobs
from ui.components.delete_job import render_delete_job
from ui.services.cookies import cookies


def render_dashboard():

    col1,col2 = st.columns([6,1])

    with col2:
        if st.button("Logout"):
            """ These logics are known issue of streamlit library related to cookie deletion, hence we need to apply another logic 
            cookies.pop("token", None)
            if "token" in cookies:
                del cookies["token"]
            """
            cookies["token"] = ""
            cookies.save()
            st.session_state.clear()
            st.rerun()

    token = st.session_state["token"]
    if "success_message" in st.session_state:
        st.success(st.session_state["success_message"])
        del st.session_state["success_message"]
    st.divider()

    render_create_jobs(token)
    render_update_jobs(token)
    render_delete_job(token)
    render_jobs_table(token)