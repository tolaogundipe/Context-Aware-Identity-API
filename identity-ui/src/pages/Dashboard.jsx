import { getContexts } from "../api/contextApi";
import { useEffect, useState } from "react";
import ResolveIdentity from "../components/ResolveIdentity";
import { getAuditLogs } from "../api/auditApi";
import UpdateDisplayName from "../components/UpdateDisplayName";
import { getCurrentUser } from "../services/authService";


// dashboard component
// main ui that brings together contexts, identity resolution,
// user info, and audit logs
function Dashboard() {

  // store application state
  const [contexts, setContexts] = useState([]);
  const [auditLogs, setAuditLogs] = useState([]);
  const [currentUser, setCurrentUser] = useState(null);

  // extract role name for access control
  const roleName = currentUser?.role?.name || currentUser?.role;


  // load data on component mount
  // fetches contexts, audit logs, and current user
  useEffect(() => {

    // fetch all available contexts
    async function loadContexts() {
      const data = await getContexts();
      setContexts(data.results ? data.results : data);
    }

    // fetch audit logs only for registry officer
    async function loadAuditLogs() {
      if (roleName === "Registry Officer") {
        const logs = await getAuditLogs();
        setAuditLogs(logs.results ? logs.results : logs);
      }
    }

    // fetch current logged-in user
    async function loadCurrentUser() {
      try {
        const token = localStorage.getItem("access");
        const user = await getCurrentUser(token);
        setCurrentUser(user);
      } catch (error) {
        console.error("Failed to load user:", error);
      }
    }

    loadContexts();
    loadAuditLogs();
    loadCurrentUser();
   
  }, [roleName]);


  // render dashboard ui
  // includes sidebar, user info, contexts, identity features,
  // and audit logs with role-based visibility
  return (
    <div className="flex min-h-screen bg-gray-100">

      {/* SIDEBAR */}
      <div className="w-64 bg-gray-900 text-white p-6">
        <h2 className="text-xl font-bold mb-8">Identity System</h2>

        <ul className="space-y-4 text-sm">
          <li className="hover:text-blue-400 cursor-pointer">Dashboard</li>
          <li className="hover:text-blue-400 cursor-pointer">Contexts</li>
          <li className="hover:text-blue-400 cursor-pointer">Audit Logs</li>
        </ul>
      </div>

      {/* MAIN CONTENT */}
      <div className="flex-1 p-10">

        {/* HEADER */}
        <h1 className="text-3xl font-bold mb-2 text-gray-800">
          Dashboard
        </h1>

        {/* CURRENT USER INFO */}
        {currentUser && (
          <div className="mb-6 p-4 bg-white rounded-xl shadow-sm border border-gray-200">
            <p className="text-sm text-gray-500">Logged in as</p>
            <p className="font-semibold text-gray-800">
              {currentUser.first_name} {currentUser.last_name}
            </p>
            <p className="text-sm text-gray-600">
              Role: {currentUser.role?.name || currentUser.role}
            </p>
            <p className="text-sm text-gray-600">
              ID: {currentUser.student_id}
            </p>
          </div>
        )}

        <p className="text-gray-500 mb-8">
          Manage identities, contexts, and audit logs
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

          {/* CONTEXT LIST */}
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-200">
            <h2 className="text-xl font-semibold mb-4">Contexts</h2>

            {contexts.map((context) => (
              <div
                key={context.id}
                className="p-3 mb-2 rounded-lg bg-gray-50 hover:bg-gray-100 transition"
              >
                {context.name}
              </div>
            ))}
          </div>

          {/* RESOLVE IDENTITY FEATURE */}
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-200">
            <ResolveIdentity contexts={contexts} />
          </div>

          {/* UPDATE DISPLAY NAME (STUDENT ONLY) */}
          {roleName === "Student" && (
            <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-200">
              <UpdateDisplayName contexts={contexts} />
            </div>
          )}

          {/* AUDIT LOGS SECTION */}
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-200 col-span-1 md:col-span-2">
            <h2 className="text-xl font-semibold mb-4">Audit Logs</h2>

            {/* restrict audit logs to registry officer */}
            {roleName !== "Registry Officer" ? (
              <p className="text-gray-500">
                Audit logs are restricted to administrative users.
              </p>
            ) : auditLogs.length === 0 ? (
              <p>No audit logs yet.</p>
            ) : (
              auditLogs.map((log) => (
                <div
                  key={log.id}
                  className="p-4 mb-3 rounded-xl bg-white border border-gray-200 shadow-sm"
                >
                  <p className="text-sm">
                    <span className="font-semibold text-gray-800">
                      {log.actor}
                    </span>{" "}
                    resolved{" "}
                    <span className="font-semibold text-gray-800">
                      {log.target_user}
                    </span>
                  </p>

                  <p className="text-gray-500 text-sm mt-1">
                    {log.context}
                  </p>

                  <div className="flex justify-between items-center mt-2">
                    <span
                      className={`text-xs font-semibold px-2 py-1 rounded ${
                        log.status === "SUCCESS"
                          ? "bg-green-100 text-green-700"
                          : "bg-red-100 text-red-700"
                      }`}
                    >
                      {log.status}
                    </span>

                    <span className="text-xs text-gray-400">
                      {new Date(log.timestamp).toLocaleString()}
                    </span>
                  </div>
                </div>
              ))
            )}
          </div>

        </div>
      </div>
    </div>
  );
}

export default Dashboard;