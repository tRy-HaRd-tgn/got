import $api from "../http";
export default class SkinService {
  static async uploadSkin(url) {
    
    return $api.post(`/skins/upload-skin`, { url });
  }
  static async getSkin() {
    
    return $api.put(`/skins/get-skin`);
  }
  static async getAvatar() {
    
    return $api.get("/skins/avatar");
  }
}
