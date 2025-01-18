import $api from "../http";
export default class PostService {
  static async getPost(id) {
    // получение поста по id
    return $api.post(`/posts/${id}`, { id });
  }
  static async updatePost(id) {
    // обновление информации поста
    return $api.put(`/posts/${id}`, { id });
  }
  static async getPosts() {
    // получение всех постов
    return $api.get("/posts");
  }
  static async createPost(title, content, discord_url, image) {
    return $api.post("/posts", { title, content, discord_url, image });
  }
  static async getPostImg(id) {
    return $api.get(`/posts/${id}/image`);
  }
}
