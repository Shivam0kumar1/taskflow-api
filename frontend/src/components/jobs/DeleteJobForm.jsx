import { useState } from "react";
import { deleteJob } from "../../api/jobs";
import { useAuth } from "../../context/AuthContext";

function DeleteJobForm({ onDeleted }) {
  const { token } = useAuth();
  const [jobId, setJobId] = useState("");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setIsSubmitting(true);

    try {
      const response = await deleteJob(token, jobId.trim());

      if (response.ok) {
        setJobId("");
        onDeleted();
      } else {
        const data = await response.json();
        setError(
          typeof data.detail === "string" ? data.detail : "Failed to delete job."
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
      <h2>Delete Job</h2>

      <label htmlFor="delete-job-id">Job ID</label>
      <input
        id="delete-job-id"
        type="text"
        value={jobId}
        onChange={(e) => setJobId(e.target.value)}
        required
      />

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? "Deleting..." : "Delete Job"}
      </button>

      {error && <p>{error}</p>}
    </form>
  );
}

export default DeleteJobForm;