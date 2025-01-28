import styles from "./styles.module.scss";
import { NavBar } from "../navBar";
import { useNavigate } from "react-router-dom";
import { useSelector } from "react-redux";
import UserService from "../../services/UserService";
import { useDispatch } from "react-redux";
import { useEffect } from "react";
export const Header = () => {
  const dispatch = useDispatch();
  const isAuth = useSelector((state) => state.auth.isAuth);
  const nickname = useSelector((state) => state.user.nickname);
  const dontate = useSelector((state) => state.user.donate);
  const setAuth = (temp) => dispatch({ type: "SET_AUTH", isAuth: temp });
  const choise = useSelector((state) => state.menu.choise);
  const setChoise = (temp) => dispatch({ type: "SET_CHOISE", choise: temp });
  const router = useNavigate();
  const avatar = useSelector((state) => state.user.profilePhoto);
  useEffect(() => {
    const href = window.location.href;
    if (href.includes("blog")) setChoise("блог");
    if (href.includes("donate")) setChoise("донат");
    if (href.includes("letsPlay")) setChoise("начать игру");
    if (href.includes("main")) setChoise("главная");
    if (href.includes("profile")) setChoise("");
  }, []);
  return (
    <header className={styles.header}>
      <div className={styles.container}>
        <NavBar />
        <div className={styles.menu}>
          <p
            style={choise == "главная" ? { color: "white" } : {}}
            className={styles.menuP}
            onClick={() => {
              setChoise("главная");
              router("/main");
            }}
          >
            Главная
          </p>
          <p
            style={choise == "блог" ? { color: "white" } : {}}
            className={styles.menuP}
            onClick={() => {
              router("/blog");
              setChoise("блог");
            }}
          >
            БЛОГ
          </p>
          <p
            style={{
              fontSize: "24px",
              color: "white",
            }}
            className={styles.menuP}
            onClick={() => {
              router("/main");
            }}
          >
            TORTUGA GOT
          </p>
          <p
            style={choise == "донат" ? { color: "white" } : {}}
            className={styles.menuP}
            onClick={() => {
              router("/donate");
              setChoise("донат");
            }}
          >
            ДОНАТ
          </p>
          <p
            style={choise == "начать игру" ? { color: "white" } : {}}
            className={styles.menuP}
            onClick={() => {
              router("/letsPlay");
              setChoise("начать игру");
            }}
          >
            НАЧАТЬ ИГРУ
          </p>
        </div>
        {!isAuth ? (
          <button className={styles.authBtn} onClick={() => router("/logReg")}>
            Авторизация
          </button>
        ) : (
          <div className={styles.userInfo} onClick={() => router("/profile")}>
            <img className={styles.avatar} src={avatar} alt="error" />
            <div style={{ marginLeft: "5%" }}>
              <p
                className={styles.userInfoP}
                style={{ fontSize: "28px", color: "white" }}
              >
                {nickname}
              </p>
              <p className={styles.userInfoP}>{dontate + " "} Золотых</p>
              <button
                onClick={async () => {
                  try {
                    const responce = await UserService.logout();
                    console.log(responce);
                    localStorage.removeItem("token");
                    setAuth(false);
                    router("/main");
                    location.reload();
                  } catch (e) {
                    console.log(e.responce?.data?.message);
                  }
                }}
                className={styles.userInfoBtn}
              >
                выход
              </button>
            </div>
          </div>
        )}
      </div>
    </header>
  );
};
