import streamlit as st

from ui.services.jobs import create_jobs

def render_create_jobs(token):
    with st.form("create job form", clear_on_submit=True):
        st.subheader("➕ Create Job")
        title = st.text_input("Job Title")
        description = st.text_area("Job Description")

        if st.form_submit_button("Create Job"):
            response = create_jobs(token, title, description)
            if response.status_code == 200:
                st.session_state["success_message"] = "Job created successfully!"
                st.rerun()
            else:
                st.error(response.json().get("detail","Failed to create job"))

