import styles from "./styles.module.scss";
import { NavBar } from "../navBar";
import { useNavigate } from "react-router-dom";
export const Footer = (props) => {
  const navigator = useNavigate();
  return (
    <footer className={styles.footer}>
      <div className={styles.wrapper}>
        <div className={styles.wrapperLeft}>
          <h2 className={styles.wrapperLeftH2}>TORTUGA GOT</h2>
          <p
            style={{
              width: "55%",
              fontFamily: "pieces-of-eight-cyrillic-aa",
              fontSize: "20px",
            }}
          >
            Мы предоставляем ознакомительный бесплатный вариант игры minecraft,
            купить лицензионную версию игры можно  здесь.
          </p>
        </div>
        <p
          style={{
            width: "55%",
            fontFamily: "pieces-of-eight-cyrillic-aa",
            fontSize: "30px",
          }}
        >
          developed by{" "}
          <span style={{ color: "white", cursor: "pointer" }}>
            <a href="https://t.me/right_wing_it">@RightWingIt</a>
          </span>
        </p>
        <div className={styles.wrapperRight}>
          <NavBar />
        </div>
      </div>
    </footer>
  );
};
