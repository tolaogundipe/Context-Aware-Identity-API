import apiClient from "./apiClient";

// identity resolution api that sends request to backend to 
// resolve identity using identifier and context
export const resolveIdentity = async (externalIdentifier, contextId) => {
  const response = await apiClient.post("/api/identities/resolve/", {
    external_identifier: externalIdentifier,
    context_id: contextId,
  });

  return response.data;
};

// update display name api for updating the uder's
// display name for a selected context
export const updateDisplayName = async (contextId, displayName) => {
  const response = await apiClient.patch(
    "/api/identities/update-display-name/",
    {
      context_id: contextId,
      display_name: displayName,
    }
  );

  return response.data;
};