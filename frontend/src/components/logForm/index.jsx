import UserService from "../../services/UserService";
import styles from "./styles.module.scss";
import { useSelector, useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
export const LogForm = ({ setState, state }) => {
  const [login, setLogin] = useState("");
  const [password, setPassword] = useState("");
  const navigator = useNavigate();
  const auth = useSelector((state) => state.auth.isAuth);
  const dispatch = useDispatch();
  const setAuth = () => {
    dispatch({ type: "SET_AUTH", isAuth: true });
  };
  const logSubmit = async (e) => {
    e.preventDefault();
    try {
      const responce = await UserService.login(login, password);
      console.log(responce);
      localStorage.setItem("token", responce.data.accessToken);
      setInfo(responce.data.user);
      setAuth(true);
    } catch (e) {
      console.log(e.responce?.data?.message);
    }
    navigator("/");
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
