import styles from "./styles.module.scss";
import { Header, Footer } from "../../components";
import { vector } from "../../imgs";
import { useState } from "react";
import { priviligies, pets, mounts, other } from "./data";
import { DonateComp } from "../../components";
export const Donate = (props) => {
  const [choise, setChoise] = useState("");
  const func = (state) => {
    switch (state) {
      case "privileges": {
        return priviligies.map((value, index) => (
          <DonateComp text={value.text} price={value.price} key={index} />
        ));
      }
      case "pets": {
        return pets.map((value, index) => <DonateComp key={index} />);
      }
      case "mounts": {
        return mounts.map((value, index) => <DonateComp key={index} />);
      }
      case "other":
        {
          return other.map((value, index) => <DonateComp key={index} />);
        }
        return;
    }
  };
  return (
    <main className={styles.main}>
      <Header />
      <div className={styles.description}>
        <h1 className={styles.h1}>донат магазин</h1>
        <div className={styles.descriptionDiv}>
          <button
            className={styles.descriptionDivButton}
            onClick={() => setChoise("privileges")}
          >
            Привилегии
          </button>
          <button
            className={styles.descriptionDivButton}
            onClick={() => setChoise("pets")}
          >
            питомцы
          </button>
          <button
            className={styles.descriptionDivButton}
            onClick={() => setChoise("mounts")}
          >
            маунты
          </button>
          <button
            className={styles.descriptionDivButton}
            onClick={() => setChoise("other")}
          >
            разное
          </button>
        </div>
        <div className={styles.donateWrapper}>{func(choise)}</div>
      </div>
      <img src={vector} alt="" className={styles.devider} />
      <div className={styles.project}></div>
      <Footer />
    </main>
  );
};
