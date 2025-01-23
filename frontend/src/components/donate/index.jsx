import styles from "./styles.module.scss";
import { useState } from "react";
import { useEffect } from "react";
import { useDispatch } from "react-redux";
export const DonateComp = ({ setModal, price, img, color, text }) => {
  const dispatch = useDispatch();
  function hexToDec(hex) {
    return parseInt(hex, 16);
  }
  const setColor2 = (temp) => {
    dispatch({ type: "SET_COLOR", color: temp });
  };
  const setImage2 = (temp) => {
    dispatch({ type: "SET_IMAGE", image: temp });
  };

  const [rr, setRr] = useState(false);
  const [gg, setGg] = useState(false);
  const [bb, setBb] = useState(false);
  const [image, setImage] = useState(null);
  useEffect(() => {
    setImage("http://localhost:8000" + img);
    setRr(hexToDec(color[1] + color[2]));
    setGg(hexToDec(color[3] + color[4]));
    setBb(hexToDec(color[5] + color[6]));
  }, []);
  return (
    <div
      style={{
        background: `linear-gradient(
      180deg,
      rgba(${rr}, ${gg}, 73, 0.0625) 0%,
      rgba(${rr}, ${gg}, ${bb}, 0.25) 100%
    ),
    linear-gradient(180deg, #111111 0%, #111111 50%, #1a1a1a 100%)`,
      }}
      className={styles.wrapper}
    >
      <img className={styles.wrapperImg} src={image} alt="error" />
      <p className={styles.wrapperHeader}>{text}</p>
      <p className={styles.priceP}>
        {price}
        <span style={{ marginLeft: "15px" }}>золотых</span>
      </p>
      <button
        onClick={() => {
          setModal(true);
          setColor2(color);
          setImage2(image);
        }}
        className={styles.btn}
      >
        Купить
      </button>
    </div>
  );
};
