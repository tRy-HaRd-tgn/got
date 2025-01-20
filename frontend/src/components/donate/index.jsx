import styles from "./styles.module.scss";
export const DonateComp = ({ price, img, color, text }) => {
  return (
    <div className={styles.wrapper}>
      <img className={styles.wrapperImg} src={img} alt="error" />
      <p className={styles.wrapperHeader}>{text}</p>
      <p className={styles.priceP}>
        {price}
        <span style={{ marginLeft: "15px" }}>золотых</span>
      </p>
      <button className={styles.btn}>Купить</button>
    </div>
  );
};
