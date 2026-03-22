import apiClient from "./apiClient";

// audit api that retrieves
// audit logs for administrative users
export const getAuditLogs = async () => {
  const response = await apiClient.get("/api/audit/logs/");
  return response.data;
};