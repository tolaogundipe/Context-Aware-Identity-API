import apiClient from "../api/apiClient";


// authentication service that handles
// login and token generation
export const login = async (username, password) => {
  const response = await apiClient.post("/api/token/", {
    username,
    password,
  });

  return response.data;
};


// current user service that fetches the details
// of the logged-in user
export const getCurrentUser = async (token) => {
  const response = await apiClient.get("/api/users/me/", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return response.data;
};