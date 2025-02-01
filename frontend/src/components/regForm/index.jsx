import styles from "./styles.module.scss";
import { useState } from "react";
import UserService from "../../services/UserService";
export const RegForm = ({ setState, state }) => {
  const [error, setError] = useState();
  const [success, setSuccess] = useState("");
  const [login, setLogin] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [secPassword, setSecPassword] = useState("");
  const [focus, setFocus] = useState(false);
  const [secError, setSecError] = useState(false);
  const [secFocus, setSecFocus] = useState(false);
  const submitForm = async (e) => {
    e.preventDefault();
    if (password == secPassword) {
      try {
        const responce = await UserService.registration(login, email, password);
        if (responce.status === 422) {
          throw new Error("ошибка валидации");
        }
        setLogin("");
        setPassword("");
        setEmail("");
        setSecPassword("");
        setSuccess(true);
        setError(false);
      } catch (e) {
        setSuccess(false);
        setError(true);
        setEmail("");
        setPassword("");
        setLogin("");
        setSecPassword("");
        console.log(e.responce?.data?.message);
      }
    } else {
      console.log("Пароли не совпадают");
      setSecError(true);
      setSuccess(false);
      setEmail("");
      setPassword("");
      setLogin("");
      setSecPassword("");
    }
  };
  return (
    <form className={styles.descriptionForm} action="">
      <h2 className={styles.descriptionFormH2}>Регистрация</h2>
      <h4 className={styles.descriptionFormH4}>
        Добро пожаловать, введите свои данные, чтобы продолжить!
      </h4>
      {focus ? (
        <p className={styles.error}>Логин не должен содержать цифры</p>
      ) : (
        <></>
      )}
      <input
        placeholder={"Логин"}
        title="Логин не должен содержать цифр"
        className={styles.descriptionFormInput}
        type="text"
        value={login}
        onClick={() => {
          setError(false);
        }}
        onFocus={() => {
          setFocus(true);
          setError(false);
          setSecError(false);
        }}
        onBlur={() => setFocus(false)}
        onChange={(e) => setLogin(e.target.value)}
      />{" "}
      <input
        placeholder={"Почта"}
        className={styles.descriptionFormInput}
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        onFocus={() => {
          setError(false);
          setSecError(false);
        }}
      />
      {secFocus ? (
        <p
          style={{ paddingLeft: "5%", paddingRight: "5%" }}
          className={styles.error}
        >
          Пароль должен быть длиной от 8 символов, содержать хотя бы одну букву,
          одну цифру и один из специальных символов:{" "}
          <span style={{ fontFamily: "segoe ui" }}>@$!%*?&</span>.
        </p>
      ) : (
        <></>
      )}
      <input
        placeholder={"Пароль"}
        title="Пароль должен быть длиной от 8 символов, содержать хотя бы одну букву, одну цифру и один из специальных символов: @$!%*?&."
        className={styles.descriptionFormInput}
        type="password"
        value={password}
        onBlur={() => setSecFocus(false)}
        onChange={(e) => setPassword(e.target.value)}
        onFocus={() => {
          setSecFocus(true);
          setError(false);
          setSecError(false);
        }}
      />
      <input
        placeholder={"Повторите пароль"}
        className={styles.descriptionFormInput}
        type="password"
        value={secPassword}
        onChange={(e) => setSecPassword(e.target.value)}
        onFocus={() => {
          setError(false);
          setSecError(false);
        }}
      />
      {secError ? (
        <div className={styles.error}>пароли не совпадают</div>
      ) : (
        <></>
      )}
      {error ? <div className={styles.error}>ошибка регистрации</div> : <></>}
      {success ? (
        <div className={styles.text}>подтвердите создание в почтовом ящике</div>
      ) : (
        <></>
      )}
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