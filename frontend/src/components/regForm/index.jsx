import styles from "./styles.module.scss";
import axios from "axios";
import { useState } from "react";
import UserService from "../../services/UserService";
import { useNavigate } from "react-router-dom";
export const RegForm = ({ setState, state }) => {
  const router = useNavigate();
  const [login, setLogin] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [secPassword, setSecPassword] = useState("");
  const submitForm = async (e) => {
    e.preventDefault();
    if (password == secPassword) {
      try {
        const responce = await UserService.registration(login, email, password);
        console.log(responce);
      } catch (e) {
        console.log(e.responce?.data?.message);
      }
    }
  };
  return (
    <form className={styles.descriptionForm} action="">
      <h2 className={styles.descriptionFormH2}>Регистрация</h2>
      <h4 className={styles.descriptionFormH4}>
        Добро пожаловать, введите свои данные, чтобы продолжить!
      </h4>
      <input
        placeholder={"Логин"}
        className={styles.descriptionFormInput}
        type="text"
        value={login}
        onChange={(e) => setLogin(e.target.value)}
      />{" "}
      <input
        placeholder={"Почта"}
        className={styles.descriptionFormInput}
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        placeholder={"Пароль"}
        className={styles.descriptionFormInput}
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <input
        placeholder={"Повторите пароль"}
        className={styles.descriptionFormInput}
        type="password"
        value={secPassword}
        onChange={(e) => setSecPassword(e.target.value)}
      />
      <div className={styles.descriptionFormButtons}>
        <button
          style={{ background: "#181F37" }}
          className={styles.descriptionFormButton}
          onClick={submitForm}
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
          Есть аккаунт?
        </button>
      </div>
    </form>
  );
};
