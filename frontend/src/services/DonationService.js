import $api from "../http";
export default class DonationService {
  static async getDonations() {
    // get all donations
    return $api.get("/donations");
  }
  static async createDonation() {
    //crete donation
    return $api.post("/donations");
  }
  static async getDonationByCategory(category) {
    // получить донат по категории
    return $api.get(`/donations/${category}`);
  }
  static async buyDonation(donationId) {
    // покупка доната
    return $api.post(`/donations/${donationId}/buy`);
  }
  static async updateDonation(donationId) {
    // обновить донат
    return $api.put(`/donations/${donationId}`);
  }
}
