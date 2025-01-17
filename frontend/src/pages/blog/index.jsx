import styles from "./styles.module.scss";
import { Header, Footer } from "../../components";
import { vector } from "../../imgs";
import { useEffect } from "react";
import { News } from "../../components";
import PostService from "../../services/PostService";
import data from "./data";
export const Blog = (props) => {
  const pickNews = async (e) => {
    try {
      const responce = await PostService?.getPosts();
      console.log(responce);
    } catch {
      console.log(e.responce?.data?.message);
    }
  };
  useEffect(() => {
    console.log("загрузка новостей");
    pickNews();
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
