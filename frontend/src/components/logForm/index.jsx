import { useEffect } from "react";
import styles from "./styles.module.scss";
import { useSelector, useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
export const LogForm = ({ setState, state }) => {
  const navigator = useNavigate();
  const auth = useSelector((state) => state.auth.isAuth);
  const dispatch = useDispatch();
  const setAuth = () => {
    dispatch({ type: "SET_AUTH", isAuth: true });
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
      />
      <input
        placeholder={"Пароль"}
        className={styles.descriptionFormInput}
        type="password"
      />
      <div className={styles.descriptionFormButtons}>
        <button
          style={{ background: "#181F37" }}
          className={styles.descriptionFormButton}
          onClick={(e) => {
            e.preventDefault();
            try {
              const responce = await AuthService.login(email, password);
              console.log(responce);
              localStorage.setItem("token", responce.data.accessToken);
              setAuth(true);
              setInfo(responce.data.user);
              setPassword("");
            } catch (e) {
              setError(true);
              setPassword("");
              console.log(e.responce?.data?.message);
            }


            navigator("/");
          }}
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
