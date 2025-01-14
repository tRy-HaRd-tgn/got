import styles from "./styles.module.scss";
import { NavBar } from "../navBar";
import { useNavigate } from "react-router-dom";
import { useSelector } from "react-redux";
import { profile } from "../../imgs";
export const Header = (props) => {
  const isAuth = useSelector((state) => state.auth.isAuth);
  const nickname = useSelector((state) => state.user.nickname);
  const dontate = useSelector((state) => state.user.donate);
  const router = useNavigate();
  return (
    <header className={styles.header}>
      <div className={styles.container}>
        <NavBar />
        <div className={styles.menu}>
          <p className={styles.menuP} onClick={() => router("/")}>
            Главная
          </p>
          <p className={styles.menuP} onClick={() => router("/blog")}>
            БЛОГ
          </p>
          <p
            style={{ fontSize: "24px", color: "white", cursor: "default" }}
            className={styles.menuP}
          >
            TORTUGA GOT
          </p>
          <p className={styles.menuP} onClick={() => router("/donate")}>
            ДОНАТ
          </p>
          <p className={styles.menuP} onClick={() => router("/letsPlay")}>
            НАЧАТЬ ИГРУ
          </p>
        </div>
        {!isAuth ? (
          <button className={styles.authBtn} onClick={() => router("/logReg")}>
            Авторизация
          </button>
        ) : (
          <div className={styles.userInfo} onClick={() => router("/profile")}>
            <img src={profile} alt="error" />
            <div style={{ marginLeft: "5%" }}>
              <p
                className={styles.userInfoP}
                style={{ fontSize: "28px", color: "white" }}
              >
                {nickname}
              </p>
              <p className={styles.userInfoP}>{dontate + " "} Золотых</p>
            </div>
          </div>
        )}
      </div>
    </header>
  );
};
