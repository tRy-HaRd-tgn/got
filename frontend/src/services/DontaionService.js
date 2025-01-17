import $api from "../http";
export default class DonationService {
  static async getDonations() {
    // get all donations
    return $api.get("/api/donations");
  }
  static async createDonation() {
    //crete donation
    return $api.post("/api/donations");
  }
  static async getDonationByCategory(category) {
    // получить донат по категории
    return $api.get(`/api/donations/${category}`);
  }
  static async buyDonation(donationId) {
    // покупка доната
    return $api.post(`/api/donations/${donationId}/buy`);
  }
  static async updateDonation(donationId) {
    // обновить донат
    return $api.put(`/api/donations/${donationId}`);
  }
}
