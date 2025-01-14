import styles from "./styles.module.scss";
import { gold } from "../../imgs";
export const DonateComp = ({ price, color, text }) => {
  return (
    <div className={styles.wrapper}>
      <img className={styles.wrapperImg} src={gold} alt="error" />
      <p className={styles.wrapperHeader}>{text}</p>
      <p className={styles.priceP}>
        {price}
        <span style={{ marginLeft: "15px" }}>золотых</span>
      </p>
      <button className={styles.btn}>Купить</button>
    </div>
  );
};
