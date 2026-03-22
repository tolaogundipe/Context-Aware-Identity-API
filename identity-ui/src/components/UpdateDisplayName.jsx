import { useState } from "react";
import { updateDisplayName } from "../api/identityApi";


// update display name component
// allows users to update their identity display name per context

function UpdateDisplayName({ contexts }) {

  // store input values and response states
  const [contextId, setContextId] = useState("");
  const [displayName, setDisplayName] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);


  // handles display name update and sends
  // update request to backend and updates state
  const handleUpdate = async () => {
    setLoading(true);
    setMessage("");
    setError("");

    try {
      const data = await updateDisplayName(contextId, displayName);

      // store success message
      setMessage(data.message);
    } catch (err) {
      // extract and display error message
      setError(
        err.response?.data?.error || "Failed to update display name"
      );
    } finally {
      // stop loading state
      setLoading(false);
    }
  };


  // render the ui including context selection,
  // input field, and feedback messages
  return (
    <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-200">
      <h2 className="text-lg font-semibold mb-4 text-gray-800">
        Update Display Name
      </h2>

      <div className="space-y-4">

        <select
          value={contextId}
          onChange={(e) => setContextId(e.target.value)}
          className="w-full border p-2 rounded"
        >
          <option value="">Select Context</option>
          {contexts.map((c) => (
            <option key={c.id} value={c.id}>
              {c.name}
            </option>
          ))}
        </select>

        <input
          placeholder="New display name"
          value={displayName}
          onChange={(e) => setDisplayName(e.target.value)}
          className="w-full border p-2 rounded"
        />

        <button
          onClick={handleUpdate}
          disabled={loading}
          className="w-full bg-green-600 text-white py-2 rounded"
        >
          {loading ? "Updating..." : "Update Name"}
        </button>

        {message && <p className="text-green-600">{message}</p>}
        {error && <p className="text-red-600">{error}</p>}
      </div>
    </div>
  );
}

export default UpdateDisplayName;