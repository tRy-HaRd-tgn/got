import $api from "../http";
export default class UserService {
  static async login(email, password) {
    return $api.post("/api/users/login", { email, password });
  }
  static async registration(email, password) {
    return $api.post("/api/users/register", { email, password });
  }
  static async logout() {
    return $api.post("/api/users/logout");
  }
  static async checkAuth() {
    return $api.post("/api/users/refresh-token");
  }
  static async getProfile() {
    return $api.get("/api/users/profile");
  }
}
