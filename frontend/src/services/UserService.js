import $api from "../http";
export default class UserService {
  static async login(login, password) {
    return $api.post("/api/users/login", { login, password });
  }
  static async registration(login, email, password) {
    return $api.post("/api/users/register", { login, email, password });
  }
  static async getProfile() {
    return $api.get("/api/users/profile");
  }
  static async logout() {
    return $api.post("/api/users/logout");
  }
  static async checkAuth() {
    return $api.post("/api/users/refresh-token");
  }
}
