import { useEffect, useState } from "react";
import { getJobs } from "../../api/jobs";
import { useAuth } from "../../context/AuthContext";

function JobsTable() {
  const { token } = useAuth();
  const [jobs, setJobs] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadJobs() {
      const response = await getJobs(token);
      const data = await response.json();

      if (response.status === 200) {
        setJobs(data);
      } else {
        setError(data.detail || "Unable to fetch jobs.");
      }
    }

    loadJobs();
  }, [token]);

  return (
    <div>
      <h2>My Jobs</h2>

      {error && <p>{error}</p>}

      {jobs.length === 0 && !error && <p>No jobs found.</p>}

      {jobs.map((job) => (
        <div key={job.id}>
          <h3>Job ID: {job.id}</h3>
          <p>Title: {job.title}</p>
          <p>Description: {job.description}</p>
          <p>Status: {job.status}</p>
          <hr />
        </div>
      ))}
    </div>
  );
}

export default JobsTable;