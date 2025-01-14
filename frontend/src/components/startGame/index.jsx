import styles from "./styles.module.scss";
export const StartGame = ({ index, text }) => {
  return (
    <div className={styles.component}>
      <div className={styles.componentWrapper}>
        <h2 className={styles.componentWrapperH2}>{index + 1}</h2>
        <p className={styles.componentWrapperP}>Шаг</p>
      </div>
      <p className={styles.componentP}>{text}</p>
    </div>
  );
};
