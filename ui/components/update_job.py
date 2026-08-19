import streamlit as st
from ui.services.jobs import update_jobs

def render_update_jobs(token):
    with st.form("update job form", clear_on_submit=True):
        st.subheader("📝 Update Job")

        job_id = st.text_input("Job ID")
        status = st.text_input("Job Status")

        if st.form_submit_button("Update Job"):
            response = update_jobs(token, job_id, status)
            if response.status_code == 200:
                st.session_state["success_message"] = "Job updated successfully!"
                st.rerun()
            else:
                st.error(response.json().get("detail","Failed to update job."))
