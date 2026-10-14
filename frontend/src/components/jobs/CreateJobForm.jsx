import { useState } from "react";
import { createJob } from "../../api/jobs";
import { useAuth } from "../../context/AuthContext";

function CreateJobForm({ onCreated }) {
  const { token } = useAuth();
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setIsSubmitting(true);

    try {
      const response = await createJob(token, title.trim(), description.trim());

      if (response.ok) {
        setTitle("");
        setDescription("");
        onCreated();
      } else {
        const data = await response.json();
        setError(
          typeof data.detail === "string" ? data.detail : "Failed to create job."
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
      <h2>Create Job</h2>

      <label htmlFor="job-title">Title</label>
      <input
        id="job-title"
        type="text"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        required
      />

      <label htmlFor="job-description">Description</label>
      <textarea
        id="job-description"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        required
      />

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? "Creating..." : "Create Job"}
      </button>

      {error && <p>{error}</p>}
    </form>
  );
}

export default CreateJobForm;