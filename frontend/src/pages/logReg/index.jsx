import styles from "./styles.module.scss";
import { Header, Footer,LogForm, RegForm } from "../../components";
import { vector } from "../../imgs";
import { useState } from "react";
export const LogReg = (props) => {
  const [state, setState] = useState(false);
  return (
    <main className={styles.main}>
      <Header />
      <div className={styles.description}>
        {!state ? (
          <LogForm state={state} setState={setState} />
        ) : (
          <RegForm state={state} setState={setState} />
        )}
      </div>
      <img src={vector} alt="" className={styles.devider} />
      <Footer />
    </main>
  );
};
