import axios from "axios";

// api client configuration that
// creates a reusable axios instance for all api requests
const apiClient = axios.create({
  baseURL: "http://127.0.0.1:8000",
  headers: {
    "Content-Type": "application/json",
  },
});


// request interceptor
// automatically attaches jwt token to every request
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("access");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

export default apiClient;