import { useState } from "react";
import { resolveIdentity } from "../api/identityApi";

// resolve identity component that allows users
// to resolve identity using identifier and context
function ResolveIdentity({ contexts }) {

  // store user input and response state
  const [externalIdentifier, setExternalIdentifier] = useState("");
  const [contextId, setContextId] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);


  // handle identity resolution sends request
  //  to the backend and updates state

  const handleResolve = async () => {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const data = await resolveIdentity(externalIdentifier, contextId);

      // store successful response
      setResult(data);
    } catch (err) {
      // extract and display error message
      setError(
        err.response?.data?.detail ||
        err.response?.data?.error ||
        "Identity resolution failed"
      );
    } finally {
      // stop loading state
      setLoading(false);
    }
  };


  // ui render and it includes input
  // fields, button, success and error states

  return (
    <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-200">
      <h2 className="text-lg font-semibold mb-4 text-gray-800">
        Resolve Identity
      </h2>

      {/* INPUTS */}
      <div className="space-y-4">

        <div>
          <label className="block text-sm text-gray-600 mb-1">
            External Identifier
          </label>
          <input
            placeholder="e.g. STD-100"
            value={externalIdentifier}
            onChange={(e) => setExternalIdentifier(e.target.value)}
            className="w-full border border-gray-300 p-2.5 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="block text-sm text-gray-600 mb-1">
            Context
          </label>
          <select
            value={contextId}
            onChange={(e) => setContextId(e.target.value)}
            className="w-full border border-gray-300 p-2.5 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Select Context</option>
            {contexts.map((context) => (
              <option key={context.id} value={context.id}>
                {context.name}
              </option>
            ))}
          </select>
        </div>

        <button
          onClick={handleResolve}
          disabled={loading}
          className="w-full bg-blue-600 text-white py-2.5 rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
        >
          {loading ? "Resolving..." : "Resolve Identity"}
        </button>
      </div>

      {/* SUCCESS RESULT */}
      {result && (
        <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg">
          <p className="text-green-700 font-semibold mb-2">
            ✔ Identity Found
          </p>
          <p className="text-sm text-gray-700">
            <strong>Name:</strong> {result.display_name}
          </p>
          <p className="text-sm text-gray-700">
            <strong>Identifier:</strong> {result.external_identifier}
          </p>
          <p className="text-sm text-gray-700">
            <strong>Context:</strong> {result.context}
          </p>
        </div>
      )}

      {/* ERROR MESSAGE */}
      {error && (
        <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-red-700 font-semibold">
            ❌ {error}
          </p>
        </div>
      )}
    </div>
  );
}

export default ResolveIdentity;