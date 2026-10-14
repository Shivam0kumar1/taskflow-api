import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import CreateJobForm from "../components/jobs/CreateJobForm";
import UpdateJobForm from "../components/jobs/UpdateJobForm";
import DeleteJobForm from "../components/jobs/DeleteJobForm";
import JobsTable from "../components/jobs/JobsTable";

function DashboardPage() {
  const { logout } = useAuth();
  const [refreshKey, setRefreshKey] = useState(0);

  function triggerRefresh() {
    setRefreshKey((k) => k + 1);
  }

  return (
    <div>
      <button onClick={logout}>Logout</button>
      <CreateJobForm onCreated={triggerRefresh} />
      <UpdateJobForm onUpdated={triggerRefresh} />
      <DeleteJobForm onDeleted={triggerRefresh} />
      <JobsTable refreshKey={refreshKey} />
    </div>
  );
}

export default DashboardPage;