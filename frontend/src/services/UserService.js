import $api from "../http";
export default class UserService {
  static async login(username, password) {
    return $api.post("/users/login", {
      username,
      password,
    });
  }

  static async registration(login, email, password) {
    return $api.post("/users/register", {
      login,
      email,
      password,
    });
  }
  static async getProfile() {
    return $api.get("/users/profile");
  }
  static async logout() {
    return $api.post("/users/logout");
  }
  static async checkAuth() {
    // проверка refresh токена
    return $api.post("/users/refresh-token");
  }
}
