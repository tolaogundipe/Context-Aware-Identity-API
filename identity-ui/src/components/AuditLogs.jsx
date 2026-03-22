import { useEffect, useState } from "react";
import { getAuditLogs } from "../api/auditApi";

// audit logs component that fetches
// and displays audit logs from backend
function AuditLogs() {

  // store audit logs in state
  const [logs, setLogs] = useState([]);


  // load audit logs on component mount so it
  // handles api call and updates state
  useEffect(() => {
    async function loadLogs() {
      try {
        const data = await getAuditLogs();

        // handle paginated and non-paginated responses
        if (data.results) {
          setLogs(data.results);
        } else {
          setLogs(data);
        }
      } catch (error) {
        // log error if request fails
        console.error("Failed to load audit logs", error);
      }
    }

    loadLogs();
  }, []);


  // render audit logs ui
  // it displays logs or fallback message if empty
  return (
    <div className="bg-white p-6 rounded shadow">
      <h2 className="text-xl font-semibold mb-4">Audit Logs</h2>

      {logs.length === 0 && (
        <p>No audit logs available.</p>
      )}

      {logs.map((log) => (
        <div key={log.id} className="border p-2 mb-2 rounded">
          <p><strong>Actor:</strong> {log.actor}</p>
          <p><strong>Target:</strong> {log.target_user}</p>
          <p><strong>Context:</strong> {log.context}</p>
          <p><strong>Action:</strong> {log.action}</p>
          <p><strong>Time:</strong> {log.timestamp}</p>
        </div>
      ))}
    </div>
  );
}

export default AuditLogs;