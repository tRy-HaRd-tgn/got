import styles from "./styles.module.scss";
import { Header, Footer } from "../../components";
import { vector } from "../../imgs";
import { useEffect } from "react";
import { News } from "../../components";
import data from "./data";
export const Blog = (props) => {
  useEffect(() => {
    console.log("загрузка новостей");
  }, []);
  return (
    <main className={styles.main}>
      <Header />
      <div className={styles.description}>
        <h1 style={{ marginTop: "20vh" }}>новости проекта</h1>
      </div>
      <div className={styles.newsWrapper}>
        {data.map((value, index) => (
          <News
            key={index}
            header={value.header}
            author={value.creator}
            data={value.data}
            text={value.text}
          ></News>
        ))}
      </div>
      <img src={vector} alt="" className={styles.devider} />

      <div className={styles.project}></div>
      <Footer />
    </main>
  );
};
