import styles from "./styles.module.scss";
import { useState } from "react";
import { useEffect } from "react";
import { useDispatch } from "react-redux";
import { ModalIcon } from "../modalIcon";
export const DonateComp = ({ description, price, img, color, text }) => {
  function hexToDec(hex) {
    return parseInt(hex, 16);
  }
  const [modal, setModal] = useState(false);
  const [rr, setRr] = useState();
  const [gg, setGg] = useState();
  const [bb, setBb] = useState();
  const [temp, setTemp] = useState();
  const [image, setImage] = useState(null);
  useEffect(() => {
    setImage("http://localhost:8000" + img);
    setRr(hexToDec(color[1] + color[2]));
    setGg(hexToDec(color[3] + color[4]));
    setBb(hexToDec(color[5] + color[6]));
  }, []);
  return (
    <>
      <ModalIcon style={{ width: "100vw" }} active={modal} setState={setModal}>
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            width: "100%",
            height: "100%",
          }}
        >
          <div
            className={styles.imgWrapper}
            style={{
              background: `linear-gradient(
          180deg,
          rgba(${rr}, ${gg}, ${bb}, 0.0625) 0%,
          rgba(${rr}, ${gg}, ${bb}, 0.25) 100%
        ),
        linear-gradient(180deg, #111111 0%, #111111 50%, #1a1a1a 100%)`,
            }}
          >
            <img style={{ width: "70%", height: "40%" }} src={image} alt="" />
          </div>
          <div
            style={{
              width: "60%",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
            }}
          >
            <div className={styles.rightWrapper}>
              <div className={styles.rightWrapperUp}>
                <p className={styles.p}>{text}</p>
                <button
                  onClick={() => setModal(false)}
                  className={styles.close}
                >
                  X
                </button>
              </div>
              <div className={styles.description}>{description}</div>
              <>
                <div className={styles.first}>
                  <p style={{ fontSize: "34px" }} className={styles.p}>
                    Цена
                  </p>
                  <p style={{ fontSize: "34px" }} className={styles.p}>
                    {price} {"Золотых"}
                  </p>
                </div>
                <div className={styles.first}>
                  <p style={{ fontSize: "34px" }} className={styles.p}>
                    Промокод
                  </p>
                  <input className={styles.input} type="text" />
                </div>
              </>
              <button className={styles.btn2}>Купить</button>
            </div>
          </div>
        </div>
      </ModalIcon>
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
          }}
          className={styles.btn}
        >
          Купить
        </button>
      </div>
    </>
  );
};
