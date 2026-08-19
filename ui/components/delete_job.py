import streamlit as st

from ui.services.jobs import delete_jobs

def render_delete_job(token):
    with st.form("delete job form", clear_on_submit=True):
        st.subheader("🗑️ Delete Job")

        delete_job_id = st.text_input("Job ID to be delete")
        if st.form_submit_button("Delete Job"):
            response = delete_jobs(token, delete_job_id)
            if response.status_code == 200:
                st.session_state["success_message"] = "Job deleted successfully!"
                st.rerun()
            else:
                detail = response.json().get("detail","Failed to delete job.")
                st.error(detail)
