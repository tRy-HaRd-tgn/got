import styles from "./styles.module.scss";
export const RegForm = ({ setState, state }) => {
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
      />{" "}
      <input
        placeholder={"Почта"}
        className={styles.descriptionFormInput}
        type="email"
      />
      <input
        placeholder={"Пароль"}
        className={styles.descriptionFormInput}
        type="password"
      />
      <input
        placeholder={"Повторите пароль"}
        className={styles.descriptionFormInput}
        type="password"
      />
      <div className={styles.descriptionFormButtons}>
        <button
          style={{ background: "#181F37" }}
          className={styles.descriptionFormButton}
          onClick={(e) => {
            e.preventDefault();
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
          Есть аккаунт?
        </button>
      </div>
    </form>
  );
};
