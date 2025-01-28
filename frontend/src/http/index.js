import axios from "axios";

export const API_URL = "https://tortugagot.com/api";
export const API_URL2 = "https://tortugagot.com";

const $api = axios.create({
  withCredentials: true,
  baseURL: API_URL,
});

$api.interceptors.request.use((config) => {
  config.headers.Authorization = `Bearer ${localStorage.getItem("token")}`;
  return config;
});

$api.interceptors.response.use(
  (config) => {
    return config;
  },
  async (error) => {
    if (error.response.status == 401) {
      const originalRequest = error.config;
      try {
        const response = await AuthService.checkAuth();
        console.log(response);
        localStorage.setItem("token", response.data.accessToken);
        return $api.request(originalRequest);
      } catch (e) {
        console.log("НЕ АВТОРИЗОВАН");
      }
    }
  }
);

export default $api;
