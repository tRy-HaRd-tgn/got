import styles from "./styles.module.scss";
import { useState } from "react";
import { useEffect } from "react";
export const DonateComp = ({ price, img, color, text }) => {
  const [image, setImage] = useState(null);
  useEffect(() => {
    console.log(img);
    setImage("http://localhost:8000"+img);
  }, []);
  return (
    <div className={styles.wrapper}>
      <img className={styles.wrapperImg} src={image} alt="error" />
      <p className={styles.wrapperHeader}>{text}</p>
      <p className={styles.priceP}>
        {price}
        <span style={{ marginLeft: "15px" }}>золотых</span>
      </p>
      <button className={styles.btn}>Купить</button>
    </div>
  );
};
