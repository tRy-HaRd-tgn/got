import styles from "./styles.module.scss";
import { Header, Footer } from "../../components";
import { vector } from "../../imgs";
import { StartGame } from "../../components";
import { sandCastle } from "../../imgs";
import data from "./data";
export const LetsPlay = (props) => {
  return (
    <main className={styles.main}>
      <Header />
      <div className={styles.description}>
        <img className={styles.img} src={sandCastle} alt="error" />
        <h1>Начать игру</h1>
        <div className={styles.componentWrapper}>
          {data.map((value, index) => (
            <StartGame key={index} index={index} text={value.text} />
          ))}
        </div>
      </div>
      <img src={vector} alt="" className={styles.devider} />
      <Footer />
    </main>
  );
};
