import UserService from "../../services/UserService";
import SkinService from "../../services/SkinService";
import styles from "./styles.module.scss";
import { useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
export const LogForm = ({ setState, state }) => {
  const [error, setError] = useState();
  const [login, setLogin] = useState("");
  const [password, setPassword] = useState("");
  const navigator = useNavigate();
  const dispatch = useDispatch();
  const setAuth = (temp) => {
    dispatch({ type: "SET_AUTH", isAuth: temp });
  };
  const setNickName = (temp) => {
    dispatch({ type: "SET_NICKNAME", nickname: temp });
  };
  const setProfilePhoto = (temp) => {
    dispatch({ type: "SET_PROFILEPHOTO", profilePhoto: temp });
  };
  const setSkin = (temp) => {
    dispatch({ type: "SET_SKIN", skin: temp });
  };
  const setDonate = (temp) => {
    dispatch({ type: "SET_DONATE", donate: temp });
  };
  const setRegDate = (temp) => {
    dispatch({ type: "SET_REGDATE", regDate: temp });
  };
  const setEmail = (temp) => {
    dispatch({ type: "SET_EMAIL", email: temp });
  };
  const configureStore = async () => {
    const responce = await UserService.getProfile();
    setNickName(responce.data.login);
    setDonate(responce.data.balance);
    setRegDate(responce.data.created_at.split("T")[0]);
    setEmail(responce.data.email);
    const responce2 = await SkinService.getAvatar();
    console.log(responce2);
    setProfilePhoto(responce2.data.url);
    console.log(responce2)
    const responce3 = await SkinService.getSkin();
    setSkin(responce3.data.url);
  };

  const logSubmit = async (e) => {
    e.preventDefault();
    try {
      const responce = await UserService.login(login, password);
      console.log(responce);
      localStorage.setItem("token", responce.data.access_token);
      setError(false);
      setAuth(true);
      configureStore();
      navigator("/main");
    } catch (e) {
      setError(true);
      console.log(e.responce?.detail?.msg);
    }
  };
  return (
    <form className={styles.descriptionForm} action="">
      <h2 className={styles.descriptionFormH2}>Авторизация</h2>
      <h4 className={styles.descriptionFormH4}>
        Добро пожаловать, введите свои данные, чтобы продолжить!
      </h4>
      <input
        placeholder={"Логин"}
        className={styles.descriptionFormInput}
        type="text"
        value={login}
        onChange={(e) => setLogin(e.target.value)}
      />
      <input
        value={password}
        placeholder={"Пароль"}
        className={styles.descriptionFormInput}
        type="password"
        onChange={(e) => setPassword(e.target.value)}
      />
      {error ? <div className={styles.text}>ошибка авторизации</div> : <></>}
      <div className={styles.descriptionFormButtons}>
        <button
          style={{ background: "#181F37" }}
          className={styles.descriptionFormButton}
          onClick={logSubmit}
        >
          Продолжить
        </button>
        <button
          className={styles.descriptionFormButton}
          onClick={(e) => {
            e.preventDefault();
            setState(!state);
          }}
        >
          Нет аккаунта?
        </button>
      </div>
    </form>
  );
};
