import styles from "./styles.module.scss";
import { NavBar } from "../navBar";
export const Footer = (props) => {
  return (
    <footer className={styles.footer}>
      <div className={styles.wrapper}>
        <div className={styles.wrapperLeft}>
          <h2 className={styles.wrapperLeftH2}>TORTUGA GOT</h2>
          <p
            style={{ width: "55%", fontFamily: "pieces-of-eight-cyrillic-aa",fontSize:"20px" }}
          >
            Мы предоставляем ознакомительный бесплатный вариант игры minecraft,
            купить лицензионную версию игры можно  здесь.
          </p>
        </div>
        <div className={styles.wrapperRight}>
          <NavBar />
        </div>
      </div>
    </footer>
  );
};
