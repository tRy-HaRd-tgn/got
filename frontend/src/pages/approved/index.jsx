import styles from "./styles.module.scss";
export const Approved = () => {
  return (
    <div className={styles.container}>
      Оплата прошла успешно
      <a href="/main">вернуться на сайт</a>
    </div>
  );
};
