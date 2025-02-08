import $api from "../http";
export default class PaymentService {
  static async addBalance(amount) {
    return $api.post("/payments/topup", amount);
  }
}
