import { useState } from "react";
import { updateJob } from "../../api/jobs";
import { useAuth } from "../../context/AuthContext";

const STATUS_OPTIONS = ["processing", "completed", "failed"];

function UpdateJobForm({ onUpdated }) {
  const { token } = useAuth();
  const [jobId, setJobId] = useState("");
  const [status, setStatus] = useState(STATUS_OPTIONS[0]);
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setIsSubmitting(true);

    try {
      const response = await updateJob(token, jobId.trim(), status);

      if (response.ok) {
        setJobId("");
        onUpdated();
      } else {
        const data = await response.json();
        setError(
          typeof data.detail === "string" ? data.detail : "Failed to update job."
        );
      }
    } catch {
      setError("Cannot reach the server. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <h2>Update Job</h2>

      <label htmlFor="update-job-id">Job ID</label>
      <input
        id="update-job-id"
        type="text"
        value={jobId}
        onChange={(e) => setJobId(e.target.value)}
        required
      />

      <label htmlFor="update-status">New Status</label>
      <select
        id="update-status"
        value={status}
        onChange={(e) => setStatus(e.target.value)}
      >
        {STATUS_OPTIONS.map((option) => (
          <option key={option} value={option}>
            {option}
          </option>
        ))}
      </select>

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? "Updating..." : "Update Job"}
      </button>

      {error && <p>{error}</p>}
    </form>
  );
}

export default UpdateJobForm;