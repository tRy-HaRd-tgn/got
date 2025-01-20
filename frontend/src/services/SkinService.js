import $api from "../http";
export default class SkinService {
  static async uploadSkin(url) {
    
    return $api.post(`/users/upload-skin`, { url });
  }
  static async getSkin() {
    
    return $api.put(`/users/get-skin`);
  }
  static async getAvatar() {
    
    return $api.get("/users/avatar");
  }
}
