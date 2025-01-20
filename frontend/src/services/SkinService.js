import $api from "../http";
export default class SkinService {
  static async uploadSkin(url) {
    // получение поста по id
    return $api.post(`/users/upload-skin`, { url });
  }
  static async getSkin() {
    // обновление информации поста
    return $api.put(`/users/get-skin`);
  }
  static async getAvatar() {
    // получение всех постов
    return $api.get("/users/avatar");
  }
}
