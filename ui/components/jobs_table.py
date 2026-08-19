import streamlit as st

from ui.services.jobs import get_jobs

def render_jobs_table(token):
    st.header("📋 My Jobs")

    if "jobs_page" not in st.session_state:
        st.session_state["jobs_page"] = 1

    page = st.session_state["jobs_page"]

    col1,col2 = st.columns(2)

    with col1:
        limit=st.selectbox(
            "Jobs per page",
            [5,10,15],
            index = 0
        )

    with col2:
        status = st.selectbox(
            "Filter by status",
            ["All", "queued", "processing", "completed", "failed"]
        )

    status_filter = None if status == "All" else status

    response = get_jobs(
        token,
        page = page,
        limit = limit,
        status = status_filter,
    )

    if response.status_code == 200:

        jobs = response.json()

        if jobs:
            for job in jobs:
                st.subheader(f"job id: **{job["id"]}**")
                st.write(f"Title: **{job["title"]}**")
                st.write(f"Description: **{job["description"]}**")
                st.write(f"status: **{job["status"]}**")
                st.divider()
        else:
            st.info("No jobs found.")
    else:
        st.error(response.json().get("details","Unable to fetch Jobs."))

    col1, col2 = st.columns(2)

    with col1:
        if page > 1:
            if st.button("← Previous"):
                st.session_state["jobs_page"] -= 1
                st.rerun()

    with col2:
        if len(jobs)==limit:
            if st.button("Next →"):
                st.session_state["jobs_page"] += 1
                st.rerun()
