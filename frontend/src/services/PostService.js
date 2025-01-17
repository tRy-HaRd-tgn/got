import $api from "../http";
export default class PostService {
  static async getPost(id) {
    // получение поста по id
    return $api.post(`/api/posts/${id}`, { id });
  }
  static async updatePost(id) {
    // обновление информации поста
    return $api.put(`/api/posts/${id}`, { id });
  }
  static async getPosts() {
    // получение всех постов
    return $api.get("/api/posts");
  }
  static async createPost() {
    return $api.post("/api/posts");
  }
  static async getPostImg(id) {
    return $api.get(`/api/posts/${id}/image`);
  }
}
