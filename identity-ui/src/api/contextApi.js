import apiClient from "./apiClient";

// context api that fetches all
// available contexts from backend
export const getContexts = async () => {
  const response = await apiClient.get("/api/contexts/");
  return response.data;
};